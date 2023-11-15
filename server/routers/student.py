from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import schemas
import json
from server.custom_utils import crypto
from server.ethereum import methods
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import traceback
from server.config import settings
from pathlib import Path
import server.models as models
from server.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/student", tags=["Send Degree Details"])
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/", response_class=HTMLResponse)
def show_block_details_form(request: Request):
    return templates.TemplateResponse("student_block.html", {"request": request})


@router.post(
    "/secure_send", status_code=status.HTTP_201_CREATED, response_model=schemas.SecretKeyEncryptionDetails
)
def encrypt_block(record: schemas.BlockDetails, db: Session = Depends(get_db)):
    try:
        json_record = jsonable_encoder(record)
        student_email = json_record.pop('student_email')

        hex_ecdh_passphrase = crypto.generate_shared_secret(sender_private_key=settings.student_private_key, receiver_public_key=settings.verifier_public_key)

        # encryption
        encrypted_block_details = crypto.encrypt(plain_text=json.dumps(json_record), passphrase=hex_ecdh_passphrase)

        encrypted_block_details["student_public_key"] = settings.student_public_key
        encrypted_block_details["student_email"] = student_email
        db.add(models.StudentRecordDetails(**encrypted_block_details))
        db.commit()

        return JSONResponse(content=encrypted_block_details)

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error",
        )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlockDetails
)
def encrypt_block(record: schemas.StudentDetails):
    try:
        json_record = jsonable_encoder(record)

        # encryption
        encrypted_data_details = crypto.encrypt(plain_text=json.dumps(json_record))
        encrypted_student_record = encrypted_data_details["cipher_text"]

        # adding to ethereum
        block_details = methods.add_record(encrypted_student_record=encrypted_student_record)

        del encrypted_data_details["cipher_text"]
        block_data = jsonable_encoder(
            {"block_number": block_details["blockNumber"], "encryption_details": encrypted_data_details})

        return JSONResponse(content=block_data)

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error",
        )
