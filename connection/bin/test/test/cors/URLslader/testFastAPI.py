from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn  # 포트 번호 설정하기 위해 사용

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
# 템플릿 디렉토리 설정
# templates = Jinja2Templates(directory="src\\main\\resources\\templates")
templates = Jinja2Templates(directory="src\\test\\java\\test\\cors\\URLslader")

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

@app.get("/range", response_class=HTMLResponse)
async def read_range(request: Request, val: int = 0):
    return templates.TemplateResponse("testrange.html", {"request": request, "val": val})

@app.post("/submit")
async def handle_submit(slider_value: dict):
    print(f"슬라이더 값: {slider_value['slider_value']}")
    return {"message": "슬라이더 값이 출력되었습니다!"}


## 서버 실행 명령어 uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    # uvicorn.run(app, port=8080)

## /docs 참고하면, 자동 대화형 API 문서 확인 가능