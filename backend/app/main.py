import os
from datetime import datetime, timezone
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    ClaimCreate,
    ClaimInput,
    ClaimRecord,
    Passport,
    Project,
    ProjectCreate,
    RunHandle,
    RunStatus,
)
from .service import PASSPORTS, RUNS, verify


app = FastAPI(title="ReproForge Sentinel API", version="0.2.0")
origins = [value.strip() for value in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])
projects: dict[str, Project] = {}
claims: dict[str, ClaimRecord] = {}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "reproforge-sentinel", "version": app.version}


@app.post("/projects", response_model=Project, status_code=201)
def create_project(payload: ProjectCreate) -> Project:
    project = Project(
        **payload.model_dump(),
        id=f"proj_{uuid.uuid4().hex[:10]}",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    projects[project.id] = project
    return project


@app.post("/claims", response_model=ClaimRecord, status_code=201)
def create_claim(payload: ClaimCreate) -> ClaimRecord:
    if payload.project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    claim = ClaimRecord(
        **payload.model_dump(),
        id=f"claim_{uuid.uuid4().hex[:10]}",
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    claims[claim.id] = claim
    return claim


@app.post("/verify", response_model=RunHandle)
async def start_verification(claim: ClaimInput) -> RunHandle:
    passport = await verify(claim)
    return RunHandle(run_id=passport.run_id, status="complete")


@app.get("/runs/{run_id}", response_model=RunStatus)
def get_run(run_id: str) -> RunStatus:
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="Run not found")
    return RUNS[run_id]


@app.get("/passport/{run_id}", response_model=Passport)
def get_passport(run_id: str) -> Passport:
    if run_id not in PASSPORTS:
        raise HTTPException(status_code=404, detail="Passport not found")
    return PASSPORTS[run_id]
