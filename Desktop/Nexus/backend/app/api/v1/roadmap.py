"""Roadmap endpoints."

Note: full learning endpoints live in learning.py; this module exposes
roadmap routes under a dedicated prefix for backwards compatibility.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import roadmap as crud
from app.database import get_db
from app.models.learning import Roadmap
from app.schemas.learning import RoadmapOut

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])


@router.get("", response_model=list[RoadmapOut])
def list_roadmaps(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    return crud.list_roadmaps(db, category=category)


@router.get("/{roadmap_id}", response_model=RoadmapOut)
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)) -> Roadmap:
    roadmap = crud.get_roadmap(db, roadmap_id)
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    return roadmap
