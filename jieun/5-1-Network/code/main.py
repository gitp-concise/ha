from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Member(BaseModel):
    gi: str
    team: str
    role: str
    name: str

members = [
    {"gi": 23, "team": "DE팀", "role": "전 부대장", "name": "이어흥"},
    {"gi": 24, "team": "DE팀", "role": "DE 팀장", "name": "임채림"},
    {"gi": 22, "team": "DS팀", "role": "교육부장", "name": "김지훈"},
    {"gi": 24, "team": "DE팀", "role": "부회장", "name": "조윤영"},
    {"gi": 24, "team": "DS팀", "role": "회장", "name": "이동진"},
]

# 1. POST
@app.post("/list")
async def create_member(member: Member):
    members.append(member.dict())
    return {"message": "Member added successfully"}

# 2. GET
@app.get("/list")
async def read_members():
    return {"members": members}

# 3. PUT
@app.put("/list/{name}")
async def update_member(name: str, updated_member: Member):
    for member in members:
        if member['name'] == name:
            member.update(updated_member.dict())
            return {"message": "Member updated successfully"}
    raise HTTPException(status_code=404, detail="Member not found")

# 4. DELETE
@app.delete("/list/{name}")
async def delete_member(name: str):
    global members
    members = [member for member in members if member["name"] != name]
    return {"message": "Member deleted successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")