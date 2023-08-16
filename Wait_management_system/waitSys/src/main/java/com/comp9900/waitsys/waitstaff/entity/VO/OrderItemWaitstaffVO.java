package com.comp9900.waitsys.waitstaff.entity.VO;

import lombok.Data;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
@Data
public class OrderItemWaitstaffVO {
    private Integer id;
    private String itemName;
    private Integer isCook;
    private Integer isServe;
}
