package com.comp9900.waitsys;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan({"com.comp9900.waitsys.manager.mapper", "com.comp9900.waitsys.customer.mapper", "com.comp9900.waitsys.waitStaff.mapper", "com.comp9900.waitsys.kitchenStaff.mapper"})
public class WaitSysApplication {

    public static void main(String[] args) {

        SpringApplication.run(WaitSysApplication.class, args);
    }

}
