import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.utils import JWT_SECRET, JWT_ALGORITHM
from app.schema_definitions import UserRole

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), role: str = Depends(get_current_user_role)):
    if role != UserRole.OPS:
        raise HTTPException(status_code=403, detail="Only OPS users can upload files.")

    allowed_extensions = ["pptx", "docx", "xlsx", "pdf"]
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": "File uploaded successfully.", "filename": filename}
