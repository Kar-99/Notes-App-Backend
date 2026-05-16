from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, User, Note
import schemas
import auth

app = FastAPI()

security = HTTPBearer()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    user_id = auth.verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    return user


@app.get("/")
def home():
    return {"message": "Notes App API"}


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = auth.hash_password(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = auth.verify_password(
        user.password,
        existing_user.password
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = auth.create_access_token(
        data={"user_id": existing_user.id}
    )

    return {
        "access_token": access_token
    }


@app.post("/notes")
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "message": "Note created successfully"
    }

@app.get("/notes", response_model=list[schemas.NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).all()

    return notes


@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note

@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    updated_note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()
    db.refresh(note)

    return {
        "message": "Note updated successfully"
    }

@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    updated_note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()
    db.refresh(note)

    return {
        "message": "Note updated successfully"
    }

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }


@app.post("/notes/{note_id}/share")
def share_note(
    note_id: int,
    share_data: schemas.ShareNote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    target_user = db.query(User).filter(
        User.email == share_data.email
    ).first()

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="Target user not found"
        )

    note.shared_users.append(target_user)

    db.commit()

    return {
        "message": f"Note shared with {target_user.email}"
    }

@app.get("/shared-notes", response_model=list[schemas.NoteResponse])
def get_shared_notes(
    current_user: User = Depends(get_current_user)
):

    return current_user.shared_with_me

@app.get("/about")
def about():

    return {
        "name": "Kartik Pandey",
        "email": "kartikpandey139.you@gmail.com",

        "my_features": {
            "Note Sharing":
            "Users can securely share notes with other registered users using email-based sharing."
        }
    }