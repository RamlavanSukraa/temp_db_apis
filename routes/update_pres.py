# update_pres.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from utils.mongo_conn import connect_to_mongo  # Updated import path for db_conn
from utils.logger import app_logger  # Import the logger instance from logger.py
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

# Use the configured logger from utils
logger = app_logger

# Initialize the router
router = APIRouter()

# Establish a MongoDB connection
client, prescriptions_collection = connect_to_mongo()

# Models for PrescribedTest and Data Fields
class PrescribedTest(BaseModel):
    extracted_test_name: str
    mapped_test_name: str
    mapped_test_code: str

class ExtractedDataAI(BaseModel):
    doc_date: str
    pt_address: str
    pt_age: str
    pt_age_period: str
    pt_contact: str
    pt_name: str
    pt_sex: str
    pt_title: str
    ref_name: str
    ref_type: str
    mapped_ref_name: str
    mapped_ref_type: str
    mapped_ref_code: str
    remark: Optional[str] = None
    uhid_id: str
    prescribed_tests: List[PrescribedTest]

class CorrectedData(BaseModel):
    doc_date: str
    pt_address: str
    pt_age: str
    pt_age_period: str
    pt_contact: str
    pt_name: str
    pt_sex: str
    pt_title: str
    ref_name: str
    ref_type: str
    mapped_ref_name: str
    mapped_ref_type: str
    mapped_ref_code: str
    remark: Optional[str] = None
    uhid_id: str
    prescribed_tests: List[PrescribedTest]

class CreatedBy(BaseModel):
    userId: str
    CRNID: str

class PrescriptionUpdateData(BaseModel):
    extracted_data_AI: Optional[ExtractedDataAI] = None
    corrected_data: Optional[CorrectedData] = None
    booking_id: Optional[str] = None

@router.put("/api/v1/prescriptions/{id}", status_code=200, summary="Update a Prescription Entry", 
            description="Update an existing prescription entry by its ID. Allows for partial updates of the extracted_data_AI and corrected_data fields.",
            responses={
                200: {"description": "Successfully updated the prescription."},
                400: {"description": "Invalid ID format or no valid fields provided for update."},
                404: {"description": "Prescription not found."}
            })
def update_prescription_entry(id: str, updated_data: PrescriptionUpdateData):
    logger.info(f"Attempting to update prescription with ID: {id}")
    
    try:
        try:
            object_id = ObjectId(id)
            logger.info(f"Valid ObjectId for prescription: {id}")
        except:
            logger.warning(f"Invalid ID format for updating prescription: {id}")
            raise HTTPException(status_code=400, detail="Invalid ID format")

        update_dict = updated_data.dict(exclude_unset=True)
        if not update_dict:
            logger.warning("No valid fields provided for updating prescription.")
            raise HTTPException(status_code=400, detail="No valid fields provided for update")

        result = prescriptions_collection.update_one({"_id": object_id}, {"$set": update_dict})

        if result.matched_count == 0:
            logger.warning(f"Prescription with ID {id} not found for update.")
            raise HTTPException(status_code=404, detail="Prescription not found")

        updated_record = prescriptions_collection.find_one({"_id": object_id})

        response_data = { 
            "_id": f'ObjectId("{str(updated_record["_id"])}")'.replace('"', ''),
            "extracted_data_AI": updated_record.get("extracted_data_AI"),
            "corrected_data": updated_record.get("corrected_data", updated_record.get("extracted_data_AI")),
            "created_by": updated_record.get("created_by"),
            "created_at": updated_record.get("created_at"),
            "booking_id": updated_record.get("booking_id")
        }

        logger.info(f"Updated prescription with ID {id}.")  

        if '_id' in response_data:
            response_data['_id'] = str(response_data['_id']).replace("ObjectId(",'').replace(")",'').strip()

        return jsonable_encoder(response_data)

    except HTTPException as e:
        logger.error(f"HTTP error encountered while updating prescri   ption with ID {id}: {e}")
        raise e

    except Exception as e:
        logger.error(f"Error updating prescription with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating prescription.")

