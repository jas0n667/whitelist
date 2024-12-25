from fastapi import FastAPI
from core.base import router
app = FastAPI(title="Unified API Docs")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    