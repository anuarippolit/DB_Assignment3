from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, caregivers, members, addresses, jobs, job_applications, appointments
from app.models import User, Caregiver, Member, Address, Job, JobApplication, Appointment
import os
import markdown

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Caregiver Management API",
    version="1.0.3",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

@app.get("/admin")
async def admin_panel():
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "admin.html")
    return FileResponse(template_path)

@app.get("/")
async def root():
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "admin.html")
    return FileResponse(template_path)

@app.get("/readme")
async def readme():
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        html_content = markdown.markdown(content)
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>README</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #555; margin-top: 30px; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>README not found</h1>", status_code=404)

app.include_router(users.router)
app.include_router(caregivers.router)
app.include_router(members.router)
app.include_router(addresses.router)
app.include_router(jobs.router)
app.include_router(job_applications.router)
app.include_router(appointments.router)