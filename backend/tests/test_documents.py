import io
import pytest


def test_medical_documents_lifecycle_and_upload(client):
    # 1. Register Caregiver
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "dr.vance.docs@example.com",
            "password": "Password123!",
            "display_name": "Dr. Elena Vance",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    # 2. Create Patient
    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "Eli Vance", "email": "eli.docs@example.com"},
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Upload PDF Doctor Prescription (JSON Base64)
    sample_pdf_b64 = "data:application/pdf;base64,JVBERi0xLjQKMSAwIG9iajw8L1R5cGUvQ2F0YWxvZz4+ZW5kb2Jq"
    doc_res = client.post(
        f"/api/v1/patients/{patient_id}/documents",
        headers=auth_header,
        json={
            "title": "Donepezil 10mg Neurology Prescription",
            "document_type": "PRESCRIPTION",
            "doctor_name": "Dr. Elena Vance, Neurologist",
            "document_date": "2026-11-15",
            "notes": "Take 1 tablet daily with dinner. Monitor blood pressure.",
            "file_name": "Donepezil_Prescription.pdf",
            "file_type": "application/pdf",
            "file_size_bytes": 1024,
            "file_data_url": sample_pdf_b64,
        },
    )
    assert doc_res.status_code == 201
    doc = doc_res.json()
    assert doc["title"] == "Donepezil 10mg Neurology Prescription"
    assert doc["document_type"] == "PRESCRIPTION"
    assert doc["file_type"] == "application/pdf"
    doc_id = doc["id"]

    # 4. Upload Medical Condition Detail (Image)
    sample_img_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    img_res = client.post(
        f"/api/v1/patients/{patient_id}/documents",
        headers=auth_header,
        json={
            "title": "Brain MRI Scan & Clinical Evaluation",
            "document_type": "MEDICAL_CONDITION",
            "doctor_name": "City Radiology Center",
            "document_date": "2026-11-10",
            "notes": "Mild hippocampal volume reduction consistent with early amnestic MCI.",
            "file_name": "mri_brain_scan.png",
            "file_type": "image/png",
            "file_size_bytes": 2048,
            "file_data_url": sample_img_b64,
        },
    )
    assert img_res.status_code == 201
    assert img_res.json()["document_type"] == "MEDICAL_CONDITION"

    # 5. Upload via Multipart Form (`/upload`)
    fake_file_content = b"%PDF-1.4 Fake PDF Content for Multipart Test"
    multipart_res = client.post(
        f"/api/v1/patients/{patient_id}/documents/upload",
        headers=auth_header,
        data={
            "title": "Comprehensive Blood & Metabolic Lab Report",
            "document_type": "LAB_REPORT",
            "doctor_name": "Metro Diagnostic Labs",
            "document_date": "2026-11-16",
            "notes": "All electrolytes and B12 vitamins within healthy normal range.",
        },
        files={
            "file": ("lab_blood_report.pdf", io.BytesIO(fake_file_content), "application/pdf")
        },
    )
    assert multipart_res.status_code == 201
    assert multipart_res.json()["title"] == "Comprehensive Blood & Metabolic Lab Report"

    # 6. List Patient Documents
    list_res = client.get(f"/api/v1/patients/{patient_id}/documents", headers=auth_header)
    assert list_res.status_code == 200
    docs = list_res.json()
    assert len(docs) >= 3

    # Filter by document_type=PRESCRIPTION
    presc_res = client.get(
        f"/api/v1/patients/{patient_id}/documents?document_type=PRESCRIPTION",
        headers=auth_header,
    )
    assert presc_res.status_code == 200
    assert all(d["document_type"] == "PRESCRIPTION" for d in presc_res.json())

    # 7. Get Document Details
    detail_res = client.get(
        f"/api/v1/patients/{patient_id}/documents/{doc_id}", headers=auth_header
    )
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == doc_id

    # 8. Download / Stream Document File
    file_res = client.get(
        f"/api/v1/patients/{patient_id}/documents/{doc_id}/file", headers=auth_header
    )
    assert file_res.status_code == 200
    assert "application/pdf" in file_res.headers.get("content-type", "")
    assert len(file_res.content) > 0

    # 9. Test Invalid File Type Rejection
    invalid_res = client.post(
        f"/api/v1/patients/{patient_id}/documents",
        headers=auth_header,
        json={
            "title": "Malicious Executable",
            "document_type": "OTHER",
            "file_name": "virus.exe",
            "file_type": "application/x-msdownload",
            "file_size_bytes": 500,
        },
    )
    assert invalid_res.status_code == 400
    assert "Unsupported file type" in invalid_res.text

    # 10. Test Multi-Tenant Isolation
    stranger_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "stranger.care@example.com",
            "password": "Password123!",
            "display_name": "Stranger Care",
            "role": "CAREGIVER",
        },
    )
    stranger_header = {"Authorization": f"Bearer {stranger_res.json()['access_token']}"}

    forbidden_res = client.get(
        f"/api/v1/patients/{patient_id}/documents", headers=stranger_header
    )
    assert forbidden_res.status_code == 403

    # 11. Delete Document
    del_res = client.delete(
        f"/api/v1/patients/{patient_id}/documents/{doc_id}", headers=auth_header
    )
    assert del_res.status_code == 204

    # Verify deleted document is omitted from active list
    after_del = client.get(f"/api/v1/patients/{patient_id}/documents", headers=auth_header)
    assert all(d["id"] != doc_id for d in after_del.json())
