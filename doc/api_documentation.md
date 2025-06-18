# API Documentation - Hearline Webapp

## Overview

The Hearline Webapp provides a comprehensive RESTful API for healthcare management with AI-powered ECG analysis. This document details all available endpoints, request/response formats, and integration guidelines.

## Base URL
```
https://your-domain.com/api
```

## Authentication

All API requests require authentication using session-based authentication or API keys.

### Session Authentication
```http
POST /login
Content-Type: application/json

{
  "username": "doctor@example.com",
  "password": "securepassword"
}
```

### API Key Authentication
```http
GET /api/patients
Authorization: Bearer your-api-key-here
```

## Core Endpoints

### 1. Patient Management

#### Get All Patients
```http
GET /api/patients
```

**Parameters:**
- `page` (optional): Page number for pagination
- `per_page` (optional): Items per page (default: 10)
- `search` (optional): Search term for patient names

**Response:**
```json
{
  "patients": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1980-01-01",
      "gender": "Male",
      "phone": "+213555123456",
      "email": "john.doe@example.com",
      "medical_history": "Hypertension",
      "created_at": "2024-01-01T10:00:00Z",
      "visits_count": 5,
      "last_visit": "2024-06-01T14:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

#### Get Patient by ID
```http
GET /api/patients/{patient_id}
```

**Response:**
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1980-01-01",
  "gender": "Male",
  "address": "123 Main St, Algiers",
  "phone": "+213555123456",
  "email": "john.doe@example.com",
  "medical_history": "Hypertension, controlled with medication",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-06-01T14:30:00Z",
  "visits": [
    {
      "id": 10,
      "visit_date": "2024-06-01T14:30:00Z",
      "diagnosis": "Routine checkup",
      "doctor_name": "Dr. Smith"
    }
  ]
}
```

#### Create New Patient
```http
POST /api/patients
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "date_of_birth": "1985-03-15",
  "gender": "Female",
  "address": "456 Oak Ave, Oran",
  "phone": "+213555654321",
  "email": "jane.smith@example.com",
  "medical_history": "No known allergies"
}
```

#### Update Patient
```http
PUT /api/patients/{patient_id}
Content-Type: application/json

{
  "phone": "+213555999888",
  "medical_history": "Hypertension, diabetes type 2"
}
```

#### Delete Patient
```http
DELETE /api/patients/{patient_id}
```

### 2. Visit Management

#### Get Patient Visits
```http
GET /api/patients/{patient_id}/visits
```

**Response:**
```json
{
  "visits": [
    {
      "id": 10,
      "patient_id": 1,
      "doctor_id": 2,
      "visit_date": "2024-06-01T14:30:00Z",
      "diagnosis": "Atrial fibrillation detected",
      "follow_up_date": "2024-07-01T14:30:00Z",
      "payment_total": 150.00,
      "payment_status": "paid",
      "ecg_analysis": {
        "primary_diagnosis": "AF",
        "confidence": 0.89,
        "probabilities": {
          "SNR": 0.05,
          "AF": 0.89,
          "IAVB": 0.02,
          "LBBB": 0.01,
          "RBBB": 0.01,
          "PAC": 0.01,
          "PVC": 0.01,
          "STD": 0.00,
          "STE": 0.00
        }
      },
      "prescriptions": [
        {
          "medication": "Warfarin 5mg",
          "dosage": "1 tablet daily",
          "quantity": 30
        }
      ]
    }
  ]
}
```

#### Create New Visit
```http
POST /api/visits
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 2,
  "visit_date": "2024-06-15T10:00:00Z",
  "diagnosis": "Routine follow-up",
  "prescriptions": [
    {
      "medicament_num_enr": "12345",
      "dosage_instructions": "Take with food, twice daily",
      "quantity": 60
    }
  ]
}
```

### 3. ECG Analysis

#### Analyze ECG Files
```http
POST /api/ecg/analyze
Content-Type: multipart/form-data

Form Data:
- mat_file: [ECG .mat file]
- hea_file: [ECG .hea file]
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "probabilities": {
      "SNR": 0.05,
      "AF": 0.89,
      "IAVB": 0.02,
      "LBBB": 0.01,
      "RBBB": 0.01,
      "PAC": 0.01,
      "PVC": 0.01,
      "STD": 0.00,
      "STE": 0.00
    },
    "primary_diagnosis": {
      "abbreviation": "AF",
      "name": "Atrial Fibrillation",
      "probability": 0.89
    },
    "summary": "Primary finding: Atrial Fibrillation (89% confidence)",
    "analysis_time": "2024-06-15T10:05:32Z"
  }
}
```

#### Get ECG History
```http
GET /api/ecg/history
```

**Parameters:**
- `patient_id` (optional): Filter by specific patient
- `from_date` (optional): Start date filter (YYYY-MM-DD)
- `to_date` (optional): End date filter (YYYY-MM-DD)
- `condition` (optional): Filter by detected condition

**Response:**
```json
{
  "ecg_records": [
    {
      "visit_id": 10,
      "patient_name": "John Doe",
      "patient_age": 44,
      "visit_date": "2024-06-01T14:30:00Z",
      "primary_diagnosis": "Atrial Fibrillation",
      "confidence": 0.89,
      "all_probabilities": {
        "SNR": 0.05,
        "AF": 0.89,
        "IAVB": 0.02
      },
      "files_available": ["MAT", "HEA"]
    }
  ],
  "statistics": {
    "total_ecgs": 150,
    "normal_rhythm": 120,
    "abnormal_findings": 30,
    "high_confidence": 140
  }
}
```

### 4. Medication Management

#### Search Medications
```http
GET /api/medications/search?q=aspirin
```

**Response:**
```json
{
  "medicaments": [
    {
      "id": "12345",
      "text": "ASPEGIC 100MG - ASPIRINE - 100mg",
      "nom_com": "ASPEGIC",
      "nom_dci": "ASPIRINE",
      "dosage": "100mg",
      "unite": "mg"
    }
  ],
  "pagination": {
    "more": false
  }
}
```

#### Get Medication Details
```http
GET /api/medications/{medication_id}
```

**Response:**
```json
{
  "num_enr": "12345",
  "nom_com": "ASPEGIC",
  "nom_dci": "ASPIRINE",
  "dosage": "100",
  "unite": "mg",
  "forme": "tablets",
  "presentation": "Box of 30 tablets",
  "laboratory": "Pharmaceutical Company Name"
}
```

### 5. Appointment Management

#### Get Appointments
```http
GET /api/appointments
```

**Parameters:**
- `date` (optional): Filter by specific date (YYYY-MM-DD)
- `doctor_id` (optional): Filter by doctor
- `status` (optional): Filter by status (scheduled, completed, canceled)

**Response:**
```json
{
  "appointments": [
    {
      "id": 25,
      "patient_name": "John Doe",
      "doctor_name": "Dr. Smith",
      "date": "2024-06-15T10:00:00Z",
      "reason": "Follow-up consultation",
      "status": "scheduled",
      "duration_minutes": 30
    }
  ]
}
```

#### Create Appointment
```http
POST /api/appointments
Content-Type: application/json

{
  "patient_id": 1,
  "doctor_id": 2,
  "date": "2024-06-20T14:00:00Z",
  "reason": "Initial consultation",
  "duration_minutes": 45
}
```

### 6. User Management

#### Get Current User
```http
GET /api/user/profile
```

**Response:**
```json
{
  "id": 1,
  "username": "doctor.smith",
  "email": "dr.smith@clinic.com",
  "role": "doctor",
  "first_name": "John",
  "last_name": "Smith",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-06-15T08:30:00Z",
  "permissions": [
    "view_patients",
    "create_visits",
    "analyze_ecg",
    "prescribe_medications"
  ]
}
```

#### Update User Profile
```http
PUT /api/user/profile
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@newclinic.com"
}
```

## Error Handling

### Standard Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  },
  "timestamp": "2024-06-15T10:00:00Z"
}
```

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `AUTHENTICATION_FAILED` | Invalid credentials |
| `AUTHORIZATION_DENIED` | Insufficient permissions |
| `VALIDATION_ERROR` | Input validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist |
| `ECG_ANALYSIS_FAILED` | ECG processing error |
| `FILE_UPLOAD_ERROR` | File upload failed |
| `DATABASE_ERROR` | Database operation failed |

## Rate Limiting

API requests are limited to:
- **Authenticated users**: 1000 requests per hour
- **ECG analysis**: 100 analyses per hour
- **File uploads**: 50 uploads per hour

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1624387200
```

## Webhooks

Configure webhooks to receive real-time notifications for important events:

### Available Events
- `patient.created`
- `visit.completed`
- `ecg.analyzed`
- `appointment.scheduled`
- `prescription.created`

### Webhook Configuration
```http
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-system.com/webhook",
  "events": ["ecg.analyzed", "visit.completed"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload Example
```json
{
  "event": "ecg.analyzed",
  "timestamp": "2024-06-15T10:05:32Z",
  "data": {
    "visit_id": 10,
    "patient_id": 1,
    "analysis": {
      "primary_diagnosis": "AF",
      "confidence": 0.89
    }
  },
  "signature": "sha256=abc123..."
}
```

## SDK and Libraries

### Python SDK
```python
from hearline_api import HearlineClient

client = HearlineClient(api_key="your-api-key")

# Create patient
patient = client.patients.create({
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-01"
})

# Analyze ECG
with open("ecg_file.mat", "rb") as mat_file, \
     open("ecg_file.hea", "rb") as hea_file:
    analysis = client.ecg.analyze(mat_file, hea_file)
    print(f"Primary diagnosis: {analysis.primary_diagnosis}")
```

### JavaScript SDK
```javascript
import { HearlineAPI } from 'hearline-js-sdk';

const client = new HearlineAPI({
  apiKey: 'your-api-key',
  baseURL: 'https://api.hearline.com'
});

// Get patients
const patients = await client.patients.list({
  page: 1,
  search: 'john'
});

// Create appointment
const appointment = await client.appointments.create({
  patientId: 1,
  doctorId: 2,
  date: '2024-06-20T14:00:00Z',
  reason: 'Follow-up'
});
```

## Testing

### Test Environment
```
Base URL: https://api-test.hearline.com
```

### Test Credentials
```
Username: test.doctor@hearline.com
Password: TestPassword123!
API Key: test_sk_1234567890abcdef
```

### Sample Test Data
Test patient IDs: 1, 2, 3
Test ECG files available in test environment

## Support

### Technical Support
- **Email**: api-support@hearline.com
- **Documentation**: https://docs.hearline.com
- **Status Page**: https://status.hearline.com

### Community
- **GitHub**: https://github.com/hearline/api-examples
- **Discord**: https://discord.gg/hearline-dev
- **Stack Overflow**: Tag `hearline-api`

---

**Last Updated**: June 2025
**API Version**: v2.0
**Status**: Production Ready
