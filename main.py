from fastapi import FastAPI, Depends, HTTPException, Header, Request
import uvicorn
from fastapi.responses import StreamingResponse
import httpx
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app import schemas
from app import controller
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Counter
Base.metadata.create_all(bind=engine)
from app.config import settings

async def verify_api_key(request: Request, x_api_key: str = Header(None)):
    # Public endpoints
    if request.url.path in ["/", "/metrics"]:
        return

    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


app = FastAPI(dependencies=[Depends(verify_api_key)])


app.add_middleware(
    PrometheusMiddleware,
    app_name="audio_streamer",
    prefix="streamer",
)

app.add_route("/metrics", handle_metrics)

stream_counter = Counter(
    "audio_streams_total",
    "Number of times a clip is streamed",
    ["clip_id"]
)

@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Audio Streaming Service",
        "version": "1.0.0",
        "description": (
            "A lightweight audio preview streaming backend built with FastAPI. "
            "Streams MP3s, tracks play counts, exposes Prometheus metrics, and runs fully in Docker."
        ),
        "endpoints": {
            "public": ["/", "/metrics"],
            "protected": [
                "/play",
                "/play/{id}/stream",
                "/play/{id}/stats",
                "/play (POST)"
            ]
        },
        "note": (
            "All /play routes are protected by an API key. "
            "To get access, please contact Devesh. "
        ),
        "repo": "https://github.com/imdeveshshukla/audio_streamer",
        "developer": "Devesh Shukla"
    }


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

@app.get("/play/{clip_id}/stream")
async def stream_proxy(clip_id: int, db: Session = Depends(get_db)):
    clip = controller.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    async def iterfile():
        first_chunk = True
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", clip.audio_url) as r:
                async for chunk in r.aiter_bytes():
                  if first_chunk:
                    controller.increment_play_count(db, clip_id)
                    stream_counter.labels(clip_id=str(clip_id)).inc()
                    first_chunk = False
                  yield chunk

    return StreamingResponse(iterfile(), media_type="audio/mpeg")


@app.post("/play", response_model=schemas.ClipBase)
def create_new_clip(clip: schemas.ClipCreate, db: Session = Depends(get_db)):
    new_clip = controller.create_clip(db, clip)
    return new_clip

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)