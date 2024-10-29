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
params_file = "src\\main\\java\\test\\cors\\connection\\connect\\params.txt"

def load_params():
    """파일에서 파라미터를 읽어와 params 딕셔너리를 초기화합니다."""
    global params
    try:
        with params_lock:
            with open(params_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if value.startswith("(") and value.endswith(")"):  # 튜플 형식으로 저장된 경우
                        params[key] = tuple(map(int, value.strip("()").split(",")))     # 튜플 내부는 INT
                    else:
                        params[key] = str(value)    # 이외의 형태는 str로 저장
    except FileNotFoundError:
        params = {}  # 파일이 없으면 빈 딕셔너리로 초기화

def set_TxtValue(key, value):

    # 모든 값을 문자열로 변환
    value = str(value)

    """키와 값을 설정하고 params.txt에 기록합니다. 주어진 키의 값은 갱신합니다."""
    # 파일에서 현재 값을 읽어옵니다.
    try:
        with open(params_file, "r") as f:
            for line in f:
                k, v = line.strip().split("=")
                params[k] = v
    except FileNotFoundError:
        pass  # 파일이 없으면 무시

    # 주어진 키가 이미 존재하는 경우 값을 변경
    if key in params:
        if isinstance(value, tuple):  # 튜플이면 괄호 추가
            params[key] = f"({','.join(map(str, value))})"
        else:
            params[key] = value  # 문자열로 저장
    else:
        # 새로운 키일 경우 기존 방식으로 추가
        if isinstance(value, tuple):  # 튜플이면 괄호 추가
            params[key] = f"({','.join(map(str, value))})"
        else:
            params[key] = value  # 문자열로 저장

    # 파일에 모든 키-값 쌍을 기록합니다.
    with params_lock:
        with open(params_file, "w") as f:
            for k, v in params.items():
                f.write(f"{k}={v}\n")  # 기록

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
    set_TxtValue("Fd_opacity", data.opacity)
    print("Received:", data.opacity, type(data.opacity))
    return {"message": "Data received", "received": data.opacity}

@app.post("/FdBtnColor") # Fd_hex Fd_bgr_color
async def slider_data(data: Foundation):
    print(params_file, data.hex, type(data.hex))
    bgr_color = hex_to_bgr(data.hex)
    set_TxtValue("Fd_hex", data.hex)
    set_TxtValue("Fd_bgr_color", bgr_color)
    print(f"bgr = {bgr_color}")
    return {"message": "Data received", "received": data.hex}

@app.post("/LipSlider") # Lip_opacity
async def slider_data(data: LIP):
    set_TxtValue("Lip_opacity", data.opacity)
    print("Received:", data.opacity, type(data.opacity))
    return {"message": "Data received", "received": data.opacity}

@app.post("/LipBtnColor") # Lip_Hex Lip_bgr_color
async def slider_data(data: LIP):
    print(params_file, data.hex, type(data.hex))
    bgr_color = hex_to_bgr(data.hex)
    set_TxtValue("Lip_Hex", data.hex)
    set_TxtValue("Lip_bgr_color", bgr_color)
    print(f"bgr = {bgr_color}")
    return {"message": "Data received", "received": data.hex}


## 서버 종료
@app.post("/shutdown")
async def shutdown():
    # 서버 종료
    os._exit(0)  # 0은 정상 종료 상태 코드
    return {"message": "서버가 종료됩니다."}



def putText_frames(frame_copy, text, color, yArea):
    # if not isinstance(text, str):
    #     text = str(text)
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
            load_params()  # 주기적으로 매개변수 읽기

            # # 매개변수를 텍스트로 출력
            # opacity:str / hex:str / bgr_color:Tuple(int,int,int)
            if params['Fd_opacity'] == "100":
                putText_frames(frame, "MAX", (0,255,255), 30)
            else:
                putText_frames(frame, f"opacity: {params['Fd_opacity']}", params['Fd_bgr_color'], 30)

            if params['Lip_opacity'] == "100":
                putText_frames(frame, "MAX", (0,255,255), 60)
            else:
                putText_frames(frame, f"opacity: {params['Lip_opacity']}", params['Lip_bgr_color'], 60)

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
    
    # txt 초기값
    set_TxtValue("Fd_opacity",0)
    set_TxtValue("Fd_hex","#000000")
    set_TxtValue("Fd_bgr_color",hex_to_bgr("#000000"))
    set_TxtValue("Lip_opacity",0)
    set_TxtValue("Lip_Hex","#000000")
    set_TxtValue("Lip_bgr_color",hex_to_bgr("#000000"))

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