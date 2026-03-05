from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine, Base
from app.routers import dashboard, auth
from app.routers import tasks

# Import models so tables are created
from app.models import user, project, task, assignment, status_history
from app.routers import projects

app = FastAPI(title="Qurilish loyihasi boshqaruvi")

# Create tables
Base.metadata.create_all(bind=engine)

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(tasks.router)
app.include_router(projects.router)

# ROOT → automatic redirect
@app.get("/")
async def root(request: Request):
    token = request.cookies.get("session_token")

    # If not logged in → login page
    if not token:
        return RedirectResponse(url="/auth/login", status_code=303)

    # If logged in → dashboard
    return RedirectResponse(url="/dashboard", status_code=303)


