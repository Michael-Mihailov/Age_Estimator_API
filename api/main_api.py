''' Defines API endpoints '''

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent # Adjust the path to point to the project root
sys.path.insert(0, str(project_root)) # Allow imports from the project root

from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from api.services.name_service import NameStatsServiceBasic, NameStatsServiceFull
from api.schemas.name_response import NameStatsResponseBasic, NameStatsResponseFull

app = FastAPI()


# API endpoints to get name statistics and age estimation
@app.get("/name-stats-basic", response_model=NameStatsResponseBasic)
def get_name_stats_basic(
    name: str = Query(..., description="First name to look up"),
    sex: Optional[str] = Query(None, description="Gender filter: 'M' or 'F'")
):
    service = NameStatsServiceBasic()
    result = service.get_name_stats(name, sex)
    if result is None:
        raise HTTPException(status_code=404)
    
    return result

@app.get("/name-stats-full", response_model=NameStatsResponseFull)
def get_name_stats_full(
    name: str = Query(..., description="First name to look up"),
    sex: Optional[str] = Query(None, description="Gender filter: 'M' or 'F'")
):
    service = NameStatsServiceFull()
    result = service.get_name_stats(name, sex)
    if result is None:
        raise HTTPException(status_code=404)

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)