from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_name: str


class StaffMe(BaseModel):
    staff_id: int
    staff_email: EmailStr
    staff_name: str
    staff_role: str | None = None
    organization_id: int

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    sub: str
    organization_id: int
    exp: int
