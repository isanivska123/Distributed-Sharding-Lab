from fastapi import FastAPI, HTTPException
import requests
from .models import Record
from .hashing import ConsistentHashing

app = FastAPI(title="Distributed Coordinator (Modular)")
hash_ring = ConsistentHashing()

@app.post("/register-shard")
def register_shard(url: str):
    hash_ring.add_shard(url)
    return {"status": "registered", "shard": url}

@app.post("/tables/{table_name}/records")
def create_record(table_name: str, record: Record):
    target_shard = hash_ring.get_shard(record.partition_key_value)
    if not target_shard:
        raise HTTPException(status_code=500, detail="No shards available")
    
    composite_key = f"{record.partition_key_value}#{record.sort_key_value}"
    payload = {"composite_key": composite_key, "value": record.data}
    
    response = requests.post(f"{target_shard}/insert", json=payload)
    return {"target_shard": target_shard, "shard_response": response.json()}

@app.get("/tables/{table_name}/records/{part_val}/{sort_val}")
def read_record(table_name: str, part_val: str, sort_val: str):
    target_shard = hash_ring.get_shard(part_val)
    composite_key = f"{part_val}#{sort_val}"
    response = requests.get(f"{target_shard}/get/{composite_key}")
    return response.json()

@app.get("/tables/{table_name}/exists/{part_val}/{sort_val}")
def exists_record(table_name: str, part_val: str, sort_val: str):
    target_shard = hash_ring.get_shard(part_val)
    composite_key = f"{part_val}#{sort_val}"
    response = requests.get(f"{target_shard}/get/{composite_key}")
    return {"exists": response.json().get("data") is not None}

@app.delete("/tables/{table_name}/records/{part_val}/{sort_val}")
def delete_record(table_name: str, part_val: str, sort_val: str):
    target_shard = hash_ring.get_shard(part_val)
    composite_key = f"{part_val}#{sort_val}"
    response = requests.delete(f"{target_shard}/delete/{composite_key}")
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)