from fastapi import FastAPI
from app import auth
from app import auth, files_route

app = FastAPI(title="Secure File Sharing System")

# Include routers
app.include_router(auth.router)
app.include_router(files_route.router)

@app.get("/")
def root():
    return {"message": "Welcome to the secure file sharing system"}


