import cv2

# 웹캠 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if ret:
        # 원본 해상도
        original_height, original_width = frame.shape[:2]

        # 슬라이스할 크기
        slice_width = 320
        slice_height = 360

        # 중앙 좌표 계산
        center_x = original_width // 2
        center_y = original_height // 2

        # 슬라이스할 영역 계산
        x1 = center_x - (slice_width // 2)
        x2 = center_x + (slice_width // 2)
        y1 = center_y - (slice_height // 2)
        y2 = center_y + (slice_height // 2)

        # 이미지 슬라이스
        sliced_frame = frame[y1:y2, x1:x2]
        
        # 슬라이스된 이미지를 2배로 리사이즈
        resized_frame = cv2.resize(sliced_frame, (slice_width * 2, slice_height * 2))

        # 슬라이스된 이미지와 리사이즈된 이미지 보여주기
        cv2.imshow('Sliced Frame', sliced_frame)
        cv2.imshow('Resized Frame', resized_frame)

        # 원본 이미지 보여주기 (선택 사항)
        cv2.imshow('Original Frame', frame)

        # 키 입력을 기다림
        cv2.waitKey(0)

    else:
        print("프레임을 읽을 수 없습니다.")

# 자원 해제
cap.release()
cv2.destroyAllWindows()