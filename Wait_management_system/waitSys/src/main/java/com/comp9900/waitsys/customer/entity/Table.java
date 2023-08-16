package com.comp9900.waitsys.customer.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;


/**
 * @author Wei Chen
 * Date:2023-07-08 20:22
 * Description: the entity of Tables
 */
@TableName("tables")
public class Table implements Serializable {
    @TableId(type = IdType.AUTO)
    private Integer tableId;

    private Integer state;

    private Integer needHelp;

    public Table() {

    }

    public Table(Integer tableId, Integer state, Integer needHelp) {
        this.tableId = tableId;
        this.state = state;
        this.needHelp = needHelp;
    }

    public Integer getTableId() {
        return tableId;
    }

    public void setTableId(Integer tableId) {
        this.tableId = tableId;
    }

    public Integer getState() {
        return state;
    }

    public void setState(Integer state) {
        this.state = state;
    }

    public Integer getNeedHelp() {
        return needHelp;
    }

    public void setNeedHelp(Integer needHelp) {
        this.needHelp = needHelp;
    }

    @Override
    public String toString() {
        return "Table{" +
                "tableId=" + tableId +
                ", state=" + state +
                ", needHelp=" + needHelp +
                '}';
    }
}
