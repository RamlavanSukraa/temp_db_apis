# insights_pres.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from utils.mongo_conn import connect_to_mongo  # Updated import path for db_conn
from utils.logger import app_logger  # Import the logger instance from logger.py
from fastapi.encoders import jsonable_encoder
from datetime import date

# Use the configured logger from utils
logger = app_logger

# Initialize the router
router = APIRouter()

# Establish a MongoDB connection
client, prescriptions_collection = connect_to_mongo()

# Define the request body model
class AgeGroup(BaseModel):
    min: int
    max: int

class InsightsFilter(BaseModel):
    startDate: date
    endDate: date
    ref_name: Optional[str] = None
    pt_name: Optional[str] = None
    mapped_test_names: Optional[List[str]] = None
    age_group: Optional[AgeGroup] = None
    sex: Optional[str] = None

# Endpoint to get prescription insights based on specified criteria
@router.post("/api/v1/prescriptions/insights", status_code=200, summary="Get Prescription Insights", description="""Retrieve insights based on specified criteria such as date range, referring lab, patient demographics, and other filters. 
          This API can also be used to retrieve prescriptions based on specific criteria like referrer, test name, or patient ID.""")
def get_prescription_insights(insights_filter: InsightsFilter):
    logger.info(f"Fetching prescription insights with filters: {insights_filter}")
    
    try:
        # Prepare query filters based on the request body
        query_filters = {}

        # Date range filter
        if insights_filter.startDate and insights_filter.endDate:
            query_filters["extracted_data_AI.doc_date"] = {
                "$gte": insights_filter.startDate.isoformat(),
                "$lte": insights_filter.endDate.isoformat()
            }

        # Referrer name filter
        if insights_filter.ref_name:
            query_filters["extracted_data_AI.ref_name"] = insights_filter.ref_name

        # Patient name filter
        if insights_filter.pt_name:
            query_filters["extracted_data_AI.pt_name"] = insights_filter.pt_name

        # Test names filter
        if insights_filter.mapped_test_names:
            query_filters["extracted_data_AI.prescribed_tests.mapped_test_name"] = {
                "$in": insights_filter.mapped_test_names
            }

        # Age group filter
        if insights_filter.age_group:
            query_filters["extracted_data_AI.pt_age"] = {
                "$gte": str(insights_filter.age_group.min),
                "$lte": str(insights_filter.age_group.max)
            }

        # Sex filter
        if insights_filter.sex:
            query_filters["extracted_data_AI.pt_sex"] = insights_filter.sex

        # Fetch the filtered prescriptions from MongoDB
        prescriptions = list(prescriptions_collection.find(query_filters))
        total_prescriptions = len(prescriptions)

        # Aggregate common tests
        test_counts = {}
        for prescription in prescriptions:
            for test in prescription.get("extracted_data_AI", {}).get("prescribed_tests", []):
                test_name = test.get("mapped_test_name")
                if test_name:
                    test_counts[test_name] = test_counts.get(test_name, 0) + 1

        # Group prescriptions by age range
        prescriptions_by_age_group = {"30-40": 0, "41-50": 0, "51-60": 0, "60+": 0}
        for prescription in prescriptions:
            pt_age = int(prescription.get("extracted_data_AI", {}).get("pt_age", 0))
            if 30 <= pt_age <= 40:
                prescriptions_by_age_group["30-40"] += 1
            elif 41 <= pt_age <= 50:
                prescriptions_by_age_group["41-50"] += 1
            elif 51 <= pt_age <= 60:
                prescriptions_by_age_group["51-60"] += 1
            else:
                prescriptions_by_age_group["60+"] += 1

        # Prepare the response
        response_data = {
            "total_prescriptions": total_prescriptions,
            "total_tests_prescribed": sum(test_counts.values()),
            "common_tests": [{"mapped_test_name": test, "count": count} for test, count in test_counts.items()],
            "prescriptions_by_age_group": prescriptions_by_age_group
        }

        logger.info(f"Successfully generated insights for {total_prescriptions} prescriptions.")
        return jsonable_encoder(response_data)

    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Error generating insights.")
