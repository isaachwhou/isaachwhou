package com.comp9900.waitsys.kitchen.controller;

import com.comp9900.waitsys.kitchen.entity.OrderKitchenVO;
import com.comp9900.waitsys.kitchen.service.KitchenOrderItemService;
import com.comp9900.waitsys.kitchen.service.KitchenOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
@RestController
@RequestMapping("/waitsys/kitchen")
@CrossOrigin
public class KitchenController {
    @Autowired
    private KitchenOrderItemService kitchenOrderItemService;

    @Autowired
    private KitchenOrderService kitchenOrderService;



    @GetMapping("/list_all_orders_kitchen")
    public List<OrderKitchenVO> showAllOrdersKitchen() {
        return kitchenOrderItemService.showAllOrdersKitchen();
    }

    @PostMapping("/modify_order_item_is_cook")
    public Integer modifyOrderItemIsCook(@RequestParam(value = "orderItemId") Integer orderItemId){
        return kitchenOrderItemService.modifyOrderItemIsCook(orderItemId);
    }

    @PostMapping("/modify_order_is_cook")
    public boolean modifyOrderIsCook(@RequestParam(value = "orderId") Integer orderId){
        return kitchenOrderService.modifyOrderIsCook(orderId);
    }
}
