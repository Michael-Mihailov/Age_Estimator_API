from sqlalchemy import Column, String, Float, Integer, Text
from base import Base

class NameStatsTable(Base):
    __tablename__ = "name_stats"

    name = Column(String, primary_key=True)
    sex = Column(String, primary_key=True)

    avg_age = Column(Float, nullable=False) # the mathematical average
    most_likely_age = Column(Integer, nullable=False) # the mathematical mode

    occurrence_by_year = Column(Text, nullable=False) # JSON string: {year: count}
    alive_occurrence_by_year = Column(Text, nullable=False) # JSON string: {year: count}

    total_occurrence_count = Column(Integer, nullable=False) # Total number of people to ever have this name
    estimated_alive_count = Column(Float, nullable=False) # Estimated number of them still alive

    popular_years_list = Column(Text, nullable=False) # JSON string: [year1, year2, ...] sorted by occurrence count (e.g. [1990, 2000, 1980, ...] means this name was most popular in 1990, then 2000, then 1980, etc.)
    age_distribution = Column(Text, nullable=False) # JSON string {age: probability} (probability sums to 1)

    all_time_popularity_rank_non_gendered = Column(Integer, nullable=False) # The rank of this name in terms of total occurrence count
    all_time_popularity_rank_gendered = Column(Integer, nullable=False) # The rank of this name in terms of occurrence count within gender
    alive_popularity_rank_non_gendered = Column(Integer, nullable=False) # The rank of this name in terms of estimated alive count
    alive_popularity_rank_gendered = Column(Integer, nullable=False) # The rank of this name in terms of estimated alive count within gender

    baby_name_popularity_rank_non_gendered_by_year = Column(Text, nullable=False) # JSON string {year: rank} for the rank of this name among baby names in that year
    baby_name_popularity_rank_gendered_by_year = Column(Text, nullable=False) # JSON string {year: rank} for the rank of this name among baby names in that year within gender