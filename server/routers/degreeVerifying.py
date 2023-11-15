from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
import schemas
import json
from server.ethereum.methods import get_record
from server.database import get_db
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import server.models as models
from server.custom_utils import crypto
from server.ethereum import methods
from server.config import settings
import json

router = APIRouter(prefix="/verify", tags=["Degree Verifying Institution"])

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/", response_class=HTMLResponse)
def show_block_details_form(request: Request, db: Session = Depends(get_db)):
    records = db.query(models.StudentRecordDetails).all()
    return templates.TemplateResponse("degree_verifying.html", {"request": request, "records": records})


@router.get("/download/{record_id}")
def download_record(record_id: int, db: Session = Depends(get_db)):
    student_record = db.query(models.StudentRecordDetails).filter(models.StudentRecordDetails.id == record_id).first()

    if not student_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Convert the student record to a JSON string
    encrypted_rec = jsonable_encoder(student_record)
    enc_dict = {
        "salt" : encrypted_rec['salt'],
        "cipher_text" : encrypted_rec['cipher_text'],
        "nonce" : encrypted_rec['nonce'],
        "tag" : encrypted_rec['tag']
    }

    shared_secret = crypto.generate_shared_secret(sender_private_key=settings.verifier_private_key,receiver_public_key=student_record.student_public_key)
    decrypted_rec = crypto.decrypt(enc_dict=enc_dict,passphrase=shared_secret)
    decrypted_rec = json.loads(decrypted_rec)
    student_rec = methods.get_record(decrypted_rec['block_number'])
    passphrase = decrypted_rec['encryption_details']['passphrase']
    decrypted_rec['encryption_details']['cipher_text'] = student_rec
    student_rec = json.loads(crypto.decrypt(enc_dict=decrypted_rec['encryption_details'],passphrase=passphrase))
    response = JSONResponse(content=student_rec, media_type="application/json")
    response.headers["Content-Disposition"] = f'attachment; filename="record_{record_id}.txt'
    return response


@router.post(
    "/", status_code=status.HTTP_201_CREATED)
def verify_record(record: schemas.BlockDetails):
    try:
        json_record = jsonable_encoder(record)
        block_number = json_record["block_number"]
        cipher_text = get_record(block_number=block_number)
        enc_dict = json_record["encryption_details"]
        enc_dict["cipher_text"] = cipher_text
        decrypted_student_details = json.loads(crypto.decrypt(enc_dict=enc_dict))
        return JSONResponse(content=decrypted_student_details)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error",
        )
