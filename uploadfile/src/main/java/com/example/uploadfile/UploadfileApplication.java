package com.example.uploadfile;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.GetMapping;


@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class UploadfileApplication {

        public static void main(String[] args) {
                SpringApplication.run(UploadfileApplication.class, args);
        }

}
