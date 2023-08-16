package com.comp9900.waitsys.kitchen.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.comp9900.waitsys.kitchen.entity.OrderKitchenVO;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
public interface KitchenOrderItemService extends IService<OrderItem> {
    /**
    * @Description: 
    * @Param: []
    * @return: java.util.List<com.comp9900.waitsys.kitchen.entity.OrderKitchenVO>
    * @Author: Weizhe Pan
    * @Date: 2023/7/13
    */
    List<OrderKitchenVO> showAllOrdersKitchen();

    /**
    * @Description:
    * @Param: [orderItemId]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/7/13
    */
    Integer modifyOrderItemIsCook(Integer orderItemId);



}
