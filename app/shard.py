from fastapi import FastAPI
import requests
import sys
from .models import ShardRecord

app = FastAPI()
data_store = {}

@app.post("/insert")
def insert(record: ShardRecord):
    data_store[record.composite_key] = record.value
    return {"status": "ok"}

@app.get("/get/{key}")
def get_data(key: str):
    return {"data": data_store.get(key)}

@app.delete("/delete/{key}")
def delete_data(key: str):
    if key in data_store:
        del data_store[key]
        return {"status": "deleted"}
    return {"status": "not_found"}

if __name__ == "__main__":
    import uvicorn
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    
    try:
        requests.post(f"http://127.0.0.1:8000/register-shard?url=http://127.0.0.1:{port}")
    except:
        print("Coordinator not found, running standalone")

    uvicorn.run(app, host="0.0.0.0", port=port)