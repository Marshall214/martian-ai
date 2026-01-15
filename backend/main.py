from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import proof, summarize, notes, slides
from routes import auth
from database import Base, engine
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Martian AI API")

origins = [
    "http://localhost",
    "http://localhost:3000", # Frontend might run on 3000
    "http://localhost:3001", # Or 3001 if 3000 is in use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proof.router)
app.include_router(summarize.router)
app.include_router(notes.router)
app.include_router(slides.router)
app.include_router(auth.router)

# Create static directory for audio files
os.makedirs("static/audio", exist_ok=True)

# Mount static files for audio downloads
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "👽 Welcome to Martian AI Backend"}
