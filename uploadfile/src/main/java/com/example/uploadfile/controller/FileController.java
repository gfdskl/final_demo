package com.example.uploadfile.controller;

import org.apache.catalina.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;


@RestController
public class FileController{
        private static final Logger logger = LoggerFactory.getLogger(FileController.class);

        @PostMapping("/upload")
        public void upload(@RequestParam("file") MultipartFile file) {
                if(file.isEmpty()){
                        //return ;
                }
                String fileName = "test01.mp4";
                String filepath =  "/home/ping501f/member/G3/final_demo/";
                File dest = new File(filepath + fileName);
                try {
                        file.transferTo(dest);
                        logger.info("上传成功");
                      //return ;
                }catch(IOException e){
                        logger.error("上传失败");
                        e.printStackTrace();
                }
               //return ;
        }

        @GetMapping("/form")
        //@ResponseBody
        public String upForm(@RequestParam("text1") String text1,
                             @RequestParam("text2") String text2,
                             @RequestParam("text3") String text3,
                             @RequestParam("text4") String text4) throws IOException, InterruptedException {
                String coordinate = text1 + "," +text2 + "," + text3 + "," + text4;
                String path = "/home/ping501f/member/G3/final_demo/test01.mp4";
//                try {
                        //需传入的参数
                        //设置命令行传入参数
                        String[] args = new String[] { "bash", "/home/ping501f/member/G3/final_demo/run.sh", path, coordinate};
                        Process pr = Runtime.getRuntime().exec(args);
                        BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
                        String line = null;
                        while ((line = in.readLine()) != null) {
                                System.out.println(line);
                        }
                        in.close();
                        pr.waitFor();
                        String url = "gen_video.mp4";
                        return url;
//                } catch (Exception e) {
//                        e.printStackTrace();
//                }

        }
}