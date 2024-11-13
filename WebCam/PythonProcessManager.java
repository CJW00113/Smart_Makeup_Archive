package com.smwhc.smart_makeup_web.WebCam;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class PythonProcessManager {

    public void deletePID() {
        try {
            String pid;
            while (true) {
                pid = getRunningPythonProcessPid();
                if (pid != null) {
                    terminateProcess(pid);
                    System.out.println("PID: " + pid + " 종료 완료");
                } else {
                    System.out.println("No Python process found.");
                    break; // pid가 null이면 반복 종료
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }

    // 실행 중인 Python 프로세스의 PID를 반환하는 함수
    private static String getRunningPythonProcessPid() {
        String pid = null;
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("cmd", "/c", "tasklist | findstr python");
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.trim().split("\\s+");
                pid = parts[1]; // PID는 일반적으로 두 번째 열에 있다.
                System.out.println("Found Python PID: " + pid);
                break; // 첫 번째 발견된 PID만 사용
            }
        } catch (Exception e) {
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
