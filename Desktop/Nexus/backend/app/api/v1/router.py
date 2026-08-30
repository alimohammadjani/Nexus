"""API v1 router composition."""

from fastapi import APIRouter

from app.api.v1 import auth, jobs, learning, market, payments, roadmap, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(jobs.router)
api_router.include_router(learning.router)
api_router.include_router(market.router)
api_router.include_router(payments.router)
api_router.include_router(roadmap.router)
