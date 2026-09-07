from fastapi import APIRouter

router = APIRouter(prefix="/finlit", tags=["finlit"])


@router.get("/status")
def feature_status() -> dict:
    return {"feature": "finlit", "status": "planned"}
