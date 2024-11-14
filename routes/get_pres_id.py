# get_pres_id.py

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from utils.mongo_conn import connect_to_mongo  # Updated import path for db_conn
from utils.logger import app_logger  # Import the logger instance from logger.py
from fastapi.encoders import jsonable_encoder

# Use the configured logger from utils
logger = app_logger

# Initialize the router
router = APIRouter()

# Establish a MongoDB connection
client, prescriptions_collection = connect_to_mongo()

# Endpoint to get a prescription by ID
@router.get(
    "/api/v1/prescriptions/{id}", 
    status_code=200, 
    summary="Get Prescription by ID", 
    description="Fetch a specific prescription using its unique MongoDB ID (id).", 
    responses={
        200: {"description": "Successfully retrieved the prescription."},
        400: {"description": "Invalid ID format."},
        404: {"description": "Prescription not found."},
        500: {"description": "Server error while retrieving the prescription."}
    }
)
def get_prescription_by_id(id: str):
    logger.info(f"Attempting to retrieve prescription with ID: {id}")
    try:
        # Convert the string ID to MongoDB ObjectId
        try:
            object_id = ObjectId(id)
            logger.info(f"Valid ObjectId for prescription: {id}")
        except:
            logger.warning(f"Invalid ID format for fetching prescription: {id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Find the prescription in MongoDB
        prescription = prescriptions_collection.find_one({"_id": object_id})

        if not prescription:
            logger.warning(f"Prescription with ID {id} not found.")
            raise HTTPException(status_code=404, detail="Prescription not found")

        # Remove nested `booking_id` from `corrected_data` if present
        corrected_data = prescription.get("corrected_data")
        if corrected_data:
            corrected_data = corrected_data.copy()
            corrected_data.pop("booking_id", None)  # Remove booking_id if it exists in corrected_data

        # Build the response in the specified order and structure
        response_data = {
            "_id": f'ObjectId("{str(prescription["_id"])}")'.replace('"', ''),  # Display as ObjectId format
            "extracted_data_AI": prescription.get("extracted_data_AI", {})
        }

        # Conditionally add `corrected_data` to maintain the original order
        if corrected_data:
            response_data["corrected_data"] = corrected_data

        # Continue with the rest of the structure in the specified order
        response_data.update({
            "booking_id": prescription.get("booking_id", "00395"),
            "created_by": prescription.get("created_by", {
                "userId": "XXXXXXXXXX",
                "CRNID": "XXXXXXXXX"
            }),
            "created_at": prescription.get("created_at", "YYYY-MM-DD-HH-MM-SS")  # Placeholder format if not set
        })

        logger.info(f"Successfully retrieved prescription with ID {id}.")
        return jsonable_encoder(response_data)

    except HTTPException as e:
        logger.error(f"HTTP error encountered while retrieving prescription with ID {id}: {e.detail}")
        raise e  # Raise any HTTP exceptions encountered

    except Exception as e:
        logger.error(f"Unexpected error retrieving prescription with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Unexpected server error.")
