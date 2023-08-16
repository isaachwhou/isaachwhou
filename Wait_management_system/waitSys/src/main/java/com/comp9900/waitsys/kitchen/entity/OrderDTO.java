package com.comp9900.waitsys.kitchen.entity;

import lombok.Data;

import java.sql.Timestamp;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */

@Data
public class OrderDTO {
    private Integer orderId;
    private Integer tableId;
    private Timestamp startTime;
}
