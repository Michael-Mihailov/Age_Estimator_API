'''

Service layer for querying name statistics from the database.
Proivdes NameStatsService, which handles all database interaction for name-based lookups
and returns structured response objects for use by the API layer.

'''

import json
from typing import Optional
from db.engine import SessionLocal
from db.models import NameStatsTable
from api.schemas.name_response import NameStatsBase, NameStatsResponseBasic, NameStatsResponseFull

class NameStatsServiceBase:
    ''' BASE CLASS '''
    ''' Service class for querying name statistics from the database. '''

    def __init__(self):
        self.db = SessionLocal()

    def get_name_query(self, name: str, sex: Optional[str] = None):
        ''' Helper method to build the base query for a given name and optional sex filter. '''
        query = self.db.query(NameStatsTable).filter(NameStatsTable.name.ilike(name))
        if sex is not None:
            query = query.filter(NameStatsTable.sex == sex)
        else: # pick the more popular sex
            query = query.order_by(NameStatsTable.all_time_popularity_rank_non_gendered.asc())

        return query.first()

    def get_name_stats(self, name: str, sex: Optional[str] = None) -> Optional[NameStatsBase]:
        ''' Query the database for statistics on a given name. '''
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def __del__(self):
        self.db.close()

class NameStatsServiceBasic(NameStatsServiceBase):
    def get_name_stats(self, name: str, sex: Optional[str] = None) -> Optional[NameStatsResponseBasic]:
        """
        Query the database for statistics on a given name.

        Args:
        name: The first name to look up (case-insensitive).
        sex: Optional sex filter ('M' or 'F'). If omitted, returns the first match regardless of sex.

        Returns:
        A NameStatsResponse object if a match is found, otherwise None.
        """
        result = self.get_name_query(name, sex)
        if not result:
            return None
        
        # Parse JSON fields
        occurrence_by_year = json.loads(result.occurrence_by_year)
        popular_years = json.loads(result.popular_years_list)

        # Calculate fields
        first_year_appeared = min(year for year in occurrence_by_year.keys())
        top_5_years = [year for year in popular_years[:5]]

        return NameStatsResponseBasic(
            name=result.name,
            sex=result.sex,
            estimated_age=result.avg_age,
            most_likely_age=result.most_likely_age,
            first_year_appeared=first_year_appeared,
            all_time_rank_gendered=result.all_time_popularity_rank_gendered,
            top_5_popular_years=top_5_years
        )

class NameStatsServiceFull(NameStatsServiceBase):
    def get_name_stats(self, name: str, sex: Optional[str] = None) -> Optional[NameStatsResponseFull]:
        ''' Implement a more detailed query and response structure. '''
        # Similar implementation to NameStatsServiceBasic but with additional fields and processing as needed.
        
        result = self.get_name_query(name, sex)
        if not result:
            return None
        
        return NameStatsResponseFull(
            name=result.name,
            sex=result.sex,
            estimated_age=result.avg_age,
            most_likely_age=result.most_likely_age,
            occurrence_by_year=json.loads(result.occurrence_by_year),
            alive_occurrence_by_year=json.loads(result.alive_occurrence_by_year),
            total_occurrence_count=result.total_occurrence_count,
            estimated_alive_count=result.estimated_alive_count,
            popular_years_list=json.loads(result.popular_years_list),
            age_distribution=json.loads(result.age_distribution),
            all_time_rank_non_gendered=result.all_time_popularity_rank_non_gendered,
            all_time_rank_gendered=result.all_time_popularity_rank_gendered,
            alive_popularity_rank_non_gendered=result.alive_popularity_rank_non_gendered,
            alive_popularity_rank_gendered=result.alive_popularity_rank_gendered,
            baby_name_popularity_rank_non_gendered_by_year=json.loads(result.baby_name_popularity_rank_non_gendered_by_year),
            baby_name_popularity_rank_gendered_by_year=json.loads(result.baby_name_popularity_rank_gendered_by_year)
        )