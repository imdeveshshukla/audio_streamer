from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app import schemas
from app import controller

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/play", response_model=list[schemas.ClipBase])
def list_clips(db: Session = Depends(get_db)):
    clips = controller.get_all_clips(db)
    return clips

@app.get("/play/{clip_id}/stats", response_model=schemas.ClipStats)
def clip_stats(clip_id: int, db: Session = Depends(get_db)):
    clip = controller.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    return clip

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)