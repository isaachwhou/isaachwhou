package com.comp9900.waitsys.customer.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.comp9900.waitsys.customer.entity.Table;
import com.github.yulichang.base.MPJBaseMapper;
import org.springframework.stereotype.Repository;


/**
 * @author Wei Chen
 * Date:2023-07-08 20:22
 * Description: the mapper of Tables
 */
@Repository
public interface TableMapper extends BaseMapper<Table>, MPJBaseMapper<Table> {
}
