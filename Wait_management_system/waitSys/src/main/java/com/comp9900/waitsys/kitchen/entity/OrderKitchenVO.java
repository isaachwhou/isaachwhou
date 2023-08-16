package com.comp9900.waitsys.kitchen.entity;

import lombok.Data;

import java.sql.Timestamp;
import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
@Data
public class OrderKitchenVO {
    private Integer tableId;
    private Integer orderId;
    private Timestamp startTime;
    private List<OrderItemKitchenVO> orderItemList;
}
