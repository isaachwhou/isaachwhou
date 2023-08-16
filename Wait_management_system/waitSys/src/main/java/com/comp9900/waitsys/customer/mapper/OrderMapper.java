package com.comp9900.waitsys.customer.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.comp9900.waitsys.customer.entity.Order;
import com.github.yulichang.base.MPJBaseMapper;
import org.springframework.stereotype.Repository;


/**
 * @author Wei Chen
 * Date:2023-07-08 20:22
 * Description: the mapper of Orders
 */
@Repository
public interface OrderMapper extends BaseMapper<Order>, MPJBaseMapper<Order> {
}
