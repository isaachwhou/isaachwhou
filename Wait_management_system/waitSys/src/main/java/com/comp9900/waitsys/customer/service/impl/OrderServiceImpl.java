package com.comp9900.waitsys.customer.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.comp9900.waitsys.constant.Constant;
import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.customer.mapper.OrderMapper;
import com.comp9900.waitsys.customer.service.OrderItemService;
import com.comp9900.waitsys.customer.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.util.List;

@Service
public class OrderServiceImpl extends ServiceImpl<OrderMapper, Order> implements OrderService {

    @Autowired
    private OrderItemService orderItemService;

    @Override
    public Integer addNewOrder(Integer tableId) {
        Order order = new Order();
        order.setTableId(tableId);
        order.setStartTime(new Timestamp(System.currentTimeMillis()));
        order.setCost(Constant.INITIAL_COST);
        order.setIsComplete(Constant.ORDER_ISCOMPLETE_ORDERING);
        order.setIsCook(Constant.FALSE_VALUE);
        save(order);
        return order.getOrderId();
    }

    @Override
    public boolean deleteOrder(Integer tableId) {
        LambdaQueryWrapper<Order> lqwOrder = new LambdaQueryWrapper<>();
        lqwOrder.eq(Order::getTableId, tableId).eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_ORDERING);
        // need to delete all order_items which orderId = orderId
        // Order order = getOne(lqwOrder);
        // Integer orderId = order.getOrderId();
        // orderItemService.deleteOrderItemsByOrder(orderId);
        return remove(lqwOrder);
    }

    @Override
    public boolean orderById(Integer orderId) {
        Order order = getById(orderId);
        order.setIsComplete(Constant.ORDER_ISCOMPLETE_START);
        order.setStartTime(new Timestamp(System.currentTimeMillis()));
        return updateById(order);
    }

    @Override
    public boolean finishOrders(Integer tableId) {
        LambdaQueryWrapper<Order> lqw = new LambdaQueryWrapper<>();
        lqw.eq(Order::getTableId, tableId).eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_START);
        List<Order> orders = list(lqw);
        for (Order order : orders) {
            order.setIsComplete(Constant.ORDER_ISCOMPLETE_FINISH);
        }
        return updateBatchById(orders);
    }

    @Override
    public Integer getCurrentOrderId(Integer tableId) {
        LambdaQueryWrapper<Order> lqw = new LambdaQueryWrapper<>();
        lqw.eq(Order::getTableId, tableId).eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_ORDERING);
        Order order = getOne(lqw);
        return order.getOrderId();
    }

    @Override
    public Float showCostOfCurrentOrder(Integer orderId) {
        LambdaQueryWrapper<Order> lqw = new LambdaQueryWrapper<>();
        lqw.eq(Order::getOrderId, orderId)
                .eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_ORDERING);
        Order order = getOne(lqw);
        return order.getCost();
    }

    @Override
    public Float showTotalCost(Integer tableId) {
        Float totalCost = Constant.INITIAL_COST;
        LambdaQueryWrapper<Order> lqw = new LambdaQueryWrapper<>();
        lqw.eq(Order::getTableId, tableId)
                .eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_START);
        List<Order> orders = list(lqw);
        for (Order order : orders) {
            totalCost += order.getCost();
        }
        return totalCost;
    }
}
