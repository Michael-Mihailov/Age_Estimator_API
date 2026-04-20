'''

Service layer for querying name statistics from the database.
Proivdes NameStatsService, which handles all database interaction for name-based lookups
and returns structured response objects for use by the API layer.

'''

import json
from typing import Optional
from db.engine import SessionLocal
from db.models import NameStatsTable
from api.schemas.name_response import NameStatsResponse

class NameStatsService:

    def __init__(self):
        self.db = SessionLocal()

    def get_name_estimate(self, name: str, sex: Optional[str] = None) -> Optional[NameStatsResponse]:
        """
        Query the database for statistics on a given name.

        Args:
        name: The first name to look up (case-insensitive).
        sex: Optional sex filter ('M' or 'F'). If omitted, returns the first match regardless of sex.

        Returns:
        A NameStatsResponse object if a match is found, otherwise None.
        """
        query = self.db.query(NameStatsTable).filter(NameStatsTable.name.ilike(name))
        if sex is not None:
            query = query.filter(NameStatsTable.sex == sex)

        result = query.first()
        if not result:
            return None
        
        # Parse JSON fields
        occurrence_by_year = json.loads(result.occurrence_by_year)
        popular_years = json.loads(result.popular_years_list)

        # Calculate fields
        first_year_appeared = min(year for year in occurrence_by_year.keys())
        top_5_years = [year for year in popular_years[:5]]

        return NameStatsResponse(
            name=result.name,
            sex=result.sex,
            estimated_age=result.avg_age,
            most_likely_age=result.most_likely_age,
            first_year_appeared=first_year_appeared,
            all_time_rank_gendered=result.all_time_popularity_rank_gendered,
            top_5_popular_years=top_5_years
        )

    def __del__(self):
        self.db.close()