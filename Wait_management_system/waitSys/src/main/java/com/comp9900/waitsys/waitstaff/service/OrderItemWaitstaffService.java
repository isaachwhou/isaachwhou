package com.comp9900.waitsys.waitstaff.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.OrderItem;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
public interface OrderItemWaitstaffService extends IService<OrderItem> {
    /**
    * @Description:
    * @Param: [orderItemId]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/7/14
    */
    Integer modifyIsServe(Integer orderItemId);
}
