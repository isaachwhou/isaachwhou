package com.comp9900.waitsys.kitchen.entity;

import lombok.Data;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
@Data
public class OrderItemKitchenVO {
    private Integer id;
    private String itemName;
    private Integer isCook;
}
