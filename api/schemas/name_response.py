from pydantic import BaseModel
from typing import List

class NameStatsResponse(BaseModel):
    ''' Define data contracts
        Add any additional fields you want to return in the API response here.
        Currently set up for name, sex, average age, most likely age, and popularity ranks, 
        but you can expand it as needed.
    '''
    name: str
    sex: str
    estimated_age: float
    most_likely_age: int
    first_year_appeared: int
    all_time_rank_gendered: int
    top_5_popular_years: List[int]

    class Config:
        from_attributes = True