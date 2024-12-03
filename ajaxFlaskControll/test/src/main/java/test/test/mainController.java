package test.test;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class mainController {
    @GetMapping({ "/", "/index" })
    public String index() {
        return "index";
    }

}
