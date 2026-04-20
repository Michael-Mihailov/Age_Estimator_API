from pydantic import BaseModel
from typing import List

''' 
    BASE CLASS 
    Define data contracts for API responses.
'''
class NameStatsBase(BaseModel):
    name: str
    sex: str

    class Config:
        from_attributes = True

class NameStatsResponseBasic(NameStatsBase):
    ''' Define data contracts
        Add any additional fields you want to return in the API response here.
        Currently set up for name, sex, average age, most likely age, and popularity ranks, 
        but you can expand it as needed.
    '''
    estimated_age: float
    most_likely_age: int
    first_year_appeared: int
    all_time_rank_gendered: int
    top_5_popular_years: List[int]

class NameStatsResponseFull(NameStatsBase):
    ''' Define data contracts for a more detailed response, if needed. '''
    estimated_age: float
    most_likely_age: int

    occurrence_by_year: dict
    alive_occurrence_by_year: dict

    total_occurrence_count: int
    estimated_alive_count: float

    popular_years_list: List[int]
    age_distribution: dict

    all_time_rank_non_gendered: int
    all_time_rank_gendered: int
    alive_popularity_rank_non_gendered: int
    alive_popularity_rank_gendered: int

    baby_name_popularity_rank_non_gendered_by_year: dict
    baby_name_popularity_rank_gendered_by_year: dict