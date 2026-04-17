from .births_table import BirthsTable
from .name_stats import NameStats
from .engine import engine, SessionLocal
from .base import Base
from .models import NameStatsTable
from pathlib import Path
from .life_table import LifeTable
import json


start_year = 1880 # the first year for which we have data is 1880
target_year = 2024 # the max year for which we have data is 2024

data_base_path = Path(__file__).parent.parent / "data"
names_base_path = data_base_path / "names"
life_tables_base_path = data_base_path / "life_tables"
life_table_female_path = life_tables_base_path / "HMD_Life_Table_Female.txt"
life_table_male_path = life_tables_base_path / "HMD_Life_Table_Male.txt"

# DATA PARSING
life_table_female = LifeTable(life_table_female_path, target_year=target_year)
life_table_male = LifeTable(life_table_male_path, target_year=target_year)

name_stats_entry_map = {} # {(name, sex): NameStats}

for year in range(start_year, target_year + 1):
    births_table_path = names_base_path / f"yob{year}.txt"
    births_table = BirthsTable(births_table_path)
    rank = {'F': 0, 'M': 0} # separate rank counters for male and female
    for name, sex, count in births_table.get_birth_list_ordered_combined():
        rank[sex] += 1
        alive_probability = (life_table_female if sex == 'F' else life_table_male).get_alive_probability(year)
        alive_count = count * alive_probability
        
        name_stats_entry = name_stats_entry_map.get((name, sex), NameStats(name, sex))
        name_stats_entry.input_year_data(year, count, alive_count, rank[sex], rank['F'] + rank['M'])
        name_stats_entry_map[(name, sex)] = name_stats_entry

name_stats_all_time_popularity_rank_non_gendered = sorted(name_stats_entry_map.values(), key=lambda x: x.total_occurrence_count, reverse=True)
name_stats_alive_popularity_rank_non_gendered = sorted(name_stats_entry_map.values(), key=lambda x: x.estimated_alive_count, reverse=True)

rank = {'F': 0, 'M': 0}
for name_stats_entry in name_stats_all_time_popularity_rank_non_gendered:
    rank[name_stats_entry.sex] += 1
    name_stats_entry.all_time_popularity_rank_non_gendered = rank['F'] + rank['M']
    name_stats_entry.all_time_popularity_rank_gendered = rank[name_stats_entry.sex]

rank = {'F': 0, 'M': 0}
for name_stats_entry in name_stats_alive_popularity_rank_non_gendered:
    rank[name_stats_entry.sex] += 1
    name_stats_entry.alive_popularity_rank_non_gendered = rank['F'] + rank['M']
    name_stats_entry.alive_popularity_rank_gendered = rank[name_stats_entry.sex]

# DATABASE INSERTION
Base.metadata.create_all(engine) # creates the tables in the database if they don't exist yet
session = SessionLocal()

session.query(NameStatsTable).delete()
session.commit()

for name_stats_entry in name_stats_entry_map.values():
    name_stats_table_entry = NameStatsTable(
        name=name_stats_entry.name,
        sex=name_stats_entry.sex,

        avg_age=name_stats_entry.compute_average_age(current_year=target_year),
        most_likely_age=name_stats_entry.compute_most_likely_age(current_year=target_year),

        occurrence_by_year=json.dumps(name_stats_entry.occurrence_by_year),
        alive_occurrence_by_year=json.dumps(name_stats_entry.alive_occurrence_by_year),

        total_occurrence_count=name_stats_entry.total_occurrence_count,
        estimated_alive_count=name_stats_entry.estimated_alive_count,

        popular_years_list=json.dumps(name_stats_entry.compute_popular_years_list()),
        age_distribution=json.dumps(name_stats_entry.compute_age_distribution(current_year=target_year)),

        all_time_popularity_rank_non_gendered=name_stats_entry.all_time_popularity_rank_non_gendered,
        all_time_popularity_rank_gendered=name_stats_entry.all_time_popularity_rank_gendered,
        alive_popularity_rank_non_gendered=name_stats_entry.alive_popularity_rank_non_gendered,
        alive_popularity_rank_gendered=name_stats_entry.alive_popularity_rank_gendered,

        baby_name_popularity_rank_non_gendered_by_year=json.dumps(name_stats_entry.baby_name_popularity_rank_non_gendered_by_year),
        baby_name_popularity_rank_gendered_by_year=json.dumps(name_stats_entry.baby_name_popularity_rank_gendered_by_year)
    )
    session.add(name_stats_table_entry)
session.commit()

# SHUTDOWN
session.close()