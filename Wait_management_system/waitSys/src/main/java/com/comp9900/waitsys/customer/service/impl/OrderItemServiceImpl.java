package com.comp9900.waitsys.customer.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.comp9900.waitsys.constant.Constant;
import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.comp9900.waitsys.customer.entity.OrderItemDTO;
import com.comp9900.waitsys.customer.entity.OrderItemVO;
import com.comp9900.waitsys.customer.mapper.OrderItemMapper;
import com.comp9900.waitsys.customer.mapper.OrderMapper;
import com.comp9900.waitsys.customer.service.OrderItemService;
import com.comp9900.waitsys.manager.entity.Item;
import com.comp9900.waitsys.manager.mapper.ItemMapper;
import com.github.yulichang.toolkit.JoinWrappers;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.relational.core.sql.In;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Service
public class OrderItemServiceImpl extends ServiceImpl<OrderItemMapper, OrderItem> implements OrderItemService {

    @Autowired
    private OrderItemMapper orderItemMapper;

    @Autowired
    private OrderMapper orderMapper;

    @Autowired
    private ItemMapper itemMapper;

    @Override
    public boolean addNewOrderItem(Integer orderId, Integer itemId, Integer tableId) {
        OrderItem orderItem = new OrderItem();
        orderItem.setOrderId(orderId);
        orderItem.setTableId(tableId);
        orderItem.setItemId(itemId);
        orderItem.setRating(Constant.INITIAL_RATING);
        orderItem.setIsCook(Constant.ORDERITEM_ISCOOK_FALSE);
        orderItem.setIsServe(Constant.ORDERITEM_ISSERVE_FALSE);
        // need change the current cost of this order: cost = cost + item.price
        Order order = orderMapper.selectById(orderId);
        Item item = itemMapper.selectById(itemId);
        order.setCost(order.getCost() + item.getPrice());
        return save(orderItem) && (orderMapper.updateById(order) == 1);
    }

    @Override
    public boolean deleteOrderItemsByOrder(Integer orderId) {
        LambdaQueryWrapper<OrderItem> lqw = new LambdaQueryWrapper<>();
        lqw.eq(OrderItem::getOrderId, orderId);
        List<OrderItem> orderItems = list(lqw);
        return removeBatchByIds(orderItems);
    }

    private List<OrderItemVO> convertOrderItemDTOSToOrderItemVOS(List<OrderItemDTO> orderItemDTOS){
        List<OrderItemVO> orderItemVOS = new ArrayList<>();
        // calculate the item number and total price
        for (OrderItemDTO orderItemDTO : orderItemDTOS) {
            boolean inFlag = false;
            for (OrderItemVO orderItemVO : orderItemVOS) {
                if (Objects.equals(orderItemDTO.getItemId(), orderItemVO.getItemId())) {
                    inFlag = true;
                    orderItemVO.setItemNumber(orderItemVO.getItemNumber() + 1);
                    orderItemVO.setTotalPrice(orderItemDTO.getPrice() * orderItemVO.getItemNumber());
                    break;
                }
            }
            if (!inFlag){
                OrderItemVO orderItemVO = new OrderItemVO();
                orderItemVO.setItemId(orderItemDTO.getItemId());
                orderItemVO.setItemPicture(orderItemDTO.getItemPicture());
                orderItemVO.setItemName(orderItemDTO.getItemName());
                orderItemVO.setItemNumber(1);
                orderItemVO.setTotalPrice(orderItemDTO.getPrice());
                orderItemVOS.add(orderItemVO);
            }
        }
        return orderItemVOS;
    }

    @Override
    public List<OrderItemVO> showAllItemsByOrder(Integer orderId) {
        MPJLambdaWrapper<OrderItem> wrapper = JoinWrappers.lambda(OrderItem.class)
                .selectAll(OrderItem.class)
                .selectAs(Item::getName, OrderItemDTO::getItemName)
                .selectAs(Item::getPicture, OrderItemDTO::getItemPicture)
                .selectAs(Item::getPrice, OrderItemDTO::getPrice)
                .leftJoin(Item.class, Item::getItemId, OrderItem::getItemId)
                .eq(OrderItem::getOrderId, orderId);
                //.groupBy(OrderItem::getItemId);
        List<OrderItemDTO> orderItemDTOS = orderItemMapper.selectJoinList(OrderItemDTO.class, wrapper);
        return convertOrderItemDTOSToOrderItemVOS(orderItemDTOS);
    }

    @Override
    public List<OrderItemVO> showAllPreviousItems(Integer tableId) {
        MPJLambdaWrapper<OrderItem> wrapper = JoinWrappers.lambda(OrderItem.class)
                .selectAll(OrderItem.class)
                .selectAs(Item::getName, OrderItemDTO::getItemName)
                .selectAs(Item::getPicture, OrderItemDTO::getItemPicture)
                .selectAs(Item::getPrice, OrderItemDTO::getPrice)
                .leftJoin(Item.class, Item::getItemId, OrderItem::getItemId)
                .leftJoin(Order.class, Order::getOrderId, OrderItem::getOrderId)
                .eq(OrderItem::getTableId, tableId)
                .eq(Order::getIsComplete, Constant.ORDER_ISCOMPLETE_START);
        //.groupBy(OrderItem::getItemId);
        List<OrderItemDTO> orderItemDTOS = orderItemMapper.selectJoinList(OrderItemDTO.class, wrapper);
        return convertOrderItemDTOSToOrderItemVOS(orderItemDTOS);
    }

    @Override
    public boolean removeOrderItem(Integer orderId, Integer itemId, Integer tableId) {
        LambdaQueryWrapper<OrderItem> lqw = new LambdaQueryWrapper<>();
        lqw.eq(OrderItem::getTableId, tableId)
                .eq(OrderItem::getOrderId, orderId)
                .eq(OrderItem::getItemId, itemId);
        List<OrderItem> orderItems = list(lqw);
        Order order = orderMapper.selectById(orderId);
        Item item = itemMapper.selectById(itemId);
        order.setCost(order.getCost() - item.getPrice());
        boolean flag = orderMapper.updateById(order) == 1;
        return removeById(orderItems.get(0)) && flag;
    }

    @Override
    public List<Item> showAllItemsByOrders(List<Integer> orderIds) {
        LambdaQueryWrapper<OrderItem> lqw = new LambdaQueryWrapper<>();
        lqw.in(OrderItem::getOrderId, orderIds);
        List<OrderItem> orderItems = list(lqw);
        List<Integer> itemIds = new ArrayList<>();
        for (OrderItem orderItem: orderItems) {
            itemIds.add(orderItem.getItemId());
        }
        List<Integer> itemIdList = itemIds.stream().distinct().collect(Collectors.toList());
        LambdaQueryWrapper<Item> iQuery = new LambdaQueryWrapper<>();
        iQuery.in(Item::getItemId, itemIds);
        return itemMapper.selectList(iQuery);

    }

    @Override
    public boolean ratingOrderItems(List<Integer> orderIds, Integer tableId, HashMap<Integer, Float> itemRatings) {
        LambdaQueryWrapper<OrderItem> lqw = new LambdaQueryWrapper<>();
        lqw.eq(OrderItem::getTableId, tableId)
                .in(OrderItem::getOrderId, orderIds);
        List<OrderItem> orderItems = list(lqw);
        for (int i = 0; i < orderItems.size(); i++) {
            if (itemRatings.containsKey(orderItems.get(i).getItemId())){
                orderItems.get(i).setRating(itemRatings.get(orderItems.get(i).getItemId()));
            }
        }
        boolean oFlag = updateBatchById(orderItems);
        List<Item> items = itemMapper.selectBatchIds(itemRatings.keySet());
        List<Integer> itemIds = new ArrayList<>();
        for (Item item: items) {
            itemIds.add(item.getItemId());
        }
        LambdaQueryWrapper<OrderItem> query = new LambdaQueryWrapper<>();
        query.in(OrderItem::getItemId, itemIds);
        List<OrderItem> orderItemList = list(query);
        boolean iFlag = true;
        for (int i = 0; i < items.size(); i++) {
            Float totalRating = Constant.INITIAL_RATING;
            Integer totalNum = 0;
            for (int j = 0; j < orderItemList.size(); j++) {
                if (Objects.equals(items.get(i).getItemId(), orderItemList.get(j).getItemId())){
                    if(orderItemList.get(j).getRating() != 0) {
                        totalRating += orderItemList.get(j).getRating();
                        totalNum += 1;
                    }
                }
            }
            items.get(i).setRating(totalRating/totalNum);
            if(itemMapper.updateById(items.get(i)) != 1){
                iFlag = false;
            }
        }
        return oFlag && iFlag;

    }
}
