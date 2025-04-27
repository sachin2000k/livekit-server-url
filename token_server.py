from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from livekit.api import AccessToken, VideoGrants
import os
import uvicorn

from dotenv import load_dotenv
load_dotenv()

LIVEKIT_API_KEY = os.environ["LIVEKIT_API_KEY"]
LIVEKIT_API_SECRET = os.environ["LIVEKIT_API_SECRET"]
LIVEKIT_HOST = os.environ["LIVEKIT_HOST"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    room: str
    user: str

@app.get("/api/token")
async def get_token(room: str, user: str):
    at = AccessToken(api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET)
    at.identity = user

    # VERY IMPORTANT: Give proper permissions
    grant = VideoGrants(
        room_join=True,
        room=room,
        can_publish=True,
        can_subscribe=True,
    )
    at.with_grants(grants=grant)

    token = at.to_jwt()
    return {"token": token}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
