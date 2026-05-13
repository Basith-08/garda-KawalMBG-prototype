from sqlalchemy import Column, String, Integer, Float, JSON, Boolean, DateTime, ForeignKey
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
    vendorId = Column(String, ForeignKey("vendors.id"), index=True)
    vendorName = Column(String)
    trustScore = Column(Float)
    status = Column(String)
    statusText = Column(String)

class Distribution(Base):
    __tablename__ = "distributions"
    
    id = Column(String, primary_key=True, index=True)
    vendorId = Column(String, ForeignKey("vendors.id"), index=True)
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
    cookedAt = Column(String, nullable=True)
    packagedAt = Column(String, nullable=True)
    pickupAt = Column(String, nullable=True)
    deliveredAt = Column(String, nullable=True)
    arrivalStatus = Column(String, nullable=True)
    receiptIssueType = Column(String, nullable=True)
    receiptEvidenceUploaded = Column(Boolean, nullable=False, default=False)
    receiptNote = Column(String, nullable=True)
    receiptVerifiedAt = Column(DateTime(timezone=True), nullable=True)
    qcPhotoUploaded = Column(Boolean, nullable=False, default=False)
    productionPhotoUploaded = Column(Boolean, nullable=False, default=False)
    packagingPhotoUploaded = Column(Boolean, nullable=False, default=False)
    vehiclePhotoUploaded = Column(Boolean, nullable=False, default=False)
    evidenceUploaded = Column(Boolean, nullable=False, default=False)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    vendorId = Column(String, ForeignKey("vendors.id"), index=True, nullable=True)
    vendorName = Column(String)
    description = Column(String)
    time = Column(String)
    statusTag = Column(String)


class RiskScoreHistory(Base):
    __tablename__ = "risk_scores"

    id = Column(String, primary_key=True, index=True)
    distributionId = Column(String, ForeignKey("distributions.id"), index=True, nullable=False)
    vendorId = Column(String, ForeignKey("vendors.id"), index=True, nullable=False)
    finalRiskScore = Column(Float, nullable=False)
    riskStatus = Column(String, nullable=False)
    componentScores = Column(JSON, nullable=True)
    summary = Column(String, nullable=True)
    assessedAt = Column(DateTime(timezone=True), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    actorUserId = Column(String, ForeignKey("users.id"), index=True, nullable=True)
    action = Column(String, nullable=False)
    entityType = Column(String, nullable=False)
    entityId = Column(String, nullable=False, index=True)
    details = Column(JSON, nullable=True)
    createdAt = Column(DateTime(timezone=True), nullable=False)


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    vendorId = Column(String, ForeignKey("vendors.id"), index=True)
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
    vendorId = Column(String, ForeignKey("vendors.id"), index=True, nullable=True)
    isActive = Column(Boolean, nullable=False, default=True)
    createdAt = Column(DateTime(timezone=True), nullable=True)
    lastLoginAt = Column(DateTime(timezone=True), nullable=True)
    avatar = Column(String)
