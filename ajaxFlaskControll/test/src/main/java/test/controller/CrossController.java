package test.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;

@RestController
@CrossOrigin(origins = "http://localhost:8080") // Flask의 출처 허용
public class CrossController {

    @PostMapping("/api/slider")
    public ResponseEntity<String> getSliderData() {
        System.out.println("슬라이더 데이터 전송");
        return ResponseEntity.ok("슬라이더 데이터");
    }

}
