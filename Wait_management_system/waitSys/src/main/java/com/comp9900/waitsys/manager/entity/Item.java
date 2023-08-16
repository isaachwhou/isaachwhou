package com.comp9900.waitsys.manager.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.util.Arrays;

/**
 * @author Wei Chen
 * Date:2023-06-24 19:59
 * Description: the entity of dish item
 */
@TableName("item")
public class Item implements Serializable{
    @TableId(type = IdType.AUTO)
    public Integer itemId;
    private String name;
    private byte[] picture;
    private String description;
    private String ingredient;
    private Float price;
    private Integer categoryId;
    private Float rating;
    private Integer isOnMenu;
    private Integer orderNum;

    public Item() {

    }

    public Item(Integer itemId, String name, byte[] picture, String description, String ingredient, Float price, Integer categoryId, Float rating, Integer isOnMenu, Integer orderNum) {
        this.itemId = itemId;
        this.name = name;
        this.picture = picture;
        this.description = description;
        this.ingredient = ingredient;
        this.price = price;
        this.categoryId = categoryId;
        this.rating = rating;
        this.isOnMenu = isOnMenu;
        this.orderNum = orderNum;
    }

    public Integer getItemId() {
        return itemId;
    }

    public void setItemId(Integer itemId) {
        this.itemId = itemId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public byte[] getPicture() {
        return picture;
    }

    public void setPicture(byte[] picture) {
        this.picture = picture;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getIngredient() {
        return ingredient;
    }

    public void setIngredient(String ingredient) {
        this.ingredient = ingredient;
    }

    public Float getPrice() {
        return price;
    }

    public void setPrice(Float price) {
        this.price = price;
    }

    public Integer getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(Integer categoryId) {
        this.categoryId = categoryId;
    }

    public Float getRating() {
        return rating;
    }

    public void setRating(Float rating) {
        this.rating = rating;
    }

    public Integer getIsOnMenu() {
        return isOnMenu;
    }

    public void setIsOnMenu(Integer IsOnMenu) {
        isOnMenu = IsOnMenu;
    }

    public Integer getOrderNum() {
        return orderNum;
    }

    public void setOrderNum(Integer orderNum) {
        this.orderNum = orderNum;
    }

    @Override
    public String toString() {
        return "Item{" +
                "itemId=" + itemId +
                ", name='" + name + '\'' +
                ", picture=" + Arrays.toString(picture) +
                ", description='" + description + '\'' +
                ", ingredient='" + ingredient + '\'' +
                ", price=" + price +
                ", categoryId=" + categoryId +
                ", rating=" + rating +
                ", isOnMenu=" + isOnMenu +
                ", orderNum=" + orderNum +
                '}';
    }
}

