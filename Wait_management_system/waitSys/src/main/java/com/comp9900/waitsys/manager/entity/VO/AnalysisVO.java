package com.comp9900.waitsys.manager.entity.VO;

import com.comp9900.waitsys.manager.entity.DTO.CategorySalePercentDTO;
import com.comp9900.waitsys.manager.entity.DTO.ItemSaleDTO;
import lombok.Data;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/29
 */
@Data
public class AnalysisVO {
    private Double totalSale;
    private Integer orderNum;
    private Double orderAvgCost;
    private List<ItemSaleDTO> topItemSale;
    private List<CategorySalePercentDTO> categorySalePercent;

}
