package com.comp9900.waitsys.kitchen.service.impl;

import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.comp9900.waitsys.customer.mapper.OrderItemMapper;
import com.comp9900.waitsys.customer.mapper.OrderMapper;
import com.comp9900.waitsys.kitchen.entity.OrderDTO;
import com.comp9900.waitsys.kitchen.entity.OrderItemKitchenVO;
import com.comp9900.waitsys.kitchen.entity.OrderKitchenVO;
import com.comp9900.waitsys.kitchen.service.KitchenOrderItemService;
import com.comp9900.waitsys.manager.entity.Item;
import com.github.yulichang.base.MPJBaseServiceImpl;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

import static com.comp9900.waitsys.constant.Constant.*;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
@Service
public class KitchenOrderItemServiceImpl extends MPJBaseServiceImpl<OrderItemMapper, OrderItem> implements KitchenOrderItemService {
    @Autowired
    private OrderItemMapper orderItemMapper;

    @Autowired
    private OrderMapper orderMapper;


    @Override
    public List<OrderKitchenVO> showAllOrdersKitchen() {
        List<OrderKitchenVO> orderKitchenVOList=new ArrayList<>();
        MPJLambdaWrapper<Order> myWrapper = new MPJLambdaWrapper<>();
        myWrapper
                .eq(Order::getIsCook, FALSE_VALUE)
                .eq(Order::getIsComplete, ORDER_ISCOMPLETE_START)
                .selectAs(Order::getOrderId,"orderId")
                .selectAs(Order::getTableId,"tableId")
                .selectAs(Order::getStartTime,"startTime")
                .orderByAsc(Order::getStartTime);
        List<OrderDTO> orderDTOList=orderMapper.selectJoinList(OrderDTO.class,myWrapper);
        for (OrderDTO orderDTO:orderDTOList)
        {
            OrderKitchenVO orderKitchenVO=new OrderKitchenVO();
            orderKitchenVO.setTableId(orderDTO.getTableId());
            orderKitchenVO.setOrderId(orderDTO.getOrderId());
            orderKitchenVO.setStartTime(orderDTO.getStartTime());
            MPJLambdaWrapper<OrderItem> myWrapper2 = new MPJLambdaWrapper<>();
            myWrapper2
                    .leftJoin(Item.class,Item::getItemId,OrderItem::getItemId)
                    .eq(OrderItem::getOrderId,orderDTO.getOrderId())
                    .selectAs(OrderItem::getId,"id")
                    .selectAs(Item::getName,"itemName")
                    .selectAs(OrderItem::getIsCook,"isCook")
                    .orderByAsc(OrderItem::getId);
            List<OrderItemKitchenVO> orderItemList=orderItemMapper.selectJoinList(OrderItemKitchenVO.class,myWrapper2);
            orderKitchenVO.setOrderItemList(orderItemList);
            orderKitchenVOList.add(orderKitchenVO);

        }


        return orderKitchenVOList;
    }

    @Override
    public Integer modifyOrderItemIsCook(Integer orderItemId) {

        OrderItem orderItem=this.getById(orderItemId);
        Integer isCook=orderItem.getIsCook();
        if (isCook==0){
            orderItem.setIsCook(ORDERITEM_ISCOOK_TRUE);
        }
        else{orderItem.setIsCook(ORDERITEM_ISCOOK_FALSE);}
        updateById(orderItem);
        return orderItem.getIsCook();
    }


}
