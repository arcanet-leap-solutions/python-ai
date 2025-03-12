from sqlalchemy import Column, Integer, String
from ..config.db import Base

class CertificateModel(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    private_key = Column(String, nullable=False)
    public_cert = Column(String, nullable=False)
