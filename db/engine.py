from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_path = Path(__file__).parent.parent / "data" / "names.db"

engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)