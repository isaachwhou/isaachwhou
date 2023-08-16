package com.comp9900.waitsys.manager.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.manager.entity.Category;
import com.comp9900.waitsys.manager.entity.DTO.ItemSaleDTO;
import com.comp9900.waitsys.manager.entity.VO.AnalysisVO;

/**
 * @author Weizhe Pan
 * @date 2023/7/27
 */
public interface AnalysisService  extends IService<Order> {

    /**
    * @Description:
    * @Param: [state, x]
    * @return: com.comp9900.waitsys.manager.entity.DTO.ItemSaleDTO
    * @Author: Weizhe Pan
    * @Date: 2023/7/29
    */
    AnalysisVO Analyse(Integer state, Integer x);

}
