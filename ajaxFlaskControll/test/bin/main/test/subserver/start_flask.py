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

# 로그 설정
logging.basicConfig(level=logging.INFO)

process = None

CORS(app)  # CORS 설정

@app.route('/')
def index():
    return render_template('slider_display.html')  # 새로운 HTML 페이지를 렌더링


# @app.route('/api/slider', methods=['POST', 'OPTIONS'])
# def slider():
#     if request.method == 'OPTIONS':
#         return '', 200  # CORS preflight 요청에 대한 응답
#     data = request.get_json()  # JSON 데이터 받기
#     if data:  # 데이터가 존재하는지 확인
#         value = data.get('value')  # 슬라이더 값 가져오기
#         print(f"Received slider value: {value}")  # 로그 출력
#     else:
#         print("No data received")  # 데이터가 없을 경우 로그 출력
#     return jsonify({'value': value})  # JSON 응답



@app.route('/api/slider', methods=['POST', 'OPTIONS'])
def slider():
    if request.method == 'OPTIONS':
        return '', 200  # CORS preflight 요청에 대한 응답
    data = request.get_json()  # JSON 데이터 받기
    value = data.get('value')  # 슬라이더 값 가져오기
    print(f"Received slider value: {value}")
    return jsonify({'value': value})  # JSON 응답

@app.route('/api/slider', methods=['GET'])
def get_slider_value():
    try:
        response = requests.get('http://localhost:9090/api/slider')  # Spring Boot 서버의 URL
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴
        slider_value = response.json().get('value', '값 없음')
        return jsonify({'value': slider_value})
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching slider value: {e}')
        return jsonify({'value': '오류 발생'})




def generate_frames(part1=None, part2=None, part3=None):
    cap = cv2.VideoCapture(0)
    while True:
        # success는 성공여부, frame은 캠의 이미지
        success, frame = cap.read()
        if not success:
            break

        frame_copy = frame.copy()

        # 입력값이 모두 없는 경우
        if part1 is None and part2 is None and part3 is None:
            frame_copy = putText_frames(frame_copy, 'Hello, World!', 30)
        
        # 입력값이 존재하는 경우
        else:
            if part1:   # part1의 입력값이 있는 경우
                frame_copy = putText_frames(frame_copy, f'RGB:{part1[0]}, 투명도:{part1[1]}', 30)
            if part2:   # part2의 입력값이 있는 경우
                frame_copy = putText_frames(frame_copy, f'RGB:{part2[0]}, 투명도:{part2[1]}', 50)
            if part3:   # part3의 입력값이 있는 경우
                frame_copy = putText_frames(frame_copy, f'RGB:{part3[0]}, 투명도:{part3[1]}', 70)

        # JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame_copy)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_copy + b'\r\n')

# (테스트용)부위별로 텍스트 설정 (화장부위 합칠 코드로 바뀔 예정)
def putText_frames(frame_copy, text, yArea):
    if not isinstance(text, str):
        text = str(text)
    return cv2.putText(frame_copy, text, (10, yArea), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       (255, 0, 0), 2)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def run_script():
    global process
    process = subprocess.Popen(['python', 'hello.py'])  # 실행할 스크립트 경로

if __name__ == '__main__':
    logging.info("Starting Flask server on port 8080...")
    app.run(port=8080)