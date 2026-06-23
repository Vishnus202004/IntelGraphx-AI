from fastapi import APIRouter, Depends
from app.api.endpoints import competitors, alerts, predictions, chat, reports, pipeline, auth
from app.api.deps import get_current_user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(competitors.router, prefix="/competitors", tags=["competitors"], dependencies=[Depends(get_current_user)])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"], dependencies=[Depends(get_current_user)])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"], dependencies=[Depends(get_current_user)])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"], dependencies=[Depends(get_current_user)])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"], dependencies=[Depends(get_current_user)])

