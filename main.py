from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# --- 1. SETUP DATABASE (SQLAlchemy) ---
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Bikin file database bernama "task.db" di folder yg sama
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Bikin mesin database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. DEFINISI TABEL (Model Database) ---
class TaskDB(Base):
    __tablename__ = "tasks" # Nama tabel di database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_completed = Column(Boolean, default=False)

# Bikin tabelnya otomatis kalau belum ada
Base.metadata.create_all(bind=engine)

# --- 3. DEFINISI DATA API (Pydantic) ---
# Ini buat validasi data yg keluar-masuk API
class TaskSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool

    class Config:
        # Biar Pydantic bisa baca data dari SQLAlchemy
        orm_mode = True 

class TaskCreate(BaseModel):
    title: str
    description: str
    is_completed: bool = False

# --- 4. SERVER SETUP ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: Buat koneksi ke DB tiap ada request, terus tutup lagi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. ENDPOINTS (CRUD dengan Database) ---

# GET: Ambil semua data dari tabel
@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()

# POST: Simpan ke tabel
@app.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Bikin objek database baru
    new_task = TaskDB(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed
    )
    db.add(new_task)  # Masukin ke antrian
    db.commit()       # Simpan permanen (Save)
    db.refresh(new_task) # Ambil ID yang baru digenerate
    return new_task

# DELETE: Hapus dari tabel
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # Cari task berdasarkan ID
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit() # Jangan lupa commit biar perubahannya disimpan
    return {"msg": "Berhasil dihapus dari Database"}