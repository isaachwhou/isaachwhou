package com.comp9900.waitsys.manager.service;


import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.manager.entity.Category;
import com.comp9900.waitsys.manager.entity.VO.CategoryVO;

import java.util.HashMap;
import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/6/27
 */
public interface CategoryService extends IService<Category> {
    /**
    * @Description: list all categories on menu
    * @Param: []
    * @return: java.util.List<com.comp9900.waitsys.manager.entity.VO.CategoryVO>
    * @Author: Weizhe Pan
    * @Date: 2023/6/27
    */
    List<CategoryVO> listAllCategories();
    
    /**
    * @Description: add a new category
    * @Param: [categoryName]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/6/27
    */
    boolean addCategory(String categoryName);

    /**
    * @Description: remove a category
    * @Param: [categoryId]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/6/27
    */
    boolean removeCategory(Integer categoryId);


    /**
    * @Description: 
    * @Param: [categoryMap]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/6/27
    */
    boolean changeCategoryOrder(HashMap<Integer, Integer> categoryMap);
}
