from fastapi import FastAPI

app = FastAPI(title="Finance Tool API")


@app.get("/health")
def health():
    return {"status": "ok"}