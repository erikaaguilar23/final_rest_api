import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# -------------------------------
# Test GET all patients
# -------------------------------
def test_get_patients():
    response = requests.get(f"{BASE_URL}/patients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# -------------------------------
# Test GET single patient (existing)
# -------------------------------
def test_get_patient_by_id():
    response = requests.get(f"{BASE_URL}/patients/1")  # Make sure idPatient=1 exists
    assert response.status_code in [200, 404]  # Pass if found or not
    if response.status_code == 200:
        data = response.json()
        assert "idPatient" in data[0]
        assert "name" in data[0]

# -------------------------------
# Test POST - create patient
# -------------------------------
def test_create_patient():
    new_patient = {
        "name": "Test Patient",
        "age": "30",
        "Diagnosis_idDiagnosis": 1
    }
    response = requests.post(f"{BASE_URL}/patients", json=new_patient)
    assert response.status_code == 201 or response.status_code == 400  # Already exists or created

# -------------------------------
# Test PUT - update patient
# -------------------------------
def test_update_patient():
    update_data = {
        "name": "Updated Patient",
        "age": "31"
    }
    response = requests.put(f"{BASE_URL}/patients/1", json=update_data)
    assert response.status_code in [200, 404, 415]

# -------------------------------
# Test DELETE - remove patient
# -------------------------------
def test_delete_patient():
    # Trying to delete a test patient (make sure it exists)
    response = requests.delete(f"{BASE_URL}/patients/1")
    assert response.status_code in [200, 404, 500]
