import logging

import psycopg
from fastapi import FastAPI, HTTPException, Query

from app.tools import get_block_events


logger = logging.getLogger(__name__)

app = FastAPI(title="Incident Investigation API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/blocks/{block_id}/events")
def block_events(
    block_id: str,
    limit: int = Query(default=100, ge=1, le=500),
):
    try:
        return get_block_events(block_id, limit)
    except psycopg.Error:
        logger.exception("Failed to retrieve block events")

        raise HTTPException(
            status_code=503,
            detail="Could not retrieve events from the database",
        ) from None