# delete_pres.py

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from utils.mongo_conn import connect_to_mongo  # Updated import path for db_conn
from utils.logger import app_logger  # Import the logger instance from logger.py

# Use the configured logger from utils
logger = app_logger

# Initialize the router
router = APIRouter()

# Establish a MongoDB connection
client, prescriptions_collection = connect_to_mongo()

# Endpoint to delete a prescription by ID
@router.delete("/api/v1/prescriptions/{id}", status_code=200, summary="Delete a Prescription", description="Delete a specific prescription entry by its ID.", responses={
    200: {"description": "Successfully deleted the prescription."},
    404: {"description": "Prescription not found."}
})
def delete_prescription_by_id(id: str):
    logger.info(f"Attempting to delete prescription with ID: {id}")
    try:
        # Convert the string ID to MongoDB ObjectId
        try:
            object_id = ObjectId(id)
            logger.info(f"Valid ObjectId for prescription: {id}")
        except:
            logger.warning(f"Invalid ID format for deleting prescription: {id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Delete the prescription from MongoDB
        result = prescriptions_collection.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            logger.warning(f"Prescription with ID {id} not found for deletion.")
            raise HTTPException(status_code=404, detail="Prescription not found")

        logger.info(f"Successfully deleted prescription with ID {id}.")
        return {"message": "Prescription deleted successfully"}

    except HTTPException as e:
        logger.error(f"HTTP error encountered while deleting prescription with ID {id}: {e}")
        raise e  # Raise any HTTP exceptions encountered

    except Exception as e:
        logger.error(f"Error deleting prescription with ID {id}: {e}")  # Log error
        raise HTTPException(status_code=500, detail="Error deleting prescription.")
