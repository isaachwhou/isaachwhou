package com.comp9900.waitsys.customer.entity;

import java.util.HashMap;
import java.util.List;

/**
 * @author Wei Chen
 * Date:2023-07-20 13:45
 * Description: the DTO of rating
 */
public class ItemRatingDTO {
    private Integer tableId;
    private List<Integer> orderIds;
    private HashMap<Integer, Float> itemRatings;

    public Integer getTableId() {
        return tableId;
    }

    public void setTableId(Integer tableId) {
        this.tableId = tableId;
    }

    public List<Integer> getOrderIds() {
        return orderIds;
    }

    public void setOrderIds(List<Integer> orderIds) {
        this.orderIds = orderIds;
    }

    public HashMap<Integer, Float> getItemRatings() {
        return itemRatings;
    }

    public void setItemRatings(HashMap<Integer, Float> itemRatings) {
        this.itemRatings = itemRatings;
    }

    public ItemRatingDTO(Integer tableId, List<Integer> orderIds, HashMap<Integer, Float> itemRatings) {
        this.tableId = tableId;
        this.orderIds = orderIds;
        this.itemRatings = itemRatings;
    }

    public ItemRatingDTO() {
    }

    @Override
    public String toString() {
        return "ItemRatingDTO{" +
                "tableId=" + tableId +
                ", orderIds=" + orderIds +
                ", itemRatings=" + itemRatings +
                '}';
    }
}
