package com.comp9900.waitsys.customer.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.Order;

import java.util.List;

/**
 * @author Wei Chen
 * Date:2023-07-08 21:29
 * Description: the service of order
 */
public interface OrderService extends IService<Order> {

    /**
     * add a new order for this table
     * when the table activate
     * when the last order start (isComplete = ORDER_ISCOMPLETE_START), add a new order for this table
     * order IsComplete = ORDER_ISCOMPLETE_ORDERING
     * @param tableId table id
     * @return order id
     */
    Integer addNewOrder(Integer tableId);

    /**
     * delete the order which isComplete = ORDER_ISCOMPLETE_ORDERING
     * when the table checks the bill
     * need also delete the order items of this order
     * @param tableId table id
     * @return true or false
     */
    boolean deleteOrder(Integer tableId);

    /**
     * order this order by order id
     * change isComplete: ORDER_ISCOMPLETE_ORDERING -> ORDER_ISCOMPLETE_START
     * @param orderId order id
     * @return true or false
     */
    boolean orderById(Integer orderId);

    /**
     * change isComplete = ORDER_ISCOMPLETE_START -> ORDER_ISCOMPLETE_FINISH
     * for all orders of this table when table checks the bill
     * @param tableId table id
     * @return true or false
     */
    boolean finishOrders(Integer tableId);

    /**
     * get the current order id of this table, which isComplete = ORDER_ISCOMPLETE_ORDERING
     * @param tableId table id
     * @return order id
     */
    Integer getCurrentOrderId(Integer tableId);

    /**
     * show the cost of current order (doesn't order)
     * @param orderId order id
     * @return cost
     */
    Float showCostOfCurrentOrder(Integer orderId);

    /**
     * show the total cost of all orders of this table (orders need to pay)
     * @param tableId table id
     * @return total cost
     */
    Float showTotalCost(Integer tableId);

}
