package com.comp9900.waitsys.manager.entity.VO;

import com.comp9900.waitsys.manager.entity.Item;

import java.util.Objects;

/**
 * @author Wei Chen
 * Date:2023-06-25 23:00
 * Description: the entity of dish item and category
 */
public class ItemVO extends Item {
    private String category;

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public ItemVO() {

    }

    public ItemVO(Integer itemId, String name, byte[] picture, String description, String ingredient, Float price, Integer categoryId, Float rating, Integer isOnMenu, Integer orderNum, String category) {
        super(itemId, name, picture, description, ingredient, price, categoryId, rating, isOnMenu, orderNum);
        this.category = category;
    }

    @Override
    public String toString() {
        return "ItemVO{" +
                "itemId='" + itemId + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ItemVO itemVO = (ItemVO) o;
        return Objects.equals(itemId, itemVO.itemId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(itemId);
    }
}
