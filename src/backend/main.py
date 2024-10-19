from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .database import engine
from .models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud  # Asegúrate de importar correctamente el archivo crud


app = FastAPI()

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error al crear la base de datos: {e}")


# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir peticiones desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

@app.get("/")
def read_root():
    return {"message": "Hello, Fullstack!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_user(db=db, name=name, email=email)
