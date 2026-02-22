from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models.control import Control
from backend.app.models.test_result import TestResult
from backend.app.schemas.test_result import TestResultCreate, TestResultOut, TestResultUpdate

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("", response_model=list[TestResultOut])
def list_tests(
    db: Session = Depends(get_db),
    control_id: int | None = Query(default=None),
    result: str | None = Query(default=None),  # pass/fail
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    query = db.query(TestResult)
    if control_id is not None:
        query = query.filter(TestResult.control_id == control_id)
    if result:
        query = query.filter(TestResult.result == result)

    return query.order_by(TestResult.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=TestResultOut, status_code=201)
def create_test(payload: TestResultCreate, db: Session = Depends(get_db)):
    ctrl = db.query(Control).filter(Control.id == payload.control_id).first()
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control not found for control_id")

    obj = TestResult(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{test_id}", response_model=TestResultOut)
def get_test(test_id: int, db: Session = Depends(get_db)):
    obj = db.query(TestResult).filter(TestResult.id == test_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TestResult not found")
    return obj


@router.put("/{test_id}", response_model=TestResultOut)
def update_test(test_id: int, payload: TestResultUpdate, db: Session = Depends(get_db)):
    obj = db.query(TestResult).filter(TestResult.id == test_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TestResult not found")

    data = payload.model_dump(exclude_unset=True)

    # If user wants to move to another control_id, we would validate it (not in schema now).
    for k, v in data.items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{test_id}", status_code=204)
def delete_test(test_id: int, db: Session = Depends(get_db)):
    obj = db.query(TestResult).filter(TestResult.id == test_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="TestResult not found")

    db.delete(obj)
    db.commit()
    return None
