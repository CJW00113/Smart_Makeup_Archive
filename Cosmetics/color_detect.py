import cv2

# 마우스 클릭 이벤트를 처리하는 콜백 함수
def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 좌클릭일 경우
        # 클릭한 위치의 픽셀 색상 값 가져오기
        b, g, r = image[y, x]
        # RGB 값 출력
        print(f'RGB: ({r}, {g}, {b})')
        # BGR 값 출력
        print(f'BGR: ({b}, {g}, {r})')
        # HEX 값 변환
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        print(f'HEX: {hex_color} \n')

# 이미지 로드
image = cv2.imread('color_img.PNG')  # 이미지 파일 경로 변경

# 윈도우 생성
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', get_color)

while True:
    cv2.imshow('Image', image)
    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 윈도우 종료
cv2.destroyAllWindows()
