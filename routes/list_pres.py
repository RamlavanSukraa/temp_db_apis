# list_pres.py

from fastapi import APIRouter, HTTPException, Query
from utils.mongo_conn import connect_to_mongo  # Updated import path for db_conn
from utils.logger import app_logger  # Import the logger instance from logger.py
from typing import Optional, List, Dict, Any

# Use the configured logger from utils
logger = app_logger

# Initialize the router
router = APIRouter()

# Establish a MongoDB connection
client, prescriptions_collection = connect_to_mongo()

# Helper function to reorder and format each record as per required format
def reorder_record(record: Dict[str, Any]) -> Dict[str, Any]:
    # Format _id as ObjectId and ensure fields are in the specified order
    formatted_record = {
        "_id": f'ObjectId("{str(record["_id"])}")'.replace('"', ''),  # Remove extra quotes to avoid slashes
        "extracted_data_AI": record.get("extracted_data_AI", {})
    }

    # Conditionally add `corrected_data` if it exists in the record
    if "corrected_data" in record and record["corrected_data"]:
        formatted_record["corrected_data"] = record["corrected_data"]

    # Add the remaining fields in the specified order
    formatted_record.update({
        "booking_id": record.get("booking_id", "00395"),  # Default booking_id if not present
        "created_by": record.get("created_by", {
            "userId": "XXXXXXXXXX",
            "CRNID": "XXXXXXXXX"
        }),
        "created_at": record.get("created_at", "YYYY-MM-DD-HH-MM-SS")  # Default format for created_at if not set
    })

    return formatted_record

# Endpoint to get all prescriptions with optional filters (pagination, date range, etc.)
@router.get("/api/v1/prescriptions", status_code=200, summary="Get All Prescriptions", description="Fetch all prescriptions with optional filters (pagination, date range, etc.).", responses={
    200: {"description": "Successfully retrieved the prescriptions."}
})
def get_all_prescriptions(
    page: int = 1, 
    limit: int = 20, 
    startDate: Optional[str] = None, 
    endDate: Optional[str] = None, 
    pt_name: Optional[str] = None, 
    ref_name: Optional[str] = None,
    booking_id: Optional[str] = None
):
    logger.info(f"Fetching all prescriptions with filters: page={page}, limit={limit}, startDate={startDate}, endDate={endDate}, pt_name={pt_name}, ref_name={ref_name}, booking_id={booking_id}")
    
    try:
        # Prepare query filters based on optional parameters
        query_filters = {}
        if startDate and endDate:
            query_filters["extracted_data_AI.doc_date"] = {"$gte": startDate, "$lte": endDate}
        if pt_name:
            query_filters["extracted_data_AI.pt_name"] = pt_name
        if ref_name:
            query_filters["extracted_data_AI.ref_name"] = ref_name
        if booking_id:
            query_filters["booking_id"] = booking_id  # Add filter for booking_id

        # Pagination logic: skip (page - 1) * limit, and limit the results
        total_prescriptions = prescriptions_collection.count_documents(query_filters)
        prescriptions = list(prescriptions_collection.find(query_filters).skip((page - 1) * limit).limit(limit))

        # Reformat the results for the response with exact field ordering
        response_data = {
            "total": total_prescriptions,
            "prescriptions": [reorder_record(prescription) for prescription in prescriptions]
        }

        logger.info(f"Successfully retrieved {len(prescriptions)} prescriptions for page {page}.")
        return response_data

    except Exception as e:
        logger.error(f"Error retrieving prescriptions: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving prescriptions.")
