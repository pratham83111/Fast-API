from fastapi import FastAPI,HTTPException                                                                                               
from pydantic import BaseModel

app = FastAPI()
class Task (BaseModel):
    title : str
    description: str 
    completed : bool = False
    
tasks = []
@app.get("/")
def root(): 
    return{"message":"API RUNING"}

@app.post("/tasks")
def create_task(task : Task):
    task_dict = task.dict()
    task_dict["id"]= len(tasks)+1
    tasks.append(task_dict)
    return{"message":"task created","task":task_dict}



@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id:int):
    for task in tasks:
        if task["id"] == task_id :
            return task
    raise HTTPException(status_code=404,detail= "task not found")

@app.put("/tasks/{task_id}")
def update_task(task_id:int,update_task:Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"]=update_task.title
            task["description"]=update_task.description
            task["completed"]=update_task.completed
            return{"message":"task updated","task":task}
    raise HTTPException(status_code=404,detail= "task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)        # ← list se remove karo
            return {"message": "Task deleted!"}
    raise HTTPException(status_code=404, detail="Task not found")