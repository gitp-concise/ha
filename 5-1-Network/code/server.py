from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


class Member(BaseModel):
    gi: str
    team: str
    role: str
    name: str


data_store: Dict[str, dict] = {}

app: FastAPI = FastAPI()


@app.get("/list")
async def get_all() -> list[Dict[str, str]]:
    return list(data_store.values())


@app.post("/list")
async def add_member(member: Member) -> Dict[str, str | dict]:
    if member.name in data_store:
        raise HTTPException(status_code=400, detail="member with this name already exist")
    data_store[member.name] = member.dict()
    return {"status": "success", "received_data:": member.dict()}


@app.put("/list/{name}")
async def update_member(name: str, member: Member) -> Dict[str, str | dict]:
    if name not in data_store:
        raise HTTPException(status_code=404, detail="data not found")
    del data_store[name]
    data_store[member.name] = member.dict()
    return {"status": "success", "received_data:": member.dict()}


@app.delete("/list/{name}")
async def delete_data(name: str) -> Dict[str, str]:
    if name not in data_store:
        raise HTTPException(status_code=404, detail="data not found")
    del data_store[name]
    return {"status": "success", "deleted_name: ": name}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
