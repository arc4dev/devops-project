from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Konfiguracja środowiskowa
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/todo_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model Zadania (Task)
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

# Automatyczne tworzenie tabel
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nowatorski Projekt DevOps - Smart To-Do")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "ToDo API is running", "database": "connected"}

# LISTA WSZYSTKICH ZADAŃ
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# DODAWANIE ZADANIA
@app.post("/tasks")
def create_task(title: str, description: str = None, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int, 
    title: str = None, 
    description: str = None, 
    is_completed: bool = None, 
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if is_completed is not None:
        task.is_completed = is_completed
        
    db.commit()
    db.refresh(task)
    return task

# USUWANIE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Zadanie {task_id} usunięte"}