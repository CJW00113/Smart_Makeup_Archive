package test.test;

import java.io.IOException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TestApplication {

	private static Process flaskProcess; // 프로세스를 클래스 변수로 선언

	public static void main(String[] args) {
		startFlaskServer(); // Flask 서버를 시작
		SpringApplication.run(TestApplication.class, args);
	}

	public static void startFlaskServer() {
		// Flask 서버를 별도의 스레드에서 실행
		new Thread(() -> {
			try {
				ProcessBuilder processBuilder = new ProcessBuilder("python",
						"test\\src\\main\\java\\test\\flask\\start_flask.py");
				processBuilder.inheritIO(); // 콘솔에 Flask 서버의 출력을 표시
				flaskProcess = processBuilder.start(); // 프로세스를 클래스 변수에 저장
				flaskProcess.waitFor(); // Flask 서버가 종료될 때까지 대기
			} catch (IOException | InterruptedException e) {
				e.printStackTrace();
			}
		}).start(); // Flask 서버를 별도의 스레드에서 실행
	}

}