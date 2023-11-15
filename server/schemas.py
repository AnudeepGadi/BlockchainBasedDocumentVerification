from pydantic import BaseModel
from typing import List


class SubjectGrade(BaseModel):
    name: str
    grade: str


class StudentDetails(BaseModel):
    name: str
    student_id: str
    subjects: List[SubjectGrade]
    cgpa: float


class EncryptionDetails(BaseModel):
    passphrase: str
    salt: str
    nonce: str
    tag: str


class SecretKeyEncryptionDetails(BaseModel):
    cipher_text: str
    salt: str
    nonce: str
    tag: str


class BlockDetails(BaseModel):
    block_number: int
    student_email: str
    encryption_details: EncryptionDetails


class EncryptedStudentDetails(BaseModel):
    encrypted_student_record: str
