from births_table import BirthsTable
from engine import engine, SessionLocal
from base import Base
from models import NameStatsTable
from pathlib import Path
from life_table import LifeTable


Base.metadata.create_all(engine) # creates the tables in the database if they don't exist yet
session = SessionLocal()

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

name_stats_set_female = {}
name_stats_set_male = {}

# TESTING
for year in range(target_year - 2, target_year + 1 - 2):
    births_table_path = names_base_path / f"yob{year}.txt"
    births_table = BirthsTable(births_table_path)
    for name, sex, count in births_table.get_birth_list_combined():
        alive_probability = (life_table_female if sex == 'F' else life_table_male).get_alive_probability(year)
        alive_count = count * alive_probability
        if (count > 10000):
            print(f"Processing {name} ({sex}) in {year} with count {count}...")
            print(f"{alive_count:.2f} are alive ({alive_probability*100:.2f}% of the original count)")
            print()

# SHUTDOWN
session.close()