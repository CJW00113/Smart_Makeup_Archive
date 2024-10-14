import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import cv2
import asyncio  # 비동기처리
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, field_validator

# cors 미들웨어
from fastapi.middleware.cors import CORSMiddleware

import numpy as np

app = FastAPI()

# CORS 미들웨어 추가
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:9090",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()
templates = Jinja2Templates(directory="src\\main\\resources\\templates")

class Foundation(BaseModel):
    opacity: int = 0
    # Hex: str = "0"
    # colorBGR: np.ndarray = None
    # class Config:
    #     arbitrary_types_allowed = True  # numpy.ndarray와 같은 임의 타입을 허용
    
    # @field_validator('Hex', mode='before')
    # def validate_hex(cls, v):
    #     if not v.startswith('#') or len(v) != 7:
    #         raise ValueError('Hex color code must start with "#" and be followed by 6 characters')
    #     return v

    # @field_validator('colorBGR', mode='after')
    # def set_colorBGR(cls, v, values):
    #     hex_color = values.get('Hex', '0')
    #     if hex_color.startswith('#'):
    #         hex_color = hex_color[1:]  # '#' 제거
    #     # Hex 값을 BGR로 변환
    #     b = int(hex_color[4:6], 16)
    #     g = int(hex_color[2:4], 16)
    #     r = int(hex_color[0:2], 16)
    #     return np.array([b, g, r])  # BGR 배열 반환



# 전역 변수로 foundation 인스턴스 생성
foundation = Foundation()
current_websocket = None  # 현재 웹소켓 연결을 저장할 변수




@app.post("/slider")
async def slider_data(data: Foundation):
    global current_websocket
    print("Received:", data.opacity, type(data.opacity))
    return {"message": "Data received", "received": data.opacity}



@app.post("/btnColor")
async def slider_data(data: Foundation):
    print("Received:", data.Hex, type(data.Hex))
    return {"message": "Data received", "received": data.Hex}





def putText_frames(frame_copy, text, yArea):
    if not isinstance(text, str):
        text = str(text)
    return cv2.putText(frame_copy, text, (10, yArea), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       (255, 0, 0), 2)

async def video_feed(websocket: WebSocket):
    """ 웹소켓을 통해 웹캠 영상을 클라이언트에 스트리밍하는 함수 """
    await websocket.accept()
    
    # 웹캠 비디오 캡처 초기화
    cap = cv2.VideoCapture(0)

    try:
        while True:
            # 프레임 읽기
            ret, frame = cap.read()
            if not ret: # 프레임을 못읽었다면, break
                break

            # frame = putText_frames(frame, yourDataObject.value, 10)
            
            # 프레임을 JPEG 형식으로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            bytes_data = buffer.tobytes()
            
            # 웹소켓을 통해 클라이언트에 전송
            await websocket.send_bytes(bytes_data)

    # except WebSocketDisconnect:
    #     print("클라이언트 연결이 끊어졌습니다.")

    # finally:
    #     cap.release()  # 비디오 캡처 객체 해제
    #     await websocket.close()
    except WebSocketDisconnect:
        print("클라이언트가 페이지를 벗어났습니다.")
    except Exception as e:
        print(f"예외 발생: {e}")
    finally:
        cap.release()
        try:
            if websocket.client_state == "connected":  # 연결 상태 확인
                await websocket.close()
        except RuntimeError as e:
            print(f"WebSocket 종료 오류: {e}")


@app.websocket("/video-feed")
async def feed(websocket: WebSocket):
    """ 웹소켓 엔드포인트 """
    # await websocket.accept()

    # # 클라이언트로부터 초기 데이터 수신
    # data = await websocket.receive_text()  # 클라이언트가 전송한 데이터 수신
    # yourDataObject = YourDataObject(value=data)  # 수신한 데이터로 객체 생성

    await video_feed(websocket)









def is_camera_in_use(camera_index=0):
    # 카메라를 열어보려 시도
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        return True  # 카메라가 이미 사용 중임

    # 카메라를 정상적으로 열었으면 닫기
    cap.release()
    return False  # 카메라가 사용 중이지 않음

## 서버 실행 명령어 uvicorn main:app --reload
if __name__ == "__main__":
    if is_camera_in_use():
        print("웹캠이 이미 사용 중입니다.")
    else:
        print("웹캠을 사용할 수 있습니다.")
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    # uvicorn.run(app, port=8080)

## /docs 참고하면, 자동 대화형 API 문서 확인 가능
## tasklist | findstr python
## taskkill /F /PID 포트번호