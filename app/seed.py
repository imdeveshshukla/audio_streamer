from app.database import SessionLocal, engine, Base
from app.models import Clip

def seed_db():
    # Create tables synchronously
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    clips = [
        Clip(
            title="Ambient Pad",
            description="Soft atmospheric sound",
            genre="ambient",
            duration="30s",
            audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ),
        Clip(
            title="Chill Beat",
            genre="electronic",
            duration="30s",
            audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        ),
        Clip(
            title="White Noise",
            genre="ambient",
            duration="30s",
            audio_url="https://cdn.freesound.org/previews/834/834223_14312064-lq.mp3"
        ),
        Clip(
            title="Reliable Safe",
            genre="Atmospheric",
            duration="40s",
            audio_url="https://cdn.pixabay.com/audio/2025/04/15/audio_981caf755e.mp3"
        ),
        Clip(
            title="Riser Wildfire",
            genre="Swoosh",
            duration="12s",
            audio_url="https://cdn.pixabay.com/audio/2025/01/07/audio_94546afc27.mp3"
        ),
    ]

    session.add_all(clips)
    session.commit()
    session.close()

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
