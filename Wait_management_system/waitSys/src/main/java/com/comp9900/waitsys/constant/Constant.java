package com.comp9900.waitsys.constant;

/**
 * the class of Constant value
 * @author Wei Chen
 * Data 2023-06-26 15:30
 */
public class Constant {
    // initial value of item rating
    public final static Float INITIAL_RATING = 0f;

    // initial value of order price
    public final static Float INITIAL_COST = 0f;

    // value of true integer -> boolean
    public static final Integer TRUE_VALUE = 1;

    // value of false integer -> boolean
    public static final Integer FALSE_VALUE = 0;

    // value of table needHelp when table need help
    public static final Integer TABLE_NEEDHELP_NEED_HELP = 1;

    // initial value of table needHelp
    public static final Integer TABLE_NEEDHELP_NO_NEED_HELP = 0;

    // value of table state when table is using
    public static final Integer TABLE_STATE_ACTIVE = 1;

    // value of table state when table is free
    public static final Integer TABLE_STATE_EMPTY = 0;

    // value of table state when table requests bill and ready to pay
    public static final Integer TABLE_STATE_TO_PAY = 2;

    // value of order isComplete when table is ordering
    public static final Integer ORDER_ISCOMPLETE_ORDERING = 0;

    // value of order isComplete when table ordered and having meal
    public static final Integer ORDER_ISCOMPLETE_START = 1;

    // value of order isComplete when table requests bill and ready to pay
    public static final Integer ORDER_ISCOMPLETE_FINISH = 2;


    // value of orderItem isCook when item of this order is cooked
    public static final Integer ORDERITEM_ISCOOK_TRUE = 1;

    // value of orderItem isCook when item of this order doesn't cook
    public static final Integer ORDERITEM_ISCOOK_FALSE = 0;

    // value of orderItem isServe when item of this order is served
    public static final Integer ORDERITEM_ISSERVE_TRUE = 1;

    // value of orderItem isServe when item of this order doesn't serve
    public static final Integer ORDERITEM_ISSERVE_FALSE = 0;

    public static final Integer ORDER_ISCOOK_TRUE = 1;

    public static final Integer ORDER_ISCOOK_FALSE = 0;

}
