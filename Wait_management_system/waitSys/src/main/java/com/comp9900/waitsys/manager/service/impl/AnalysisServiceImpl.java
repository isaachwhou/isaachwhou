package com.comp9900.waitsys.manager.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.comp9900.waitsys.customer.entity.Order;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.comp9900.waitsys.customer.mapper.OrderItemMapper;
import com.comp9900.waitsys.customer.mapper.OrderMapper;
import com.comp9900.waitsys.customer.service.OrderService;
import com.comp9900.waitsys.manager.entity.Category;
import com.comp9900.waitsys.manager.entity.DTO.CategorySaleDTO;
import com.comp9900.waitsys.manager.entity.DTO.CategorySalePercentDTO;
import com.comp9900.waitsys.manager.entity.DTO.ItemSaleDTO;
import com.comp9900.waitsys.manager.entity.Item;
import com.comp9900.waitsys.manager.entity.VO.AnalysisVO;
import com.comp9900.waitsys.manager.mapper.CategoryMapper;
import com.comp9900.waitsys.manager.service.AnalysisService;
import com.comp9900.waitsys.manager.service.CategoryService;
import com.github.yulichang.base.MPJBaseServiceImpl;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static com.comp9900.waitsys.constant.Constant.*;

/**
 * @author Weizhe Pan
 * @date 2023/7/29
 */
@Service
public class AnalysisServiceImpl extends MPJBaseServiceImpl<OrderMapper, Order> implements AnalysisService {
    @Autowired
    OrderMapper orderMapper;

    @Autowired
    OrderItemMapper orderItemMapper;

    @Override
    public AnalysisVO Analyse(Integer state,Integer x) {
        AnalysisVO analysisVO =new AnalysisVO();
        String lastSql="limit "+String.valueOf(x);

        //count total sale
        QueryWrapper<Order> queryWrapper = new QueryWrapper<Order>();
        queryWrapper.select("cast(sum(cost) as DECIMAL(10,2)) as sum");
        queryWrapper.eq("is_complete",ORDER_ISCOMPLETE_FINISH);
        if (state==0){
            queryWrapper.apply("DATE_FORMAT(start_time,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')");
        }
        else if (state==1){
            queryWrapper.apply("TO_DAYS(start_time) between TO_DAYS(NOW())-7 and TO_DAYS(NOW())");
        }
        else if (state==2){
            queryWrapper.apply("DATE_FORMAT(start_time,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')");
        }
        else{
            queryWrapper.apply("DATE_FORMAT(start_time,'%Y')=DATE_FORMAT(NOW(),'%Y')");
        }
        Map<String, Object> count = orderMapper.selectMaps(queryWrapper).get(0);
        if (count == null){
            analysisVO.setTotalSale(Double.valueOf(0)); ;
        }else{
           analysisVO.setTotalSale(Double.valueOf(String.valueOf(count.get("sum"))));
        }

        //count total order numbers
        QueryWrapper<Order> queryWrapper2 = new QueryWrapper<Order>();
        queryWrapper2.eq("is_complete",ORDER_ISCOMPLETE_FINISH);
        if (state==0){
            queryWrapper2.apply("DATE_FORMAT(start_time,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')");
        }
        else if (state==1){
            queryWrapper2.apply("TO_DAYS(start_time) between TO_DAYS(NOW())-7 and TO_DAYS(NOW())");
        }
        else if (state==2){
            queryWrapper2.apply("DATE_FORMAT(start_time,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')");
        }
        else{
            queryWrapper2.apply("DATE_FORMAT(start_time,'%Y')=DATE_FORMAT(NOW(),'%Y')");
        }
        analysisVO.setOrderNum(Math.toIntExact(orderMapper.selectCount(queryWrapper2)));

        //average order cost
        QueryWrapper<Order> queryWrapper3 = new QueryWrapper<Order>();
        queryWrapper3.select("cast(avg(cost) as DECIMAL(10,2)) as AvgCost");
        if (state==0){
            queryWrapper3.apply("DATE_FORMAT(start_time,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')");
        }
        else if (state==1){
            queryWrapper3.apply("TO_DAYS(start_time) between TO_DAYS(NOW())-7 and TO_DAYS(NOW())");
        }
        else if (state==2){
            queryWrapper3.apply("DATE_FORMAT(start_time,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')");
        }
        else{
            queryWrapper3.apply("DATE_FORMAT(start_time,'%Y')=DATE_FORMAT(NOW(),'%Y')");
        }
        Map<String, Object> avgCost = orderMapper.selectMaps(queryWrapper3).get(0);
        if (avgCost == null){
            analysisVO.setOrderAvgCost(Double.valueOf(0)); ;
        }else{
            analysisVO.setOrderAvgCost(Double.valueOf(String.valueOf(avgCost.get("AvgCost"))));
        }

        //top x item sale
        MPJLambdaWrapper<OrderItem> orderItemMPJLambdaWrapper=new MPJLambdaWrapper<OrderItem>();
        orderItemMPJLambdaWrapper
                .leftJoin(Item.class,Item::getItemId,OrderItem::getItemId)
                .leftJoin(Order.class,Order::getOrderId,OrderItem::getOrderId)
                .leftJoin(Category.class,Category::getCategoryId,Item::getCategoryId)
                .selectAs(Item::getName, "itemName")
                .select("count(*) as itemSaleCount")
                .eq(Order::getIsComplete,ORDER_ISCOMPLETE_FINISH)
                .eq(Category::getIsOnMenu,TRUE_VALUE)
                .groupBy("itemName")
                .orderByDesc("itemSaleCount");
        if (state==0){
            orderItemMPJLambdaWrapper.apply("DATE_FORMAT(start_time,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')");
        }
        else if (state==1){
            orderItemMPJLambdaWrapper.apply("TO_DAYS(start_time) between TO_DAYS(NOW())-7 and TO_DAYS(NOW())");
        }
        else if (state==2){
            orderItemMPJLambdaWrapper.apply("DATE_FORMAT(start_time,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')");
        }
        else{
            orderItemMPJLambdaWrapper.apply("DATE_FORMAT(start_time,'%Y')=DATE_FORMAT(NOW(),'%Y')");
        }
        orderItemMPJLambdaWrapper.last(lastSql);
        analysisVO.setTopItemSale(orderItemMapper.selectJoinList(ItemSaleDTO.class,orderItemMPJLambdaWrapper));

        //category sale percent
        MPJLambdaWrapper<OrderItem> orderItemMPJLambdaWrapper2=new MPJLambdaWrapper<OrderItem>();
        orderItemMPJLambdaWrapper2
                .leftJoin(Item.class,Item::getItemId,OrderItem::getItemId)
                .leftJoin(Category.class,Category::getCategoryId,Item::getCategoryId)
                .leftJoin(Order.class,Order::getOrderId,OrderItem::getOrderId)
                .eq(Order::getIsComplete,ORDER_ISCOMPLETE_FINISH)
                .eq(Category::getIsOnMenu,TRUE_VALUE)
                .selectAs(Category::getName,"categoryName")
                .select("ifnull(cast(sum(price) as DECIMAL(10,2)),0) as categorySale")
                .groupBy("categoryName");
        if (state==0){
            orderItemMPJLambdaWrapper2.apply("DATE_FORMAT(start_time,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')");
        }
        else if (state==1){
            orderItemMPJLambdaWrapper2.apply("TO_DAYS(start_time) between TO_DAYS(NOW())-7 and TO_DAYS(NOW())");
        }
        else if (state==2){
            orderItemMPJLambdaWrapper2.apply("DATE_FORMAT(start_time,'%Y-%m')=DATE_FORMAT(NOW(),'%Y-%m')");
        }
        else{
            orderItemMPJLambdaWrapper2.apply("DATE_FORMAT(start_time,'%Y')=DATE_FORMAT(NOW(),'%Y')");
        }
        List<CategorySaleDTO> categorySaleDTOList=orderItemMapper.selectJoinList(CategorySaleDTO.class,orderItemMPJLambdaWrapper2);
        System.out.println(Arrays.toString(categorySaleDTOList.toArray()));
        List<CategorySalePercentDTO> categorySalePercentDTOList=new ArrayList<>();
        for (CategorySaleDTO categorySaleDTO:categorySaleDTOList){
            CategorySalePercentDTO categorySalePercentDTO=new CategorySalePercentDTO();
            categorySalePercentDTO.setCategoryName(categorySaleDTO.getCategoryName());
            BigDecimal bd1=new BigDecimal(Double.toString(categorySaleDTO.getCategorySale()));
            BigDecimal bd2=new BigDecimal(Double.toString(analysisVO.getTotalSale()));
            Double temp_percent=bd1.divide(bd2, 2, BigDecimal.ROUND_HALF_UP).doubleValue();
            categorySalePercentDTO.setCategorySalePercent(temp_percent);
            categorySalePercentDTOList.add(categorySalePercentDTO);
        }
        analysisVO.setCategorySalePercent(categorySalePercentDTOList);
        return analysisVO;
    }
}
