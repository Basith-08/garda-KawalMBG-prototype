from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.admin import get_admin_overview, router as admin_router, update_admin_user
from api.auth import auth_session, login, router as auth_router
from api.data import get_data, router as data_router, save_data
from api.deps import get_current_user, require_role
from api.distributions import (
    get_distribution_receipt,
    router as distributions_router,
    verify_distribution_receipt,
)
from api.public import get_public_data, health_check, router as public_router
from api.regulator import get_regulator_overview, router as regulator_router
from constants import DISTRIBUTION_FIELDS
from migrations import run_migrations
from schemas.requests import AdminUserUpdateRequest, LoginRequest, ReceiptVerificationRequest
from seed import seed_database
from services.admin import build_admin_overview
from services.serialization import build_vendor_trust_profile
from settings import get_settings, validate_runtime_settings


settings = get_settings()
validate_runtime_settings()

app = FastAPI(title="KawalMBG API with Local Supabase")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def bootstrap_data():
    run_migrations()
    if settings.auto_seed_on_startup:
        seed_database(only_if_empty=True)


app.include_router(public_router)
app.include_router(auth_router)
app.include_router(distributions_router)
app.include_router(data_router)
app.include_router(regulator_router)
app.include_router(admin_router)
