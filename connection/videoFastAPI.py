import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np

app = FastAPI()

async def video_feed(websocket: WebSocket):
    """ 웹소켓을 통해 웹캠 영상을 클라이언트에 스트리밍하는 함수 """
    await websocket.accept()
    
    # 웹캠 비디오 캡처 초기화
    cap = cv2.VideoCapture(0)

    try:
        while True:
            # 프레임 읽기
            ret, frame = cap.read()
            if not ret:
                break
            
            # 프레임을 JPEG 형식으로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            bytes_data = buffer.tobytes()
            
            # 웹소켓을 통해 클라이언트에 전송
            await websocket.send_bytes(bytes_data)

    except WebSocketDisconnect:
        print("클라이언트 연결이 끊어졌습니다.")
    
    finally:
        cap.release()  # 비디오 캡처 객체 해제
        await websocket.close()

@app.websocket("/video-feed")
async def feed(websocket: WebSocket):
    """ 웹소켓 엔드포인트 """
    await video_feed(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    # uvicorn.run(app, port=8080)