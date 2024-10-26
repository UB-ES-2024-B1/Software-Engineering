from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .db.database import engine, Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .db.database import SessionLocal
from . import crud  # Asegúrate de importar correctamente el archivo crud
from .api.routes import user_routes
from .api.routes import login_routes
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    user_routes.init_db()
    print("Database initialized")
    yield
    print("Shutting down")
    app.state.db.close()

app = FastAPI(lifespan=lifespan)


'''try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error al crear la base de datos: {e}")
'''

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir peticiones desde este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FilmHub!"}

'''@app.get("/items/{item_id}")
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
'''

# Import the routes from the other files
app.include_router(user_routes.router, prefix="/users", tags=["users"])

app.include_router(login_routes.router, prefix="/login",tags=["login"])


@app.on_event("startup")
def startup_event():
    user_routes.init_db()
    print("Database initialized")
