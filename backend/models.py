from sqlalchemy import Column, String, Integer, Float, JSON
from database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    statusText = Column(String)
    trustScore = Column(Float)
    trend = Column(Float)
    trendDir = Column(String)
    address = Column(String)
    joinDate = Column(String)
    schools = Column(JSON)

class School(Base):
    __tablename__ = "schools"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    npsn = Column(String)
    address = Column(String)
    vendorId = Column(String, index=True)
    vendorName = Column(String)
    trustScore = Column(Float)
    status = Column(String)
    statusText = Column(String)

class Distribution(Base):
    __tablename__ = "distributions"
    
    id = Column(String, primary_key=True, index=True)
    vendorId = Column(String, index=True)
    schoolName = Column(String)
    porsi = Column(Integer)
    status = Column(String)
    statusText = Column(String)
    time = Column(String)
    riskScore = Column(Float)
    menuName = Column(String)
    menuUtama = Column(String)
    suhu = Column(Float)
    durasi = Column(Integer)
    levelRisiko = Column(String)
    catatan = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    vendorName = Column(String)
    description = Column(String)
    time = Column(String)
    statusTag = Column(String)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    vendorId = Column(String, index=True)
    name = Column(String)
    expiry = Column(String)
    status = Column(String)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    avatar = Column(String)

