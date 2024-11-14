
### 해당 구문은 캠 화면 대신 이미지를 사용하는 경우임

# # 해당 구문의 video_feed() 함수만 수정
# # frame = cv2.imread('절대 경로')에서 이미지는 FastAPIServer.py와 같은 위치에 두고, 절대경로를 사용할 것
# # 이미지/동영상 사용 시, html의 출력 화면은 640x480이니 이상하게 보이는 경우에는 되도록 비슷하게 자를것, (cv2.resize(frame, (640, 480))를 통해 어느정도는 커버가 될것)



async def video_feed(websocket: WebSocket):
    """ 웹소켓을 통해 웹캠 영상을 클라이언트에 스트리밍하는 함수 """
    await websocket.accept()
    # 웹캠 비디오 캡처 초기화
    # cap = cv2.VideoCapture(0)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print(f"카메라 해상도: {width} x {height}")

    try:
        while True:
            # 프레임 읽기
            # ret, frame = cap.read()
            # frame = cv2.imread('C:\\Users\\ezen\\Desktop\\Smart_Makeup_Web-main\\smart_makeup_web\\src\\main\\python\\server\\image.jpg') # 이미지 출력구
            makeup_instance = start_Makeup()
            # if not ret: # 프레임을 못읽었다면, break
            #     break
            frame = cv2.resize(frame, (640, 480)) # html에서 보일 이미지의 크기와 같도록 설정

            # 값 가져오기 (opacity->INT, bgr->TUPLE, hex->STR)
            lip_bgr = get_value("lip_bgr")
            # lip_hex = get_value("lip_hex")
            fd_bgr = get_value("fd_bgr")
            # fd_hex = get_value("fd_hex")
            lip_opacity = get_value("lip_opacity")
            fd_opacity = get_value("fd_opacity")
            isFDmakeup = get_value("isFDmakeup")
            isLIPmakeup = get_value("isLIPmakeup")

            # # 한 번에 모든 값과 타입 출력 (확인용)
            # print(
            #     f"fd_bgr: {isFDmakeup}, 타입: {type(isFDmakeup)} | "
            #     f"fd_opacity: {fd_opacity}, 타입: {type(fd_opacity)} | "
            #     f"fd_bgr: {fd_bgr}, 타입: {type(fd_bgr)} | "
            #     f"fd_hex: {fd_hex}, 타입: {type(fd_hex)} | "
            #     f"lip_bgr: {isLIPmakeup}, 타입: {type(isLIPmakeup)} | "
            #     f"lip_opacity: {lip_opacity}, 타입: {type(lip_opacity)} | "
            #     f"lip_bgr: {lip_bgr}, 타입: {type(lip_bgr)} | "
            #     f"lip_hex: {lip_hex}, 타입: {type(lip_hex)}"
            # )
            frame = makeup_instance.run(frame, isFDmakeup, isLIPmakeup, fd_bgr, lip_bgr, fd_opacity, lip_opacity)

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
        # cap.release()
        try:
            if websocket.client_state == "connected":  # 연결 상태 확인
                await websocket.close()
        except RuntimeError as e:
            print(f"WebSocket 종료 오류: {e}")
