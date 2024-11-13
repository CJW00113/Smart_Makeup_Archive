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
import os

import threading

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

params = {}
params_lock = threading.Lock()
params_file = "src\\main\\java\\com\\smwhc\\smart_makeup_web\\WebCam\\params.txt"

# 초기 값 설정
data_store = {
    "lip_bgr": (0, 0, 0),
    "lip_hex": "#000000",
    "fd_bgr": (0, 0, 0),
    "fd_hex": "#000000",
    "lip_opacity": 0,
    "fd_opacity": 0
}



def hex_to_bgr(hex_code):
    # 헥사 코드 형식 확인
    if not isinstance(hex_code, str) or not (len(hex_code) == 7 and hex_code.startswith('#')):
        raise ValueError("유효한 헥사 코드 형식이 아닙니다. 예: '#RRGGBB'")
    
    hex_code = hex_code.lstrip('#')
    # 헥사 코드가 6자리인지 확인
    if len(hex_code) != 6:
        raise ValueError("유효한 헥사 코드 형식이 아닙니다. 예: '#RRGGBB'")
    try:
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
    except ValueError:
        raise ValueError("헥사 코드에 잘못된 문자가 포함되어 있습니다.")
    # BGR 형식으로 반환
    return (b, g, r)


# 값을 설정하는 함수
def set_value(key, value):
    if key not in data_store:
        raise ValueError(f"Invalid key: {key}")
    
    if key == "lip_hex":
        if not value.startswith("#") or len(value) != 7:
            raise ValueError(f"Invalid HEX value for {key}: {value}")
        data_store[key] = value
        # HEX 값을 BGR로 변환
        bgr = hex_to_bgr(value)
        data_store["lip_bgr"] = bgr
        print(f"Updated {key}: {data_store[key]}")
        print(f"Updated lip_bgr: {data_store['lip_bgr']}")
    
    elif key == "fd_hex":
        if not value.startswith("#") or len(value) != 7:
            raise ValueError(f"Invalid HEX value for {key}: {value}")
        data_store[key] = value
        # HEX 값을 BGR로 변환
        bgr = hex_to_bgr(value)
        data_store["fd_bgr"] = bgr
        print(f"Updated {key}: {data_store[key]}")
        print(f"Updated fd_bgr: {data_store['fd_bgr']}")
    
    elif key == "lip_opacity":
        # if not (0 <= value <= 100):
        #     raise ValueError(f"Invalid opacity value for {key}: {value}")
        data_store[key] = value
        print(f"Updated {key}: {data_store[key]}")
    
    elif key == "fd_opacity":
        # if not (0 <= value <= 100):
        #     raise ValueError(f"Invalid opacity value for {key}: {value}")
        data_store[key] = value
        print(f"Updated {key}: {data_store[key]}")

# 값을 비동기적으로 가져오는 함수
def get_value(key):
    if key not in data_store:
        raise ValueError(f"Invalid key: {key}")
    
    return data_store[key]



class Foundation(BaseModel):
    opacity: int = 0
    hex: str = "0"

class LIP(BaseModel):
    opacity: int = 0
    hex: str = "0"

# # 전역 변수로 foundation 인스턴스 생성, 비동기가 변하는 전역변수를 못읽음
# foundation = Foundation()

@app.post("/FdSlider") # Fd_opacity
async def slider_data(data: Foundation):
    # 큐 생성
    set_value("fd_opacity", data.opacity)     # FD opacity to 85%

    print("Received:", data.opacity, type(data.opacity))
    return {"message": "Data received", "received": data.opacity}

@app.post("/FdBtnColor") # Fd_hex Fd_bgr_color
async def slider_data(data: Foundation):
    print(params_file, data.hex, type(data.hex))
    bgr_color = hex_to_bgr(data.hex)

    # 큐 생성
    set_value("fd_hex", data.hex)   # SteelBlue color for fd_hex

    print(f"bgr = {bgr_color}")
    return {"message": "Data received", "received": data.hex}

@app.post("/LipSlider") # Lip_opacity
async def slider_data(data: LIP):

    # 큐 생성
    set_value("lip_opacity", data.opacity)    # Lip opacity to 75%

    print("Received:", data.opacity, type(data.opacity))
    return {"message": "Data received", "received": data.opacity}

@app.post("/LipBtnColor") # Lip_Hex Lip_bgr_color
async def slider_data(data: LIP):
    print(params_file, data.hex, type(data.hex))
    bgr_color = hex_to_bgr(data.hex)

    # 큐 생성
    set_value("lip_hex", data.hex)  # Tomato color for lip_hex

    print(f"bgr = {bgr_color}")
    return {"message": "Data received", "received": data.hex}


## 서버 종료
@app.post("/shutdown")
async def shutdown():
    # 서버 종료
    os._exit(0)  # 0은 정상 종료 상태 코드
    return {"message": "서버가 종료됩니다."}

def putText_frames(frame_copy, text, color, yArea):
    if not isinstance(text, str):
        text = str(text)
    if text == '0':
        return
    return cv2.putText(frame_copy, text, (10, yArea), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       color, 2)

async def video_feed(websocket: WebSocket):
    """ 웹소켓을 통해 웹캠 영상을 클라이언트에 스트리밍하는 함수 """
    await websocket.accept()
    # 웹캠 비디오 캡처 초기화
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"카메라 해상도: {width} x {height}")

    try:
        while True:
            # 프레임 읽기
            ret, frame = cap.read()
            if not ret: # 프레임을 못읽었다면, break
                break

            # 값 가져오기 (opacity->INT, bgr->TUPLE, hex->STR)
            lip_bgr = get_value("lip_bgr")
            # lip_hex = get_value("lip_hex")
            fd_bgr = get_value("fd_bgr")
            # fd_hex = get_value("fd_hex")
            lip_opacity = get_value("lip_opacity")
            fd_opacity = get_value("fd_opacity")

            # # 한 번에 모든 값과 타입 출력 (확인용)
            # print(
            #     f"lip_bgr: {lip_bgr}, 타입: {type(lip_bgr)} | "
            #     f"lip_hex: {lip_hex}, 타입: {type(lip_hex)} | "
            #     f"fd_opacity: {fd_opacity}, 타입: {type(fd_opacity)} | "
            #     f"lip_opacity: {lip_opacity}, 타입: {type(lip_opacity)} | "
            #     f"fd_bgr: {fd_bgr}, 타입: {type(fd_bgr)} | "
            #     f"fd_hex: {fd_hex}, 타입: {type(fd_hex)}"
            # )

            # fd_opacity 처리
            if fd_opacity == "100":
                putText_frames(frame, "MAX", (0, 255, 255), 30)
            else:
                putText_frames(frame, f"FDopacity: {fd_opacity}", fd_bgr, 30)
            # lip_opacity 처리
            if lip_opacity == "100":
                putText_frames(frame, "MAX", (0, 255, 255), 60)
            else:
                putText_frames(frame, f"LIPopacity: {lip_opacity}", lip_bgr, 60)



            # 프레임을 JPEG 형식으로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            bytes_data = buffer.tobytes()
            
            # 웹소켓을 통해 클라이언트에 전송
            await websocket.send_bytes(bytes_data)
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

    ## 뒤에 있어야함. 그래야  txt 초기화 코드가 실행됨, 근데뭔가뭔가하자가있는듯함뭔가뭔가임기분탓같은데뭔가뭔가뭔가임
    uvicorn.run(app, port=8080)

    ## 테스트용)
    # uvicorn.run(app, host="127.0.0.1", port=8080, reload=False) # 디버깅아님
    # uvicorn.run(app, host="127.0.0.1", port=8080, reload=True) # 디버깅모드임

## 경로/docs 참고하면, 자동 대화형 API 문서 확인 가능

## 종료방법 :
### tasklist | findstr python
### netstat -ano | findstr :"포트번호"
### netstat -ano | findstr :8080
### taskkill /F /PID "PID번호"
### taskkill /F /PID 