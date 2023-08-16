package com.comp9900.waitsys.customer.entity;

import java.util.Arrays;

/**
 * @author Wei Chen
 * Date:2023-07-11 17:29
 * Description: the DTO of orderItem
 */

//@TableName(value = "Order_item")

/**
 * @author Wei Chen
 * Date:2023-07-11 17:29
 * Description: the DTO of orderItem
 */
public class OrderItemDTO extends OrderItem{
    private String itemName;

    private byte[] itemPicture;

    private Float price;

    //@TableField(value = "count(*)", insertStrategy = FieldStrategy.NEVER, updateStrategy = FieldStrategy.NEVER)
    //private Integer count;

    public OrderItemDTO() {
    }

    public OrderItemDTO(Integer id, Integer orderId, Integer tableId, Integer itemId, Integer isCook, Integer isServe, Float rating, String itemName, byte[] itemPicture, Float price) {
        super(id, orderId, tableId, itemId, isCook, isServe, rating);
        this.itemName = itemName;
        this.itemPicture = itemPicture;
        this.price = price;
        //this.count = count;
    }

    public String getItemName() {
        return itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public byte[] getItemPicture() {
        return itemPicture;
    }

    public void setItemPicture(byte[] itemPicture) {
        this.itemPicture = itemPicture;
    }

    public Float getPrice() {
        return price;
    }

    public void setPrice(Float price) {
        this.price = price;
    }

//    public Integer getCount() {
//        return count;
//    }
//
//    public void setCount(Integer count) {
//        this.count = count;
//    }

    @Override
    public String toString() {
        return "OrderItemVO{" +
                "itemName='" + itemName + '\'' +
                ", itemPicture=" + Arrays.toString(itemPicture) +
                ", price=" + price +
                //", count=" + count +
                '}';
    }
}
