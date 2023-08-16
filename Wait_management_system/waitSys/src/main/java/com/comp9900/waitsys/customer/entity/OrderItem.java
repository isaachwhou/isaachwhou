package com.comp9900.waitsys.customer.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;

/**
 * @author Wei Chen
 * Date:2023-07-11 17:29
 * Description: the entity of orderItem
 */

@TableName("order_item")
public class OrderItem implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer id;

    private Integer orderId;

    private Integer tableId;

    private Integer itemId;

    private Integer isCook;

    private Integer isServe;

    private Float rating;

    public OrderItem() {
    }

    public OrderItem(Integer id, Integer orderId, Integer tableId, Integer itemId, Integer isCook, Integer isServe, Float rating) {
        this.id = id;
        this.orderId = orderId;
        this.tableId = tableId;
        this.itemId = itemId;
        this.isCook = isCook;
        this.isServe = isServe;
        this.rating = rating;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getOrderId() {
        return orderId;
    }

    public void setOrderId(Integer orderId) {
        this.orderId = orderId;
    }

    public Integer getTableId() {
        return tableId;
    }

    public void setTableId(Integer tableId) {
        this.tableId = tableId;
    }

    public Integer getItemId() {
        return itemId;
    }

    public void setItemId(Integer itemId) {
        this.itemId = itemId;
    }

    public Integer getIsCook() {
        return isCook;
    }

    public void setIsCook(Integer isCook) {
        this.isCook = isCook;
    }

    public Integer getIsServe() {
        return isServe;
    }

    public void setIsServe(Integer isServe) {
        this.isServe = isServe;
    }

    public Float getRating() {
        return rating;
    }

    public void setRating(Float rating) {
        this.rating = rating;
    }

    @Override
    public String toString() {
        return "OrderItem{" +
                "id=" + id +
                ", orderId=" + orderId +
                ", tableId=" + tableId +
                ", itemId=" + itemId +
                ", isCook=" + isCook +
                ", isServe=" + isServe +
                ", rating=" + rating +
                '}';
    }
}
