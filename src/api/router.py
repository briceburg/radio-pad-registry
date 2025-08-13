from fastapi import APIRouter

from api.routes import accounts, players
from api.routes.presets import account_presets, global_presets

router = APIRouter()

router.include_router(accounts.router, tags=["accounts"])
router.include_router(players.router, tags=["players"])
router.include_router(account_presets, tags=["station presets"])
router.include_router(global_presets, tags=["station presets"])
