package com.comp9900.waitsys.manager.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import java.io.Serializable;
import java.util.Arrays;


/**
 * @author Weizhe Pan
 * @date 2023/6/26
 */
public class Category implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer categoryId;
    private String name;
    private Integer isOnMenu;
    private Integer orderNum;

    public Integer getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Integer categoryId) {
        this.categoryId = categoryId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getIsOnMenu() {
        return isOnMenu;
    }

    public void setIsOnMenu(Integer isOnMenu) {
        this.isOnMenu = isOnMenu;
    }

    public Integer getOrderNum() {
        return orderNum;
    }

    public void setOrderNum(Integer order) {
        this.orderNum = order;
    }

//    public category(Integer categoryId, String name, Integer isOnMenu, Integer order) {
//        this.categoryId = categoryId;
//        this.name = name;
//        this.isOnMenu = isOnMenu;
//        this.order = order;
//    }

    @Override
    public String toString() {
        return "Item{" +
                "categoryId=" + categoryId +
                ", name='" + name + '\'' +
                ", isOnMenu=" + isOnMenu +
                ", order=" + orderNum +
                '}';
    }

}
