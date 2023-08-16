package com.comp9900.waitsys.kitchen.service.impl;

import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.customer.mapper.OrderMapper;
import com.comp9900.waitsys.kitchen.service.KitchenOrderService;
import com.github.yulichang.base.MPJBaseServiceImpl;
import org.springframework.stereotype.Service;

import static com.comp9900.waitsys.constant.Constant.ORDER_ISCOOK_TRUE;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
@Service
public class KitchenOrderServiceImpl extends MPJBaseServiceImpl<OrderMapper, Order> implements KitchenOrderService {


    @Override
    public boolean modifyOrderIsCook(Integer orderId){
        Order order= this.getById(orderId);
        order.setIsCook(ORDER_ISCOOK_TRUE);
        return updateById(order);
    }
}
