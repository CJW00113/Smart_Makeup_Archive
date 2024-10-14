package test.cors.connection.connect;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Component;

@Component
public class PythonRunner {
    private Process process;

    public void startPythonServer(int port) {

        try {
            // 이미 실행 중인 FastAPI 서버가 있다면 종료합니다.
            if (process != null && process.isAlive()) {
                process.destroy();
                process.waitFor(); // 프로세스가 완전히 종료될 때까지 대기
                System.out.println("Existing FastAPI server has been terminated.");
            }

            //
            ProcessBuilder builder = new ProcessBuilder("python", "src\\main\\java\\test\\cors\\connection\\connect\\testFastAPI.py",
                    String.valueOf(port));
            builder.redirectErrorStream(true);
            process = builder.start();

            // 프로세스 출력 확인
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);

                // 특정 로그 메시지를 확인할 수 있습니다.
                if (line.contains("Starting FastAPI server")) { // FastAPI 로그 메시지에 맞게 수정
                    System.out.println("FastAPI server is running successfully!");
                }
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    // public void startPythonServer(int port) {
    // try {
    // ProcessBuilder builder = new ProcessBuilder("python",
    // "src\\main\\java\\test\\cors\\connection\\connect\\testFastAPI.py");
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
}
