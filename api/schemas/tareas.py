from pydantic import BaseModel, Field
from enum import Enum


class EstadoTarea(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en progreso"
    COMPLETADA = "completada"


class PrioridadTarea(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class PayloadTarea(BaseModel):
    titulo: str = Field(min_length=3, max_length=100, description="Título de la tarea")
    descripcion: str = Field(max_length=300, description="Descripción detallada de la tarea")
    fecha_creacion: str = Field(description="Fecha de creación de la tarea")
    fecha_vencimiento: str = Field(description="Fecha límite para completar la tarea")
    estado: EstadoTarea = Field(description="Estado actual de la tarea")
    prioridad: PrioridadTarea = Field( description="Prioridad de la tarea")

    model_config = {
        "json_schema_extra": {
            "example": {
                "titulo": "Tarea 1",
                "descripcion": "Descripcion de la tarea 1",
                "fecha_creacion": "2021-01-01",
                "fecha_vencimiento": "2021-01-15",
                "estado": "pendiente",
                "prioridad": "alta"
            }
        }
    }



class PayloadTareaPatch(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    fecha_creacion: str | None = None
    fecha_vencimiento: str | None = None
    estado: str | None = None
    prioridad: str | None = None


class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str
    fecha_creacion: str
    fecha_vencimiento: str
    estado: str
    prioridad: str



class TareaResumida(BaseModel):
    id: int
    titulo: str