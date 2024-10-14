package test.cors.connection.controller;

import org.springframework.web.bind.annotation.CrossOrigin;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import lombok.Getter;
import lombok.Setter;
import test.cors.connection.connect.PythonRunner;
import test.cors.connection.connect.dataSendService;

@CrossOrigin(origins = "http://localhost:8080")
@Controller
public class mainController {

    private PythonRunner pythonRunner = new PythonRunner();
    private boolean pythonServerRunning = false;

    // Fast API 러너 초기화
    public mainController(PythonRunner pythonRunner) {
        this.pythonRunner = pythonRunner;
    }

    public void setPythonServerRunning(boolean isPythonServerRunning) {
        this.pythonServerRunning = isPythonServerRunning;
    }

    @GetMapping("/makeup")
    public String getMakeupPage() {
        int port = 8080; // 포트설정

        // Fast API가 실행중이 아닌경우 서버 실행
        if (!pythonServerRunning) {
            setPythonServerRunning(true);
            pythonRunner.startPythonServer(port);
            System.out.println("Python 서버가 시작되었습니다!");
            return "makeup";// templates/makeup.html을 반환
        } else {
            System.out.println("Python 서버는 이미 실행 중입니다!");
            return "makeup";// templates/makeup.html을 반환
        }
    }

    // // 아직안씀
    // @GetMapping("/check")
    // public String checkServer() {
    // return pythonServerRunning ? "서버가 실행 중입니다." : "서버가 실행되고 있지 않습니다.";
    // }

    @PostMapping("/shutdown") // 서버 종료를 위한 경로
    public String shutdownServer() {
        if (pythonServerRunning) {
            setPythonServerRunning(false);
            System.out.println("Python 서버가 종료되었습니다!");
            dataSendService.sendPostSignal("/shutdown");
        } else {
            System.out.println("Python 서버는 실행되고 있지 않습니다.");
        }
        return "makeup";
    }

    // // 모든 다른 경로 요청을 처리하는 메서드
    // @GetMapping("/**")
    // public String handleOtherRequests() {
    // // 서버를 종료하고 싶지 않은 경우 다른 경로 요청에 대한 응답
    // return "유효하지 않은 경로입니다. /makeup 또는 /makeup/shutdown을 사용하세요.";
    // }

    // Post 요청
    @PostMapping("/slider")
    public String getSliderValue(@RequestBody SliderValue sliderValue) {
        dataSendService.sendIntVariable(sliderValue.getOpacity(), "/slider");
        System.out.println("Received slider value: " + sliderValue.getOpacity());
        return "makeup";
    }

    // Post 요청
    @PostMapping("/btnColor")
    public String getBtnColor(@RequestBody BtnValue btnValue) {
        dataSendService.sendStringVariable(btnValue.getHex(), "/btnColor");
        System.out.println("Received btnColor : " + btnValue.getHex());
        return "makeup";
    }

    @Getter
    @Setter
    public static class SliderValue {
        private String opacity;
    }

    @Getter
    @Setter
    public static class BtnValue {
        private String hex;
    }
}