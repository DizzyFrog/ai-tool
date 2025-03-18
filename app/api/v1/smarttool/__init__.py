from fastapi import APIRouter

from .smarttool import router
smarttool_router = APIRouter()
smarttool_router.include_router(router,tags=["智能工具模块"])

__all__ = ["smarttool_router"]
