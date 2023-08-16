package com.comp9900.waitsys.customer.entity;

import java.util.Arrays;

/**
 * @author Wei Chen
 * Date:2023-07-11 17:29
 * Description: the VO of orderItem
 */

public class OrderItemVO {

    private Integer itemId;

    private byte[] itemPicture;

    private String itemName;

    private Integer itemNumber;

    private Float totalPrice;

    public OrderItemVO(Integer itemId, byte[] itemPicture, String itemName, Integer itemNumber, Float totalPrice) {
        this.itemId = itemId;
        this.itemPicture = itemPicture;
        this.itemName = itemName;
        this.itemNumber = itemNumber;
        this.totalPrice = totalPrice;
    }

    public OrderItemVO() {
    }

    public byte[] getItemPicture() {
        return itemPicture;
    }

    public void setItemPicture(byte[] itemPicture) {
        this.itemPicture = itemPicture;
    }

    public String getItemName() {
        return itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public Integer getItemNumber() {
        return itemNumber;
    }

    public void setItemNumber(Integer itemNumber) {
        this.itemNumber = itemNumber;
    }

    public Float getTotalPrice() {
        return totalPrice;
    }

    public void setTotalPrice(Float totalPrice) {
        this.totalPrice = totalPrice;
    }

    public Integer getItemId() {
        return itemId;
    }

    public void setItemId(Integer itemId) {
        this.itemId = itemId;
    }

    @Override
    public String toString() {
        return "OrderItemVO{" +
                "itemId=" + itemId +
                ", itemPicture=" + Arrays.toString(itemPicture) +
                ", itemName='" + itemName + '\'' +
                ", itemNumber=" + itemNumber +
                ", totalPrice=" + totalPrice +
                '}';
    }
}
