package com.comp9900.waitsys.waitstaff.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.Table;
import com.comp9900.waitsys.waitstaff.entity.VO.TableWaitstaffVO;

import java.util.List;

/**
 * @author Weizhe Pan
 * @date 2023/7/14
 */
public interface TableWaitstaffService extends IService<Table> {
    /**
    * @Description:
    * @Param: [tableId]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/7/14
    */
    boolean confirmRequestBill(Integer tableId);

    /**
    * @Description:
    * @Param: [tableId]
    * @return: boolean
    * @Author: Weizhe Pan
    * @Date: 2023/7/14
    */
    boolean markNeedHelp(Integer tableId);

    /**
    * @Description:
    * @Param: []
    * @return: java.util.List<com.comp9900.waitsys.waitstaff.entity.VO.TableWaitstaffVO>
    * @Author: Weizhe Pan
    * @Date: 2023/7/14
    */
    List<TableWaitstaffVO> listAllTablesWaitstaff();
}
