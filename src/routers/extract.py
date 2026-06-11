from ..schemas import ExtractRequest, ExtractResponse
from ..scripts import etl
from fastapi import APIRouter, HTTPException, status


router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("/", response_model=ExtractResponse, status_code=status.HTTP_201_CREATED)
def run_extract(request: ExtractRequest):
    try:
        orders_created = etl.insert_orders(request.amount)
        return ExtractResponse(
            message=f"Successfully extracted {orders_created} orders.",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
