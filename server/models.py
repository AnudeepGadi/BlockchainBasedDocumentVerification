from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database import Base


class StudentRecordDetails(Base):
    __tablename__ = "student_record_details"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, nullable=False)
    student_email = Column(String, nullable=False)
    cipher_text = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    nonce = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    student_public_key = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
