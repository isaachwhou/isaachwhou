package com.comp9900.waitsys.customer.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.sql.Timestamp;


/**
 * @author Wei Chen
 * Date:2023-07-08 20:22
 * Description: the entity of Orders
 */
@TableName("orders")
public class Order implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer orderId;

    private Integer tableId;

    private Timestamp startTime;

    private Float cost;

    private Integer isComplete;

    private Integer isCook;

    public Order(Integer orderId, Integer tableId, Timestamp startTime, Float cost, Integer isComplete, Integer isCook) {
        this.orderId = orderId;
        this.tableId = tableId;
        this.startTime = startTime;
        this.cost = cost;
        this.isComplete = isComplete;
        this.isCook = isCook;
    }

    public Order() {
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

    public Timestamp getStartTime() {
        return startTime;
    }

    public void setStartTime(Timestamp startTime) {
        this.startTime = startTime;
    }

    public Float getCost() {
        return cost;
    }

    public void setCost(Float cost) {
        this.cost = cost;
    }

    public Integer getIsComplete() {
        return isComplete;
    }

    public void setIsComplete(Integer isComplete) {
        this.isComplete = isComplete;
    }

    public Integer getIsCook() {
        return isCook;
    }

    public void setIsCook(Integer isCook) {
        this.isCook = isCook;
    }

    @Override
    public String toString() {
        return "Order{" +
                "orderId=" + orderId +
                ", tableId=" + tableId +
                ", startTime=" + startTime +
                ", cost=" + cost +
                ", isComplete=" + isComplete +
                ", isCook=" + isCook +
                '}';
    }
}
