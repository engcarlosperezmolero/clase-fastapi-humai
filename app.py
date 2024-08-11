from fastapi import FastAPI
from api.routers.tareas import router as tareas_router

app = FastAPI(
    title="Mi primera app con FastAPI",
    description="Esta es una descripción de mi app",
    version="0.0.3",
)
app.include_router(tareas_router)


@app.get("/")
def root_message():
    return {"message": "Mi primera app con FastAPI, soy charly"}
