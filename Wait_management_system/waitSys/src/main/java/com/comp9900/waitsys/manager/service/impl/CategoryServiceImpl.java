package com.comp9900.waitsys.manager.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.comp9900.waitsys.constant.Constant;
import com.comp9900.waitsys.manager.entity.Category;
import com.comp9900.waitsys.manager.entity.VO.CategoryVO;
import com.comp9900.waitsys.manager.mapper.CategoryMapper;
import com.comp9900.waitsys.manager.service.CategoryService;
import com.github.yulichang.base.MPJBaseServiceImpl;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;


import static com.comp9900.waitsys.constant.Constant.FALSE_VALUE;
import static com.comp9900.waitsys.constant.Constant.TRUE_VALUE;

/**
 * @author Weizhe Pan
 * @date 2023/6/27
 * @description the category service implementation of manager
 */
@Service
public class CategoryServiceImpl extends MPJBaseServiceImpl<CategoryMapper, Category> implements CategoryService {
    @Autowired
    private CategoryMapper categoryMapper;


    @Override
    public List<CategoryVO> listAllCategories() {

        MPJLambdaWrapper<Category> myWrapper = new MPJLambdaWrapper<>();
        myWrapper
                .eq(Category::getIsOnMenu, TRUE_VALUE)
                .selectAs(Category::getCategoryId,"id")
                .selectAs(Category::getName,"name")
                .selectAs(Category::getOrderNum,"orderNum")
                .orderByAsc(Category::getOrderNum);

        return categoryMapper.selectJoinList(CategoryVO.class,myWrapper);
    }

    @Override
    public boolean addCategory(String categoryName) {
        Category category=new Category();
        category.setName(categoryName);
        category.setIsOnMenu(TRUE_VALUE);
        category.setOrderNum((int) count() + 1);
        return this.save(category);
    }

    @Override
    public boolean removeCategory(Integer categoryId) {
        Category category=this.getById(categoryId);
        category.setIsOnMenu(FALSE_VALUE);
        return updateById(category);
    }

    @Override
    public boolean changeCategoryOrder(HashMap<Integer, Integer> categoryMap) {
        int count = 0;
        for (int i : categoryMap.keySet()) {
            Category category = getById(i);
            category.setOrderNum(categoryMap.get(i));
            if (updateById(category)) {
                count++;
            }
        }
        return count == categoryMap.size();
    }


}
