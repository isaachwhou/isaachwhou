package com.comp9900.waitsys.customer.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.customer.entity.Table;

import java.util.List;

/**
 * @author Wei Chen
 * Date:2023-07-08 21:29
 * Description: the service of table
 */
public interface TableService extends IService<Table> {

    /**
     * Show all available table id
     * @return list of table id
     */
    List<Integer> showAllAvailable();

    /**
     * return the total number of tables
     * @return number of tables
     */
    Integer getTableNumber();

    /**
     * add new table
     * default state = TABLE_EMPTY, needHelp = NO_NEED_HELP
     * @return true or false
     */
    boolean addNewTable();

    /**
     * activate a table by table id, change state of this table to TABLE_ACTIVE
     * table state: TABLE_STATE_EMPTY -> TABLE_STATE_ACTIVE
     * @param tableId table id
     * @return true or false
     */
    boolean activateTable(Integer tableId);

    /**
     * free a table by table id, change state of this table to TABLE_EMPTY
     * table state: TABLE_STATE_TO_PAY -> TABLE_STATE_EMPTY
     * @param tableId table id
     * @return true or false
     */
    boolean freeTable(Integer tableId);

    /**
     * change the table state to "toPay", ready to pay the bill
     * table state: TABLE_STATE_ACTIVE -> TABLE_STATE_TO_PAY
     * @param tableId table id
     * @return true or false
     */
    List<Integer> toPayTable(Integer tableId);

    /**
     * ask for help
     * @param tableId table id
     * @return true or false
     */
    boolean askForHelp(Integer tableId);

    /**
    * @Description:
    * @Param: [tableId]
    * @return: com.comp9900.waitsys.customer.entity.TableVO
    * @Author: Weizhe Pan
    * @Date: 2023/7/18
    */
    Table checkTableInfo(Integer tableId);

}
