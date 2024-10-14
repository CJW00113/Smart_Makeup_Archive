package test.controller;

// import java.io.IOException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

import test.fastAPI.PythonRunner;

import org.springframework.boot.CommandLineRunner;

@SpringBootApplication
@ComponentScan("test.fastAPI")
public class TestApplication implements CommandLineRunner {
	// public class TestApplication {
	private final PythonRunner pythonRunner;

	public TestApplication(PythonRunner pythonRunner) {
		this.pythonRunner = pythonRunner; // 여기에서 초기화
	}

	public static void main(String[] args) {
		SpringApplication.run(TestApplication.class, args);
	}

	@Override
	public void run(String... args) {
		startPython(8080); // 실행할 포트 설정
	}

	private void startPython(int port) {
		pythonRunner.startPythonServer(port);
	}

}