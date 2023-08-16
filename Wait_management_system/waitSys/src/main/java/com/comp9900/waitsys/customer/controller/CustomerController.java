package com.comp9900.waitsys.customer.controller;

import com.comp9900.waitsys.customer.entity.ItemRatingDTO;
import com.comp9900.waitsys.customer.entity.OrderItemVO;
import com.comp9900.waitsys.customer.entity.Table;
import com.comp9900.waitsys.customer.service.OrderItemService;
import com.comp9900.waitsys.customer.service.OrderService;
import com.comp9900.waitsys.customer.service.TableService;
import com.comp9900.waitsys.manager.entity.Item;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * @author Wei Chen
 * Date:2023-07-09 13:45
 * Description: the controller of customer
 */
@RestController
@RequestMapping("/waitsys/customer")
@CrossOrigin
public class CustomerController {
    @Autowired
    private TableService tableService;

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderItemService orderItemService;

    @PostMapping("/table/addTable")
    public boolean addTable() {
        return tableService.addNewTable();
    }

    @GetMapping("/table/showAll")
    public List<Integer> showAllTable(){
        return tableService.showAllAvailable();
    }

    @GetMapping("/table/getTableNum")
    public Integer getTableNumber(){
        return tableService.getTableNumber();
    }

    @PostMapping("start")
    public Map<String, Integer> startMeal(@RequestParam(value = "tableId") Integer tableId){
        Map<String,Integer> resultMap = new HashMap<>();
        tableService.activateTable(tableId);
        Integer orderId = orderService.addNewOrder(tableId);
        resultMap.put("tableId", tableId);
        resultMap.put("orderId", orderId);
        return resultMap;
    }

    @PostMapping("/finish")
    public boolean finishMeal(@RequestParam(value = "tableId") Integer tableId){
        boolean orderFree = orderService.finishOrders(tableId);
        boolean orderDelete = orderService.deleteOrder(tableId);
        boolean tableFree = tableService.freeTable(tableId);
        return orderFree && orderDelete && tableFree;
    }

    @PostMapping("/table/toPayTable")
    public List<Integer> toPayTable(@RequestParam(value = "tableId") Integer tableId){
        return tableService.toPayTable(tableId);
    }

    @PostMapping("/table/askForHelp")
    public boolean askForHelp(@RequestParam(value = "tableId") Integer tableId){
        return tableService.askForHelp(tableId);
    }

    @GetMapping("/order/showCurrentCost")
    public Float showCurrentCost(@RequestParam(value = "orderId") Integer orderId){
        return orderService.showCostOfCurrentOrder(orderId);
    }

    @GetMapping("/order/showTotalCost")
    public Float showTotalCost(@RequestParam(value = "tableId") Integer tableId){
        return orderService.showTotalCost(tableId);
    }

    @PostMapping("/order/addItem")
    public boolean addItemToOrder(@RequestParam(value = "tableId") Integer tableId,
                                  @RequestParam(value = "orderId") Integer orderId,
                                  @RequestParam(value = "itemId") Integer itemId){
        return orderItemService.addNewOrderItem(orderId, itemId, tableId);
    }

    @PostMapping("/order/removeItem")
    public boolean removeItemFromOrder(@RequestParam(value = "tableId") Integer tableId,
                                  @RequestParam(value = "orderId") Integer orderId,
                                  @RequestParam(value = "itemId") Integer itemId) {
        return orderItemService.removeOrderItem(orderId, itemId, tableId);
    }

    @GetMapping("/order/showAllItems")
    public List<OrderItemVO> showAllItems(@RequestParam(value = "orderId") Integer orderId){
        return orderItemService.showAllItemsByOrder(orderId);
    }

    @GetMapping("/order/showAllPreviousItems")
    public List<OrderItemVO> showAllPreviousItems(@RequestParam(value = "tableId") Integer tableId){
        return orderItemService.showAllPreviousItems(tableId);
    }

    @PostMapping("/order/finishOrder")
    public Map<String, Integer> finishOrder(@RequestParam(value = "tableId") Integer tableId,
                                            @RequestParam(value = "orderId") Integer orderId){
        orderService.orderById(orderId);
        Integer newOrderId = orderService.addNewOrder(tableId);
        Map<String, Integer> map = new HashMap<>();
        map.put("tableId", tableId);
        map.put("orderId", newOrderId);
        return map;
    }

    @GetMapping("/checkTableInfo")
    public Table checkTableInfo(@RequestParam(value = "tableId") Integer tableId){
        return tableService.checkTableInfo(tableId);
    }

    @GetMapping("/order/showItemsByOrders")
    public List<Item> showItemsByOrders(@RequestParam(value = "orderIds") List<Integer> orderIds) {
        return orderItemService.showAllItemsByOrders(orderIds);
    }

    @PostMapping("/order/rating")
    public boolean ratingOrderItems(@RequestBody ItemRatingDTO itemRatingDTO){
        Integer tableId = itemRatingDTO.getTableId();
        List<Integer> orderIds = itemRatingDTO.getOrderIds();
        HashMap<Integer, Float> itemRatings = itemRatingDTO.getItemRatings();
        return orderItemService.ratingOrderItems(orderIds, tableId, itemRatings);
    }

}
