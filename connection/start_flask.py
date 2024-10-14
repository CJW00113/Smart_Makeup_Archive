from flask import Flask, Response, request, jsonify, render_template

import logging
import requests  # Spring Boot 서버와 통신을 위해 requests 모듈 사용
import os
from flask_cors import CORS
import cv2
import subprocess


app = Flask(__name__)
# app = Flask(__name__, template_folder='src/main/resources/templates/flask')

# Spring Boot의 출처 허용
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:9090"}})
# CORS(app, origins="http://localhost:9090")  # Spring Boot 서버의 출처를 지정
CORS(app)  # 개발때만 사용, CORS

# 로그 설정
logging.basicConfig(level=logging.INFO)

process = None

@app.route("/")
def hello():
    return "Hello World!"


# 받아오는 값 저장용
class Transparent:
    def __init__(self, transparent=None):  # 초기값을 None으로 설정
        self._transparent = transparent  # private 변수
    # Getter
    @property
    def transparent(self):
        return self._transparent
    # Setter
    @transparent.setter
    def transparent(self, transparent):
        self._transparent = transparent

# # 이렇게 변수받을 예정
# foundation = User()
# lips = User()
# eyeliner = User()

# 테스트용 변수 저장용 객체 생성
user = Transparent()

# # 값 받아오는거
# @app.route('/api/data', methods=['GET'])
# def receive_data():
#     data = request.args.get('value')  # GET 파라미터에서 값 추출
#     print(f"Received data from Spring Boot: {data}")  # 터미널에 데이터 출력
#     user.transparent = data  # 객체에 저장(전역변수로 저장)
#     print(f"들어간 값: {user.transparent}")
#     return jsonify({"status": "success", "data": user.transparent})  # 클라이언트에 응답 반환

@app.route('/api/data', methods=['POST'])
def receive_data():
    logging.info(f"출력 테스트 receive_data 초기 {data}")
    data = request.data.decode('utf-8')  # 바이트로 수신한 데이터 디코드
    logging.info(f"출력 테스트 receive_data 인토딩 후 {data}") 
    print(f"Received data from Spring Boot: {data}")  # 터미널에 데이터 출력
    user.transparent = data # 객체에 저장(전역변수로 저장)
    print(f"들어간 값: {user.transparent}")
    logging.info(f"출력 테스트 receive_data 전역번수 저장된거로 {user.transparent}")
    return jsonify({"status": "success", "data": user.transparent})  # 클라이언트에 응답 반환

# def generate_frames():
#     print("1")
#     cap = cv2.VideoCapture(0)
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         # 프레임에 글자 추가
#         cv2.putText(frame, 'Hello, World!', (10, 30), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, 
#                     (255, 0, 0), 2)

#         # JPEG로 인코딩
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), 
#                     mimetype='multipart/x-mixed-replace; boundary=frame')



def generate_frames(part1):
    print("읽는중")
    logging.info("읽는중")
    cap = cv2.VideoCapture(0)
    logging.info("읽음")
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        logging.info("비디오 스트림이 안댐")
        return

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            print("Error: Could not read frame.")
            continue

        frame_copy = frame.copy()

        if part1 is None:
            frame_copy = putText_frames(frame_copy, 'Hello, World!', 30)
        else:
            if part1:  # part1의 입력값이 있는 경우
                frame_copy = putText_frames(frame_copy, f'투명도:{part1}', 30)

        ret, buffer = cv2.imencode('.jpg', frame_copy)
        if not ret:
            print("Error: Could not encode frame.")
            continue
            
        frame_copy = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_copy + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(user.transparent), 
                    mimetype='multipart/x-mixed-replace; boundary=frame_copy')

def putText_frames(frame_copy, text, yArea):
    if not isinstance(text, str):
        text = str(text)
    return cv2.putText(frame_copy, text, (10, yArea), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       (255, 0, 0), 2)


def is_camera_in_use(camera_index=0):
    # 카메라를 열어보려 시도
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        return True  # 카메라가 이미 사용 중임

    # 카메라를 정상적으로 열었으면 닫기
    cap.release()
    return False  # 카메라가 사용 중이지 않음

if __name__ == '__main__':
    if is_camera_in_use():
        print("웹캠이 이미 사용 중입니다.")
    else:
        print("웹캠을 사용할 수 있습니다.")

    logging.info("Starting Flask server on port 8080...")
    print("와연결됨 1")
    logging.info("와연결됨 2")
    app.run(port=8080)
    # app.run(host='0.0.0.0', port=8080)
