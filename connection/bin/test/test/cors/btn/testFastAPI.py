import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="src\\main\\resources\\templates")

class SliderValue(BaseModel):
    slider_value: int

@app.get("/button", response_class=HTMLResponse)
async def read_button(request: Request, val: int = 0):
    return templates.TemplateResponse("testbutton.html", {"request": request, "val": val})

@app.post("/submit")
async def handle_submit(slider_value: SliderValue):
    print(f"버튼 값: {slider_value.slider_value}")
    return {"message": "버튼 값이 출력되었습니다!"}

## 서버 실행 명령어 uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    # uvicorn.run(app, port=8080)

## /docs 참고하면, 자동 대화형 API 문서 확인 가능