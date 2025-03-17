from sqlalchemy import Column, Integer, String
from ..config.db import Base

class CertificateModel(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    storage_url = Column(String, nullable=False)
    private_key_url = Column(String, nullable=False)
    public_cert_url = Column(String, nullable=False)
