from fastapi import FastAPI

app = FastAPI(title="Incident Investigation API")


@app.get("/health")
def health():
    return {"status": "ok"}