''' Defines API endpoints '''

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent # Adjust the path to point to the project root
sys.path.insert(0, str(project_root)) # Allow imports from the project root

from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from api.services.name_service import NameStatsService
from api.schemas.name_response import NameStatsResponse

app = FastAPI()


# API endpoint to get name statistics and age estimation
@app.get("/nameinfo", response_model=NameStatsResponse)
def estimate_age(
    name: str = Query(..., description="First name to look up"),
    sex: Optional[str] = Query(None, description="Gender filter: 'male' or 'female'")
):
    service = NameStatsService()
    result = service.get_name_estimate(name, sex)
    if result is None:
        raise HTTPException(status_code=404)
    
    return result

@app.post("/nameinfo", response_model=NameStatsResponse)
def create_name(name: str = Query(..., description="First name to create"),
                sex: str = Query(..., description="Gender: 'male' or 'female'"),
                year: str = Query(..., description="Year of birth"),
                count: int = Query(..., description="Number of occurrences")):
    pass
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)