package test.subserver;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class AppStartupRunner implements CommandLineRunner {

    private final PythonServer pythonServer;

    public AppStartupRunner(PythonServer pythonServer) {
        this.pythonServer = pythonServer;
    }

    @Override
    public void run(String... args) throws Exception {
        pythonServer.startPythonServer();
    }
}
