import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


from typing import List, Dict, Any

def save_message(session_id: str, role: str, message: str) -> None:
    key = f"chat:{session_id}"

    r.rpush(key, json.dumps({
        "role": role,
        "message": message
    }))


def get_history(session_id: str) -> List[Dict[str, Any]]:
    key = f"chat:{session_id}"

    messages = r.lrange(key, 0, -1)

    return [json.loads(m) for m in messages]


def clear_history(session_id: str) -> None:
    r.delete(f"chat:{session_id}")