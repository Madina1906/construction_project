# app/__init__.py

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")