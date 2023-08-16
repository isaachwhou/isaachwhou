package com.comp9900.waitsys.manager.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.comp9900.waitsys.manager.entity.Item;
import com.github.yulichang.base.MPJBaseMapper;
import org.springframework.stereotype.Repository;

@Repository
public interface ItemMapper extends BaseMapper<Item>, MPJBaseMapper<Item> {
}
