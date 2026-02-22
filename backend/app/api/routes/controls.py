from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models.control import Control
from backend.app.schemas.control import ControlCreate, ControlOut, ControlUpdate

router = APIRouter(prefix="/controls", tags=["controls"])


@router.get("", response_model=list[ControlOut])
def list_controls(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search in code/title/owner"),
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    query = db.query(Control)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Control.control_code.ilike(like)) |
            (Control.title.ilike(like)) |
            (Control.owner.ilike(like))
        )
    if status:
        query = query.filter(Control.status == status)

    return query.order_by(Control.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=ControlOut, status_code=201)
def create_control(payload: ControlCreate, db: Session = Depends(get_db)):
    existing = db.query(Control).filter(Control.control_code == payload.control_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="control_code already exists")

    obj = Control(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{control_id}", response_model=ControlOut)
def get_control(control_id: int, db: Session = Depends(get_db)):
    obj = db.query(Control).filter(Control.id == control_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Control not found")
    return obj


@router.put("/{control_id}", response_model=ControlOut)
def update_control(control_id: int, payload: ControlUpdate, db: Session = Depends(get_db)):
    obj = db.query(Control).filter(Control.id == control_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Control not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{control_id}", status_code=204)
def delete_control(control_id: int, db: Session = Depends(get_db)):
    obj = db.query(Control).filter(Control.id == control_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Control not found")

    db.delete(obj)
    db.commit()
    return None
