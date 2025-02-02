from fastapi import FastAPI
import uvicorn

# Указываем интерпретатору где находится src/main.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

# Импорт endpoints
from src.api.routes.hotels import router as router_hotels

# Подключение базы данных
from src.database import *

app = FastAPI()

# Присоединение endpoints
app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)