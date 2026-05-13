from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class AdminUserUpdateRequest(BaseModel):
    role: Optional[str] = None
    vendorId: Optional[str] = None
    isActive: Optional[bool] = None


class ReceiptVerificationRequest(BaseModel):
    arrivalStatus: str
    issueType: Optional[str] = None
    evidenceUploaded: bool = False
    note: Optional[str] = None
