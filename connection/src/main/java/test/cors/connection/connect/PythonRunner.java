package test.cors.connection.connect;

import java.io.BufferedReader;
import java.io.IOException;
// import java.io.InputStreamReader;
// import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.springframework.stereotype.Component;

@Component
public class PythonRunner {
    private Process process;

    public void startPythonServer(int port) {
        try {
            // 서버가 실행 이전에 실행된 PID를 종료함
            deletePID(port);
            // 이미 실행 중인 FastAPI 서버가 있다면 종료합니다.
            if (process != null && process.isAlive()) {
                process.destroy();
                process.waitFor(); // 프로세스가 완전히 종료될 때까지 대기
                System.out.println("Existing FastAPI server has been terminated.");
            }

            ProcessBuilder builder = new ProcessBuilder("python",
                    "src\\main\\java\\test\\cors\\connection\\connect\\testFastAPI.py",
                    String.valueOf(port));
            builder.redirectErrorStream(true);
            process = builder.start();

            // // // 프로세스 출력 확인 부분이 필요할까?? 몰루??
            // // 프로세스 출력 확인
            // BufferedReader reader = new BufferedReader(new
            // InputStreamReader(process.getInputStream()));
            // String line;
            // while ((line = reader.readLine()) != null) {
            // System.out.println(line);

            // // 특정 로그 메시지를 확인할 수 있습니다.
            // if (line.contains("Starting FastAPI server")) { // FastAPI 로그 메시지에 맞게 수정
            // System.out.println("FastAPI server is running successfully!");
            // }
            // }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    // public void startPythonServer(int port) {
    // try {
    // ProcessBuilder builder = new ProcessBuilder("python",
    // "src\\main\\java\\test\\cors\\connection\\connect\\testFastAPI.py");
    // // // 이거 아마 uvicorn가 아니라 cmd였으면 됬으듯함
    // ssBuilder builder = new ProcessBuilder("uvicorn",
    // // rs.connection.connect.testFastAPI:app",
    // // , "127.0.0.1",
    // // , String.valueOf(port),
    // // d");
    // // builder.environment().put("PYTHONPATH",
    // "src\\main\\java\\test\\cors\\connection\\connect");
    // process = builder.start();
    //

    // // 프로세스 출력 확인
    // BufferedReader reader = new BufferedReader(new
    // InputStreamReader(process.getInputStream()));
    // String line;
    //
    // while ((line = reader.readLine()) != null) {
    // System.out.println(line);

    // // 특정 로그 메시지를 확인할 수 있습니다.
    // if (line.contains("Starting Flask server")) {
    // System.out.println("Flask server is running successfully!");
    //

    // }
    // tch (IOException e) {
    // e.printStackTrace();
    //

    // }
    private static void deletePID(int port) {
        try {
            String pid = getRunningProcessPidByPort(port);
            if (pid != null) {
                terminateProcess(pid);
                System.out.println("PID: " + pid + "종료 완료");
            } else {
                System.out.println("No Python process found.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 입력한 포트에서 실행 중인 Python 프로세스의 PID를 반환하는 함수
    private static String getRunningProcessPidByPort(int port) {
        String pid = null;
        try {
            // 포트를 매개변수로 받아서 명령어 생성
            String command = String.format("netstat -ano | findstr :%d", port);
            ProcessBuilder processBuilder = new ProcessBuilder("cmd", "/c", command);
            Process PIDprocess = processBuilder.start();

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(PIDprocess.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    // PID는 마지막 열에 있다.
                    String[] parts = line.trim().split("\\s+");
                    pid = parts[parts.length - 1]; // PID는 마지막 열에 있다.
                    System.out.println(port + " 포트를 사용하는 PID: " + pid);
                    break; // 첫 번째 발견된 PID만 사용
                }
            }
        } catch (Exception e) {
            System.err.println("PID 검색 중 오류 발생: " + e.getMessage());
            e.printStackTrace();
        }
        return pid;
    }

    // 주어진 PID를 가진 프로세스를 종료하는 함수
    private static void terminateProcess(String pid) {
        try {
            ProcessBuilder killProcessBuilder = new ProcessBuilder("cmd", "/c", "taskkill /PID " + pid + " /F");
            killProcessBuilder.start();
            System.out.println("Terminated Python process with PID: " + pid);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
