from typing import Any, Optional

def ok(message: str, data: Optional[Any] = None):
    return {"message": message, "status": "success", "data": data}

def err(message: str, data: Optional[Any] = None):
    return {"message": message, "status": "error", "data": data}
