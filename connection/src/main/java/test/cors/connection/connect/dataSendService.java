package test.cors.connection.connect;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import lombok.Getter;
import lombok.Setter;

@Service
public class dataSendService {

    private static String fastApiPort = "http://127.0.0.1:8080";

    // POST 신호만 보낼 때
    public static void sendPostSignal(String postURL) {
        String fastApiURL = fastApiPort + postURL; // 전송할 URL 정의

        RestTemplate restTemplate = new RestTemplate(); // RESTful에 사용할 객체 정의

        // 통신을 위해, JSON형태로 변환
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 빈 요청 객체 생성 (본문 없이 보내기)
        HttpEntity<Void> requestEntity = new HttpEntity<>(headers);

        // 요청 로그 출력
        System.out.println("전송 경로: " + postURL + ", Sending POST request");

        // POST 요청 전송
        restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity, Void.class);
    }

    // str 보내기
    public static void sendStringVariable(String requestValue, String PostURL) {
        String fastApiURL = fastApiPort + PostURL; // 전송할 URL 정의

        RestTemplate restTemplate = new RestTemplate(); // RESTful에 사용할 객체 정의

        // 통신을 위해, JSON형태로 변환
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // YourDataObject 형태로 데이터 객체 생성
        SendStringDataObject dataObject = new SendStringDataObject();
        dataObject.setHex(requestValue);
        HttpEntity<SendStringDataObject> requestEntity = new HttpEntity<>(dataObject,
                headers);

        // 요청 로그 출력
        System.out.println("전송 경로: " + PostURL + ", Sending request: " +
                dataObject.getHex() + " String 형");

        restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity,
                Void.class);

    }

    // int 보내기
    public static void sendIntVariable(String requestValue, String PostURL) {
        String fastApiURL = fastApiPort + PostURL; // 전송할 URL 정의

        RestTemplate restTemplate = new RestTemplate(); // RESTful에 사용할 객체 정의

        // Int형으로 변환
        int requestIntValue = convertStringToInt(requestValue);

        // 통신을 위해, JSON형태로 변환
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // YourDataObject 형태로 데이터 객체 생성
        SendIntDataObject dataObject = new SendIntDataObject();
        dataObject.setOpacity(requestIntValue);
        HttpEntity<SendIntDataObject> requestEntity = new HttpEntity<>(dataObject, headers);

        // 요청 로그 출력
        System.out.println("전송 경로: " + PostURL + ", Sending request: " + dataObject.getOpacity() + " int 형");

        restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity, Void.class);
    }

    // String을 int로 변환하는 메서드
    public static int convertStringToInt(String numberString) {
        try {
            return Integer.parseInt(numberString);
        } catch (NumberFormatException e) {
            System.out.println("유효하지 않은 정수 형식입니다: " + numberString);
            return 0; // 또는 다른 에러 코드나 예외 처리를 할 수 있습니다.
        }
    }

    // 서버 간 통신을 위해 전송값을 json으로 변할 때만 쓰임..
    @Getter
    @Setter
    public static class SendIntDataObject {
        private int opacity;
    }

    @Getter
    @Setter
    public static class SendStringDataObject {
        private String hex;
    }

}
