from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()
class Note(BaseModel):
    title : str
    description: str 
    completed : bool = False
    
notes=[]
@app.get("/")
def root():
    return{"message":"API_RUNING"}

@app.post("/notes")
def create_note(note:Note):
    note_dict= note.dict()
    note_dict["id"]= len(notes)+1
    notes.append(note_dict)
    return{"message":"NOTE CREATED","note":note_dict}


@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id:int):
    for note in notes:
        if note["id"] == note_id :
            return note
    raise HTTPException(status_code=404,detail= "task not found")

@app.put("/notes/{note_id}")
def update_note(note_id:int,update_note:Note):
    for note in notes:
        if note["id"] == note_id:
            note["title"]=update_note.title
            note["description"]=update_note.description
            note["completed"]=update_note.completed
            return{"message":"note updated","task":note}
    raise HTTPException(status_code=404,detail= "note not found")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(index)        
            return {"message": "note deleted!"}
    raise HTTPException(status_code=404, detail="Task not found")