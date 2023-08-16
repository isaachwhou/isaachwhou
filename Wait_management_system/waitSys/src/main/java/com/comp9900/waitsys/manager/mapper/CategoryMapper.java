package com.comp9900.waitsys.manager.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.comp9900.waitsys.manager.entity.Category;
import com.github.yulichang.base.MPJBaseMapper;
import org.springframework.stereotype.Repository;

@Repository
public interface CategoryMapper extends BaseMapper<Category>, MPJBaseMapper<Category> {
}
