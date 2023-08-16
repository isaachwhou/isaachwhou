package com.comp9900.waitsys.waitstaff.entity.DTO;

import lombok.Data;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
@Data
public class TableDTO {
    private Integer tableId;
    private Integer state;
    private Integer needHelp;
}
