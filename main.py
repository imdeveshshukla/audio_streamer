from fastapi import FastAPI, Depends
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)