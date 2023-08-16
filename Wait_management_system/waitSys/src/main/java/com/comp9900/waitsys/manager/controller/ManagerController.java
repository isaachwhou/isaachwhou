package com.comp9900.waitsys.manager.controller;


import com.baomidou.mybatisplus.core.metadata.IPage;
import com.comp9900.waitsys.manager.entity.VO.AnalysisVO;
import com.comp9900.waitsys.manager.entity.VO.ItemVO;
import com.comp9900.waitsys.manager.entity.VO.CategoryVO;
import com.comp9900.waitsys.manager.service.AnalysisService;
import com.comp9900.waitsys.manager.service.CategoryService;
import com.comp9900.waitsys.manager.service.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;

/**
 * @author Wei Chen
 * Date:2023-06-25 18:45
 * Description: the controller of manager
 */
@RestController
@RequestMapping("/waitsys/manager")
@CrossOrigin
public class ManagerController {
    @Autowired
    private ItemService itemService;
    @Autowired
    private CategoryService categoryService;

    @Autowired
    private AnalysisService analysisService;

    @PostMapping("/item/add")
    public boolean addItem(@RequestParam(value = "name") String name,
                           @RequestParam(value = "picture") MultipartFile picture,
                           @RequestParam(value = "description") String description,
                           @RequestParam(value = "ingredient") String ingredient,
                           @RequestParam(value = "price") float price,
                           @RequestParam(value = "categoryId") Integer categoryId) throws IOException {
        return itemService.addNewItem(name, picture, description, ingredient, price, categoryId);
    }

    @PostMapping("/item/edit")
    public boolean editItem(@RequestParam(value = "itemId") Integer itemId,
                              @RequestParam(value = "name") String name,
                              @RequestParam(value = "picture") MultipartFile picture,
                              @RequestParam(value = "description") String description,
                              @RequestParam(value = "ingredient") String ingredient,
                              @RequestParam(value = "price") float price,
                              @RequestParam(value = "categoryId") Integer categoryId) throws IOException {
        return itemService.updateItem(itemId, name, picture, description, ingredient, price, categoryId);
    }

    @GetMapping("/item/delete")
    public boolean deleteItem(@RequestParam(value = "itemId") Integer itemId) {
        return itemService.removeItem(itemId);
    }


    @GetMapping("/item/showById")
    public ItemVO showById(@RequestParam(value = "itemId") Integer itemId) {
        return itemService.showItemByItemId(itemId);
    }

    @PostMapping("/add_category")
    public boolean addCategory(@RequestParam(value = "name") String name){
        return categoryService.addCategory(name);
    }

    @PostMapping("/remove_category")
    public boolean removeCategory(@RequestParam(value = "id") Integer categoryId){
        return categoryService.removeCategory(categoryId);
    }

    @PostMapping("/change_category_order")
    public boolean changeCategoryOrder(@RequestBody HashMap<Integer, Integer> categoryMap){
        return categoryService.changeCategoryOrder(categoryMap);
    }

    @GetMapping("/item/showByCategory")
    public IPage<ItemVO> showByCategory(@RequestParam(value = "categoryId") Integer categoryId,
                                        @RequestParam(value = "pageNo") Integer pageNo,
                                        @RequestParam(value = "pageSize") Integer pageSize) {
        return itemService.showItemByCategory(categoryId, pageNo, pageSize);
    }

    @GetMapping("/item/showListByCategory")
    public List<ItemVO> showListByCategory(@RequestParam(value = "categoryId") Integer categoryId) {
        return itemService.showItemListByCategory(categoryId);
    }

    @GetMapping("/item/showTop5")
    public List<ItemVO> showTop5() {
        return itemService.showTop5Item();
    }

    @GetMapping("/item/showTopSale5")
    public List<ItemVO> showTopSale5() {
        return itemService.showTop5SaleItems();
    }

    @PostMapping("/item/changeOrder")
    public boolean changeOrder(@RequestBody HashMap<Integer, Integer> itemMap) {
        return itemService.changeItemOrderNum(itemMap);
    }

    @GetMapping("/item/showAll")
    public IPage<ItemVO> showAll(@RequestParam(value = "pageNo") Integer pageNo,
                                 @RequestParam(value = "pageSize") Integer pageSize) {
        return itemService.showAllItem(pageNo, pageSize);
    }

    @GetMapping("/item/showAllList")
    public List<ItemVO> showAllList() {
        return itemService.showAllItemList();
    }

    @GetMapping("/list_all_categories")
    public List<CategoryVO> listAllCategories(){
        return categoryService.listAllCategories();
    }

    @GetMapping("/analysis")
    public AnalysisVO analyse(@RequestParam (value = "state")Integer state,
                              @RequestParam (value = "x")Integer x){
        return analysisService.Analyse(state,x);
    }
}
