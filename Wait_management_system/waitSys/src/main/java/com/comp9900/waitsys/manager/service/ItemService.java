package com.comp9900.waitsys.manager.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.comp9900.waitsys.manager.entity.Item;
import com.comp9900.waitsys.manager.entity.VO.ItemVO;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;

/**
 * @author Wei Chen
 * Date:2023-06-25 18:45
 * Description: the service of manager
 */
public interface ItemService extends IService<Item> {

    /**
     * add a new dish item to menu
     * default: rating=0, isOnMenu=0, orderNum=count()+1
     * @param name item name
     * @param picture picture data
     * @param description item description
     * @param ingredient item ingredient
     * @param price item price
     * @param categoryId item category id
     * @return True or False
     */
    boolean addNewItem(String name, MultipartFile picture, String description, String ingredient, Float price, Integer categoryId) throws IOException;

    /**
     * update a dish item information
     * @param itemId itemId of the dish item
     * @param name new name
     * @param picture new picture
     * @param description new description
     * @param ingredient new ingredient
     * @param price new price
     * @param categoryId new category
     * @return True or False
     */
    boolean updateItem(Integer itemId, String name, MultipartFile picture, String description, String ingredient, Float price, Integer categoryId) throws IOException;

    /**
     * remove a dish item, change 'isOnMenu' to 1
     * @param itemId itemId
     * @return True or False
     */
    boolean removeItem(Integer itemId);

    /**
     * change the display order of dish item
     * @param itemMap the hash map of item (itemId, orderNum)
     * @return True or False
     */
    boolean changeItemOrderNum(HashMap<Integer, Integer> itemMap);

    /**
     * show all items of menu
     * @return pages of items
     */
    IPage<ItemVO> showAllItem(Integer pageNo, Integer pageSize);

    /**
     * show all items of menu
     * @return pages of items
     */
    List<ItemVO> showAllItemList();

    /**
     * show items by their category
     * @param categoryId item category id
     * @return pages of items
     */
    IPage<ItemVO> showItemByCategory(Integer categoryId, Integer pageNo, Integer pageSize);

    /**
     * show items by their category
     * @param categoryId item category id
     * @return pages of items
     */
    List<ItemVO> showItemListByCategory(Integer categoryId);

    /**
     * show Top 5 highest-rating dish items
     * @return list of items
     */
    List<ItemVO> showTop5Item();

    List<ItemVO> showTop5SaleItems();

    /**
     * show the item information by itemId
     * @param itemId item id
     * @return Item
     */
    ItemVO showItemByItemId(Integer itemId);
}
