package com.comp9900.waitsys.manager.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.comp9900.waitsys.constant.Constant;
import com.comp9900.waitsys.customer.entity.OrderItem;
import com.comp9900.waitsys.manager.entity.Category;
import com.comp9900.waitsys.manager.entity.Item;
import com.comp9900.waitsys.manager.entity.VO.ItemVO;
import com.comp9900.waitsys.manager.mapper.ItemMapper;
import com.comp9900.waitsys.manager.service.ItemService;
import com.github.yulichang.toolkit.JoinWrappers;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * @author Wei Chen
 * Date:2023-06-25 18:45
 * Description: the service implementation of manager
 */
@Service
public class ItemServiceImpl extends ServiceImpl<ItemMapper, Item> implements ItemService {

    @Autowired
    private ItemMapper itemMapper;

    @Override
    public boolean addNewItem(String name, MultipartFile picture, String description, String ingredient, Float price, Integer categoryId) throws IOException {
        Item item = new Item();
        item.setName(name);
        if (picture != null) {
            byte[] pictureByte = picture.getBytes();
            item.setPicture(pictureByte);
        } else {
            item.setPicture(null);
        }
        item.setDescription(description);
        item.setIngredient(ingredient);
        item.setPrice(price);
        item.setCategoryId(categoryId);
        item.setRating(Constant.INITIAL_RATING);
        item.setIsOnMenu(Constant.TRUE_VALUE);
        item.setOrderNum((int) count() + 1);

        return save(item);
    }

    @Override
    public boolean updateItem(Integer itemId, String name, MultipartFile picture, String description, String ingredient, Float price, Integer categoryId) throws IOException {
        Item item = getById(itemId);
        item.setName(name);
        if (picture != null) {
            byte[] pictureByte = picture.getBytes();
            item.setPicture(pictureByte);
        } else {
            item.setPicture(null);
        }
        item.setDescription(description);
        item.setIngredient(ingredient);
        item.setPrice(price);
        item.setCategoryId(categoryId);

        return updateById(item);
    }

    @Override
    public boolean removeItem(Integer itemId) {
        Item item = getById(itemId);
        item.setIsOnMenu(Constant.FALSE_VALUE);
        return updateById(item);
    }

    @Override
    public boolean changeItemOrderNum(HashMap<Integer, Integer> itemMap) {
        int count = 0;
        for (int i : itemMap.keySet()) {
            Item item = getById(i);
            item.setOrderNum(itemMap.get(i));
            if (updateById(item)) {
                count++;
            }
        }
        return count == itemMap.size();
    }

    @Override
    public IPage<ItemVO> showAllItem(Integer pageNo, Integer pageSize) {
        Page<ItemVO> pageSetting = new Page<>(pageNo, pageSize);
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE)
                .orderByDesc(Item::getOrderNum);
        IPage<ItemVO> itemVOIPage = itemMapper.selectJoinPage(pageSetting, ItemVO.class, wrapper);
        return itemVOIPage;
    }

    @Override
    public IPage<ItemVO> showItemByCategory(Integer categoryId, Integer pageNo, Integer pageSize) {
        Page<ItemVO> pageSetting = new Page<>(pageNo, pageSize);
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .eq(Item::getCategoryId, categoryId)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE)
                .orderByDesc(Item::getOrderNum);
        IPage<ItemVO> itemVOIPage = itemMapper.selectJoinPage(pageSetting, ItemVO.class, wrapper);
        return itemVOIPage;
    }

    @Override
    public List<ItemVO> showTop5Item() {
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .orderByDesc(Item::getRating)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE)
                .last("limit 5");
        List<ItemVO> itemVOList = itemMapper.selectJoinList(ItemVO.class, wrapper);
        return itemVOList;
    }

    @Override
    public ItemVO showItemByItemId(Integer itemId) {
        // multi table search
        // select item.*, category.name from Item left join Category where item.category_id = Category.category.id;
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .eq(Item::getItemId, itemId);
        List<ItemVO> itemVOList = itemMapper.selectJoinList(ItemVO.class, wrapper);
        return itemVOList.get(0);
    }

    @Override
    public List<ItemVO> showAllItemList() {
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE);
        List<ItemVO> itemVOList = itemMapper.selectJoinList(ItemVO.class, wrapper);
        return itemVOList;
    }

    @Override
    public List<ItemVO> showItemListByCategory(Integer categoryId) {
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .eq(Item::getCategoryId, categoryId)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE);
        List<ItemVO> itemVOList = itemMapper.selectJoinList(ItemVO.class, wrapper);
        return itemVOList;
    }

    @Override
    public List<ItemVO> showTop5SaleItems() {
        MPJLambdaWrapper<Item> wrapper = JoinWrappers.lambda(Item.class)
                .selectAll(Item.class)
                .leftJoin(Category.class, Category::getCategoryId, Item::getCategoryId)
                .selectAs(Category::getName, ItemVO::getCategory)
                .leftJoin(OrderItem.class, OrderItem::getItemId, Item::getItemId)
                .eq(Item::getIsOnMenu, Constant.TRUE_VALUE)
                .eq(Category::getIsOnMenu, Constant.TRUE_VALUE);
        List<ItemVO> itemVOList = itemMapper.selectJoinList(ItemVO.class, wrapper);
        Map<ItemVO, Integer> map = new LinkedHashMap<>();
        for (ItemVO itemVO: itemVOList) {
            if (!map.containsKey(itemVO)) {
                map.put(itemVO, 1);
            }
            else {
                map.put(itemVO, map.get(itemVO) + 1);
            }
        }
        List<ItemVO> itemVOS = map.entrySet().stream()
                .sorted((entry1, entry2) -> entry2.getValue().compareTo(entry1.getValue()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
        List<ItemVO> res = new LinkedList<>();
        for (int i = 0; i < itemVOS.size(); i++) {
            if (i < 5) {
                res.add(itemVOS.get(i));
            }
            else {
                break;
            }
        }
        res.forEach(System.out::println);
        return res;
    }
}
