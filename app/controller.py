from sqlalchemy.orm import Session
from app.models import Clip


def get_all_clips(db: Session):
    return db.query(Clip).all()