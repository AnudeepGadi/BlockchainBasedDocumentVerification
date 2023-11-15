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

from pathlib import Path

router = APIRouter(prefix="/grant", tags=["Degree Giving Institution"])
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/", response_class=HTMLResponse)
def show_student_form(request: Request):
    return templates.TemplateResponse("degree_granting.html", {"request": request})


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlockDetails
)
def add_record(record: schemas.StudentDetails):
    try:
        json_record = jsonable_encoder(record)

        # encryption
        passphrase = crypto.generate_passphrase(32)
        encrypted_data_details = crypto.encrypt(plain_text=json.dumps(json_record),passphrase=passphrase)
        encrypted_student_record = encrypted_data_details["cipher_text"]

        # adding to ethereum
        block_details = methods.add_record(encrypted_student_record=encrypted_student_record)

        del encrypted_data_details["cipher_text"]
        encrypted_data_details["passphrase"] = passphrase

        block_data = jsonable_encoder(
            {"block_number": block_details["blockNumber"], "encryption_details": encrypted_data_details})

        return JSONResponse(content=block_data)

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error",
        )
