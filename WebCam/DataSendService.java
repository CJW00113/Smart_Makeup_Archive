package com.smwhc.smart_makeup_web.WebCam;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class DataSendService {
    private static String fastApiPort = "http://127.0.0.1:8080";

    public void sendPostSignal(String postURL) {
        String fastApiURL = fastApiPort + postURL; // 전송할 URL 정의
        RestTemplate restTemplate = new RestTemplate(); // RESTful에 사용할 객체 정의
        // 통신을 위해, JSON형태로 변환
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        // 빈 요청 객체 생성 (본문 없이 보내기)
        HttpEntity<Void> requestEntity = new HttpEntity<>(headers);
        // 요청 로그 출력
        System.out.println("전송 경로: " + postURL + ", Sending POST request");

        try {
            // POST 요청 전송
            ResponseEntity<Void> response = restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity, Void.class);
            // 응답 상태 로그 출력
            System.out.println("응답 상태: " + response.getStatusCode());
        } catch (RestClientException e) {
            // 예외 로그 출력
            System.err.println("POST 요청 예외 로그 출력: " + e.getMessage());
        }
    }

    // str 보내기
    public void sendStringVariable(String requestValue, String PostURL) {
        String fastApiURL = fastApiPort + PostURL; // 전송할 URL 정의

        RestTemplate restTemplate = new RestTemplate(); // RESTful에 사용할 객체 정의
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        // 통신을 위해, JSON형태로 변환
        // JSON 형태로 데이터 객체 생성
        Map<String, String> requestData = new HashMap<>();
        requestData.put("hex", requestValue);

        // YourDataObject 형태로 데이터 객체 생성
        HttpEntity<Map<String, String>> requestEntity = new HttpEntity<>(requestData, headers);

        try {
            ResponseEntity<Void> response = restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity, Void.class);
            System.out.println("응답 상태: " + response.getStatusCode());
        } catch (RestClientException e) {
            System.err.println("POST 요청 예외 로그 출력: " + e.getMessage());
        }
    }

    // int 보내기
    public void sendIntVariable(Integer opacityValue, String postURL) {
        String fastApiURL = fastApiPort + postURL;

        RestTemplate restTemplate = new RestTemplate();

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // JSON 형태로 데이터 객체 생성
        Map<String, Integer> requestData = new HashMap<>();
        requestData.put("opacity", opacityValue);

        HttpEntity<Map<String, Integer>> requestEntity = new HttpEntity<>(requestData, headers);

        try {
            ResponseEntity<Void> response = restTemplate.exchange(fastApiURL, HttpMethod.POST, requestEntity, Void.class);
            System.out.println("응답 상태: " + response.getStatusCode());
        } catch (RestClientException e) {
            System.err.println("POST 요청 예외 로그 출력: " + e.getMessage());
        }
    }
}
