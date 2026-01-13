from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Tambah ini
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- 2. Tambah blok ini (Setting CORS) ---
# Ini biar React (port 5173) boleh ngobrol sama Python (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Buka untuk semua alamat (aman buat belajar)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    is_completed: bool = False

fake_db = [
    {"id": 1, "title": "Belajar FastAPI", "description": "Bikin API pertama", "is_completed": False}
]

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return fake_db

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in fake_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Tugas tidak ditemukan")
    return task

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    new_id = fake_db[-1]["id"] + 1 if fake_db else 1
    new_task = task.dict()
    new_task["id"] = new_id
    fake_db.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global fake_db
    fake_db = [t for t in fake_db if t["id"] != task_id]
    return {"msg": "Tugas berhasil dihapus"}