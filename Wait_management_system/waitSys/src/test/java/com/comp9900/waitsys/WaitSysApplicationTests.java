package com.comp9900.waitsys;

import com.comp9900.waitsys.manager.entity.Item;
import com.comp9900.waitsys.manager.mapper.ItemMapper;
import com.comp9900.waitsys.manager.service.CategoryService;
import com.comp9900.waitsys.manager.service.ItemService;
import org.apache.tomcat.util.http.fileupload.disk.DiskFileItem;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

@SpringBootTest
class WaitSysApplicationTests {

    @Autowired
    private ItemMapper itemMapper;

    @Autowired
    private ItemService itemService;
    private CategoryService categoryService;

    @Test
    public void testSelect() {
        System.out.println(("----- selectAll method test ------"));
        List<Item> itemList = itemMapper.selectList(null);
        System.out.println(itemList.get(1));
    }

    @Test
    public void testAddNewItem() throws IOException {
        File file = new File("/Users/vallen/IntelliJIDEA/waitSys/src/main/database/ERD.png");
        FileInputStream input = new FileInputStream(file);
        MultipartFile picture = new MockMultipartFile("file",
                file.getName(), "image/png", input);
        boolean flag = itemService.addNewItem("test picture null", picture, null, null, 20.8f, 2);
        System.out.println("The flag = " + flag);
    }

    @Test
    public void testAddNewCategory(){
        boolean flag = categoryService.addCategory("drinks");
        System.out.println("The flag = " + flag);
    }
}
