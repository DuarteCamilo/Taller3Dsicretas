from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import message_routes

app = FastAPI(
    title="Simple API",
    description="API sencilla para el taller",
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
app.include_router(message_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)