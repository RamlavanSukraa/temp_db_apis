# Prescription Data Extractor API Documentation

This API facilitates the extraction, management, and insights generation of prescription data from images, specifically designed for lab clients.

## Table of Contents
1. [Create a Prescription Entry](#1-create-a-prescription-entry)
2. [Update a Prescription Entry](#2-update-a-prescription-entry)
3. [Get Prescription by ID](#3-get-prescription-by-id)
4. [Delete a Prescription](#4-delete-a-prescription)
5. [Get All Prescriptions](#5-get-all-prescriptions)
6. [Get Prescription Insights](#6-get-prescription-insights)
7. [Additional Notes](#additional-notes)

---

## 1. Create a Prescription Entry
- **Method**: `POST`
- **Endpoint**: `/api/v1/prescriptions`
- **Description**: Create a new prescription entry with extracted data from the prescription image.

### Request Body:
```json
{
  "extracted_data_AI": {
    "doc_date": "2024-09-27",
    "pt_address": "Adyar, Chennai",
    "pt_age": "50",
    "pt_age_period": "Y",
    "pt_contact": "7676543345",
    "pt_name": "Venkataramani",
    "pt_sex": "M",
    "pt_title": "Mr",
    "ref_name": "VRR Diagnostics",
    "ref_type": "L",
    "remark": "Dr Vimal",
    "uhid_id": "01-013549-00",
    "prescribed_tests": [
      {
        "extracted_test_name": "SOME NAME",
        "mapped_test_name": "SOME NAME",
        "mapped_test_code": "00013"
      }
    ]
  },
  "created_by": {
    "userId": "XXXXXXXXXX",
    "CRNID": "XXXXXXXXX"
  },
  "created_at": "YYYY-MM-DD-HH-MM-SS"
}
```

### Response:
- **201 Created**: When the record is successfully inserted.
- **400 Bad Request**: If there is any missing/invalid data.

---

## 2. Update a Prescription Entry
- **Method**: `PUT`
- **Endpoint**: `/api/v1/prescriptions/{id}`
- **Description**: Update an existing prescription entry by its ID. Allows for partial updates of the `extracted_data_AI` and `corrected_data` fields.

### Request Body:
```json
{
  "extracted_data_AI": {
    "doc_date": "2024-09-27",                     
    "pt_address": "New Address, Chennai",         
    "pt_age": "51",                               
    "pt_age_period": "Y",                          
    "pt_contact": "1234567890",                   
    "pt_name": "New Name",                         
    "pt_sex": "F",                                 
    "pt_title": "Ms",                              
    "ref_name": "New Referring Lab",              
    "ref_type": "L",                               
    "remark": "New Remarks",                       
    "uhid_id": "01-013549-01",                     
    "prescribed_tests": [                          
      {
        "extracted_test_name": "NEW TEST NAME",
        "mapped_test_name": "NEW TEST NAME",
        "mapped_test_code": "00015"
      }
    ]
  },
  "corrected_data": {                             
    "doc_date": "2024-09-27",
    "pt_address": "Adyar, Chennai",
    "pt_age": "51",
    "pt_age_period": "Y",
    "pt_contact": "1234567890",
    "pt_name": "Venkataramani",
    "pt_sex": "M",
    "pt_title": "Mr",
    "ref_name": "VRR Diagnostics",
    "ref_type": "L",
    "remark": "Dr Vimal",
    "uhid_id": "01-013549-01",
    "prescribed_tests": [
      {
        "extracted_test_name": "SOME NAME",
        "mapped_test_name": "SOME NAME",
        "mapped_test_code": "00013"
      }
    ]
  }
}
```

### Response Codes:
- **200 OK**: When the update is successful.
- **404 Not Found**: If the prescription with the given ID does not exist.
- **400 Bad Request**: If the request body contains invalid or missing parameters.

---

## 3. Get Prescription by ID
- **Method**: `GET`
- **Endpoint**: `/api/v1/prescriptions/{id}`
- **Description**: Fetch a specific prescription using its unique MongoDB ID (`id`).

### Response:
```json
{
  "_id": "prescription_object_id",
  "extracted_data_AI": { ... },
  "corrected_data": { ... },
  "created_by": { ... },
  "created_at": "YYYY-MM-DD-HH-MM-SS"
}
```

### Response Codes:
- **200 OK**: When the prescription is found.
- **404 Not Found**: If the prescription with the given ID does not exist.

---

## 4. Delete a Prescription
- **Method**: `DELETE`
- **Endpoint**: `/api/v1/prescriptions/{id}`
- **Description**: Delete a specific prescription entry by its ID.

### Response Codes:
- **200 OK**: When the deletion is successful.
- **404 Not Found**: If the record with the given ID does not exist.

---

## 5. Get All Prescriptions
- **Method**: `GET`
- **Endpoint**: `/api/v1/prescriptions`
- **Description**: Fetch all prescriptions with optional filters (pagination, date range, etc.).

### Query Parameters:
- `page`: Page number for pagination.
- `limit`: Number of items per page.
- `startDate`: Filter by starting date (`doc_date`).
- `endDate`: Filter by ending date (`doc_date`).
- `pt_name`: Filter by patient name.
- `ref_name`: Filter by referring lab name.

### Example Request:  
`/api/v1/prescriptions?page=1&limit=20&startDate=2024-01-01&endDate=2024-09-30`

### Response:
```json
{
  "total": 100,
  "prescriptions": [
    {
      "_id": "prescription_object_id",
      "extracted_data_AI": { ... },
      "corrected_data": { ... },
      ...
    },
    ...
  ]
}
```

---

## 6. Get Prescription Insights
- **Method**: `POST`
- **Endpoint**: `/api/v1/prescriptions/insights`
- **Description**: Retrieve insights based on specified criteria such as date range, referring lab, patient demographics, and other filters. This API can also be used to retrieve prescriptions based on specific criteria like referrer, test name, or patient ID.

### Request Body:
```json
{
  "startDate": "2024-01-01",                     
  "endDate": "2024-09-30",                       
  "ref_name": "VRR Diagnostics",                 
  "pt_name": "Venkataramani",                    
  "mapped_test_names": ["Blood Test", "X-Ray"],  
  "age_group": {
    "min": 30,                                   
    "max": 60                                    
  },
  "sex": "M"                                     
}
```

### Response:
```json
{
  "total_prescriptions": 100,
  "total_tests_prescribed": 250,
  "common_tests": [
    {
      "mapped_test_name": "Blood Test",
      "count": 80
    },
    {
      "mapped_test_name": "X-Ray",
      "count": 50
    }
  ],
  "prescriptions_by_age_group": {
    "30-40": 20,
    "41-50": 30,
    "51-60": 25,
    "60+": 25
  }
}
```

### Response Codes:
- **200 OK**: When the insights are successfully generated.
- **400 Bad Request**: If the request body contains invalid or missing parameters.

---

## Additional Notes

- **Authentication & Authorization**: Implement authentication tokens (e.g., JWT) for secure access to the API, especially for sensitive data.
- **Pagination**: Use query parameters like `page` and `limit` to paginate results for large datasets.
- **Error Handling**: Each API should return appropriate error messages such as `404 Not Found`, `400 Bad Request`, etc.

---