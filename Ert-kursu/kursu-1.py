import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import redis.asyncio as aioredis

app = FastAPI()

# Connect to a high-speed Redis cluster/instance
redis_pool = aioredis.ConnectionPool(host='localhost', port=6379, db=0)
redis_client = aioredis.Redis(connection_pool=redis_pool)


class VotePayload(BaseModel):
    voter_id: str
    candidate_id: str
    election_id: str
    signature: str  # Cryptographic verification token


@app.post("/cast-vote", status_code=status.HTTP_202_ACCEPTED)
async def ingest_vote(vote: VotePayload):
    try:
        # 1. Quick payload transformation
        vote_data = vote.model_dump_json()

        # 2. Push directly to the tail of a Redis list (O(1) complexity, ultra fast)
        # This handles hundreds of thousands of operations per second per node
        await redis_client.rpush("voting_queue", vote_data)

        # 3. Respond immediately so the user's browser isn't hanging
        return {"status": "accepted", "message": "Vote queued securely."}

    except Exception as e:
        # Fallback if queue tier is unreachable
        raise HTTPException(status_code=503, detail="System busy, try again.")
