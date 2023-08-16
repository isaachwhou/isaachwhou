package com.comp9900.waitsys.kitchen.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.Order;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
public interface KitchenOrderService extends IService<Order> {
    /**
     * @Description:
     * @Param: [orderId]
     * @return: boolean
     * @Author: Weizhe Pan
     * @Date: 2023/7/13
     */
    boolean modifyOrderIsCook(Integer orderId);
}
