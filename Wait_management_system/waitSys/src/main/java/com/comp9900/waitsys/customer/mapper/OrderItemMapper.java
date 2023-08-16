package com.comp9900.waitsys.customer.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.github.yulichang.base.MPJBaseMapper;
import org.springframework.stereotype.Repository;

@Repository
public interface OrderItemMapper extends BaseMapper<OrderItem>, MPJBaseMapper<OrderItem> {
}
