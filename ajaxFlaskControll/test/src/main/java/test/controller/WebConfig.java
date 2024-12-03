package test.controller;

import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(@SuppressWarnings("null") CorsRegistry registry) {
        // registry.addMapping("/api/**") // 모든 /api/** 경로에 대해
        registry.addMapping("/**") // 모든 /api/** 경로에 대해
                .allowedOrigins("http://localhost:8080") // Flask의 출처
                .allowedMethods("GET", "POST", "OPTIONS"); // 허용할 메서드
    }

}
