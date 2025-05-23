from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.salon_routes import router as salon_routes
from routes.materia_routes import router as materia_routes
from routes.docente_routes import router as docente_routes
from routes.curso_route import router as curso_routes
from routes.main_route import router as main_routes


app = FastAPI(
    title="API Horarios",
    description="API  para el taller de tercer Corte",
    version="0.1.0"
)

# Configure CORS to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routes
app.include_router(salon_routes, prefix="/salones", tags=["salones"])
app.include_router(materia_routes, prefix="/materias", tags=["materias"])
app.include_router(docente_routes, prefix="/docentes", tags=["docentes"])
app.include_router(curso_routes, prefix="/cursos", tags=["cursos"])
app.include_router(main_routes, prefix="/main", tags=["main"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)