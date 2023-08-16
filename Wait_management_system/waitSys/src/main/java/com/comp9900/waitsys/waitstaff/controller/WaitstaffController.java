package com.comp9900.waitsys.waitstaff.controller;

import com.comp9900.waitsys.waitstaff.entity.VO.TableWaitstaffVO;
import com.comp9900.waitsys.waitstaff.service.OrderItemWaitstaffService;
import com.comp9900.waitsys.waitstaff.service.TableWaitstaffService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/13
 */
@RestController
@RequestMapping("/waitsys/waitstaff")
@CrossOrigin
public class WaitstaffController {
    @Autowired
    OrderItemWaitstaffService orderItemWaitstaffService;

    @Autowired
    TableWaitstaffService tableWaitstaffService;

    @GetMapping("/list_all_tables_waitstaff")
    public List<TableWaitstaffVO> listAllTablesWaitstaff(){return tableWaitstaffService.listAllTablesWaitstaff();}

    @PostMapping("/confirm_request_bill")
    public boolean confirmRequestBill(@RequestParam(value = "tableId")Integer tableId){
        return tableWaitstaffService.confirmRequestBill(tableId);
    }

    @PostMapping("/mark_need_help")
    public boolean markNeedHelp(@RequestParam(value = "tableId")Integer tableId){
        return tableWaitstaffService.markNeedHelp(tableId);
    }

    @PostMapping("/modify_order_item_is_serve")
    public Integer modifyIsServe(@RequestParam(value = "orderItemId")Integer orderItemId){
        return orderItemWaitstaffService.modifyIsServe(orderItemId);
    }
}
