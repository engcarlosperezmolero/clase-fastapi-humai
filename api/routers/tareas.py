import os
from fastapi import APIRouter, Query, Path, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
from fastapi.exceptions import HTTPException
from api.data.base_de_datos import tabla_tareas
from api.schemas.tareas import TareaResumida, Tarea, PayloadTarea, PayloadTareaPatch

router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)

# region GETs


@router.get("/")
def get_tareas_sin_pydantic() -> list[dict]:
    return tabla_tareas


@router.get("/pydantic", response_model=list[Tarea])
def get_tareas_con_pydantic() -> list[dict]:
    return tabla_tareas


@router.get("/{tarea_id}")
def get_tarea(tarea_id: int) -> dict:
    for tarea in tabla_tareas:
        if tarea["id"] == tarea_id:
            return tarea
    raise HTTPException(status_code=404,
                        detail=f"Tarea con id {tarea_id} no encontrada")


@router.get("/resumen/{tarea_id}")
def get_tarea_resumida_sin_pydantic(tarea_id: int) -> dict:
    for tarea in tabla_tareas:
        if tarea["id"] == tarea_id:
            return {"id": tarea['id'], "titulo": tarea["titulo"]}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.get("/pydantic/resumen/{tarea_id}", response_model=TareaResumida)
def get_tarea_resumida_con_pydantic(tarea_id: int) -> dict:
    for tarea in tabla_tareas:
        if tarea["id"] == tarea_id:
            print(tarea)
            return tarea
    raise HTTPException(status_code=404,
                        detail=f"Tarea con id {tarea_id} no encontrada")



@router.get("/pydantic/busqueda", response_model=list[Tarea])
def get_tareas_con_pydantic_y_filtro(
        estado: str
):
    return [tarea for tarea in tabla_tareas if tarea["estado"] == estado]

# endregion

# region POSTs
@router.post("/", response_model=Tarea, status_code=status.HTTP_201_CREATED)
def create_tarea(tarea: PayloadTarea):
    tarea_dict = tarea.model_dump()
    tarea_dict["id"] = len(tabla_tareas) + 1
    tabla_tareas.append(tarea_dict)
    return tarea_dict

# endregion

# region PUTs y PATCHs
@router.put("/{tarea_id}", response_model=Tarea)
def update_tarea(tarea_id: int, updated_tarea: PayloadTarea):
    for index, tarea in enumerate(tabla_tareas.copy()):
        if tarea["id"] == tarea_id:
            tabla_tareas[index] = {"id": tarea_id, **updated_tarea.model_dump()}
            return tabla_tareas[index]
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@router.patch("/{tarea_id}", response_model=Tarea)
def patch_tarea(tarea_id: int, updated_fields: PayloadTareaPatch):
    for tarea in tabla_tareas:
        if tarea["id"] == tarea_id:
            for key, value in updated_fields.model_dump().items():
                if value is not None:
                    tarea[key] = value
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
# endregion

# region DELETEs
@router.delete("/{tarea_id}")
def delete_tarea(tarea_id: int):
    for index, tarea in enumerate(tabla_tareas):
        if tarea["id"] == tarea_id:
            tabla_tareas.pop(index)
            return {"message": f"Tarea con id {tarea_id} eliminada"}
    raise HTTPException(status_code=404,
                        detail=f"Tarea con id {tarea_id} no encontrada")

# endregion


# region GETs con Path y Query
@router.get("/busqueda_compleja/{palabra_clave}", response_model=list[Tarea])
def get_tarea_busqueda_compleja(
        palabra_clave: Annotated[str, Path(description="Palabra clave en el título",
                                           pattern=r"^[^\-]+$")],
        orden: Annotated[str, Query(description="Ordenar por campo, asc o desc")] = "asc",
        ordenar_por: Annotated[str, Query(description="Campo por el que ordenar")] = "id",
        limite: Annotated[int, Query(description="Cantidad de tareas a devolver", ge=1, le=10)] = 5
):
    tareas_filtradas = [
        tarea for tarea in tabla_tareas
        if palabra_clave.lower() in tarea["titulo"].lower()]

    if not tareas_filtradas:
        return []

    # Ordenar las tareas filtradas
    reverse_order = orden == "desc"
    if ordenar_por in ["id", "estado", "prioridad"]:
        tareas_filtradas.sort(key=lambda x: x[ordenar_por], reverse=reverse_order)
    else:
        raise HTTPException(status_code=400,
                            detail="El parámetro 'ordenar_por' debe ser 'id', 'estado' o 'prioridad'")

    return tareas_filtradas[:limite]

# endregion


# region POST con File

@router.post("/upload-file/")
async def upload_file(file: UploadFile):
    UPLOAD_DIRECTORY = "./uploaded_files"

    # Crear el directorio si no existe
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "location": file_location}
# endregion


@router.get("/html/html_page")
def show_html():
    return HTMLResponse(content="<h1>Hola Mundo</h1>")


@router.get("/page/redirect")
def redirect_to_other_location():
    return RedirectResponse(url="https://www.linkedin.com/in/carlos-perez-molero/")