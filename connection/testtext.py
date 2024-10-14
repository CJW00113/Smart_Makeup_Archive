from fastapi import FastAPI
import cv2
import asyncio
import threading

app = FastAPI()
params_lock = threading.Lock()
params_file = "params.txt"

# 초기 매개변수 설정
params = {"brightness": 0, "contrast": 0}

def read_params():
    global params
    with params_lock:
        with open(params_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split("=")
                params[key] = int(value)

async def video_stream():
    cap = cv2.VideoCapture(0)
    while True:
        read_params()  # 주기적으로 매개변수 읽기
        ret, frame = cap.read()
        if not ret:
            break
        
        # 매개변수 적용 (예: 밝기와 대비 조정)
        frame = cv2.convertScaleAbs(frame, alpha=params["contrast"], beta=params["brightness"])

        # 매개변수를 텍스트로 출력
        text = f"Brightness: {params['brightness']}, Contrast: {params['contrast']}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(video_stream())

@app.post("/update_params/")
async def update_params(brightness: int, contrast: int):
    with params_lock:
        with open(params_file, "w") as f:
            f.write(f"brightness={brightness}\n")
            f.write(f"contrast={contrast}\n")
    return {"message": "Parameters updated"}
