from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app=FastAPI()

notes=[]

class Note(BaseModel):
    id: int
    title: str
    content: str
    
@app.get("/")
def home():
    return {"message": "Welcome to the Notes API"}

@app.post("/notes/",response_model=Note)
def create_note(note: Note):
    for existing_note in notes:
        if existing_note.id == note.id:
            raise HTTPException(status_code=400,detail="ID already exists.")
    
    notes.append(note)
    return note

@app.get("/notes/",response_model=List[Note])
def get_notes():
    return notes

@app.get("/notes/{note_id}",response_model=Note)
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=400, detail="Note not found.")

@app.put("/notes/{note_id}",response_model=Note)
def update_note(note_id: int, update_note: Note):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes[index] = update_note
            return update_note
    raise HTTPException(status_code=400, detail="Note not found.")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            del notes[index]
            return {"message":"Note deleted successfully!!"}
    raise HTTPException(status_code=400, detail="Note not found.")