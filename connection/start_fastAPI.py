from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn  # 포트 번호 설정하기 위해 사용

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:9090",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9090"],  # Spring Boot 서버의 URL
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 데이터 모델 정의
class Signal(BaseModel):
    id: int
    message: str

# 메모리에 저장할 리스트
signals: List[Signal] = []

# GET 요청 처리
@app.get("/signal/{signal_id}")
async def get_signal(signal_id: int):
    for signal in signals:
        if signal.id == signal_id:
            return signal
    return {"error": "Signal not found"}

@app.post("/signal/")
async def save_signal(signal: Signal):
    signals.append(signal)
    return {"message": "Signal saved", "signal": signal}

@app.get("/")
async def main():
    return {"message": "Hello World"}

## 서버 실행 명령어 uvicorn main:app --reload
if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    uvicorn.run(app, port=8080)

## /docs 참고하면, 자동 대화형 API 문서 확인 가능