package com.comp9900.waitsys.waitstaff.entity.VO;

import com.comp9900.waitsys.kitchen.entity.OrderItemKitchenVO;
import lombok.Data;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
@Data
public class TableWaitstaffVO {
    private Integer tableId;
    private Integer state;
    private Integer needHelp;
    private List<OrderItemWaitstaffVO> orderItemList;
}
