from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc

# Configuración de la base de datos
DATABASE_URL = (
    "mssql+pyodbc://db_a9d1fc_tsiai_admin:TSI555$$$@SQL8005.site4now.net/db_a9d1fc_tsiai_admin?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class PhoneNumberModel(Base):
    __tablename__ = 'phone_numbers_test_with_front'
    phone_number = Column(String, primary_key=True, index=True)
    auth_token = Column(String)
    twilio_sid = Column(String)
    label = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI()


class PhoneNumberSchema(BaseModel):
    phone_number: str
    auth_token: str
    twilio_sid: str
    label: str

@app.post("/api/phone_numbers")
async def create_phone_number(phone_number: PhoneNumberSchema):
    db = SessionLocal()
    phone_entry = PhoneNumberModel(
        phone_number=phone_number.phone_number,
        auth_token=phone_number.auth_token,
        twilio_sid=phone_number.twilio_sid,
        label=phone_number.label
    )

    db.add(phone_entry)
    try:
        db.commit()
        db.refresh(phone_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Phone number already exists or an error occurred")
    finally:
        db.close()

    return {"message": "Phone number saved successfully!", "phone_number": phone_entry.phone_number}
