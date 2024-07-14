import json
import os
from typing import Dict, Any

class JSONFileStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def read(self) -> Dict[str, Any]:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def write(self, data: Dict[str, Any]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get(self, key: str) -> Any:
        data = self.read()
        return data.get(key)

    def set(self, key: str, value: Any):
        data = self.read()
        data[key] = value
        self.write(data)

    def delete(self, key: str):
        data = self.read()
        if key in data:
            del data[key]
            self.write(data)

    def list_keys(self) -> list:
        return list(self.read().keys())