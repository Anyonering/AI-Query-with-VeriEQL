# -*- coding:utf-8 -*-
from z3 import *
import itertools
import functools

sql1 = "WITH TEMP AS (SELECT DISTINCT A.CUSTOMER_ID, B.CUSTOMER_NAME, SUM(CASE WHEN A.PRODUCT_NAME IN ('A', 'B') THEN 1 ELSE 0 END) AS AB, SUM(CASE WHEN A.PRODUCT_NAME = 'C' THEN 1 ELSE 0 END) AS C FROM ORDERS A JOIN CUSTOMERS B ON A.CUSTOMER_ID = B.CUSTOMER_ID GROUP BY A.CUSTOMER_ID) SELECT CUSTOMER_ID, CUSTOMER_NAME FROM TEMP WHERE AB >= 2 AND C = 0"
sql2 = "SELECT CUSTOMER_ID, CUSTOMER_NAME FROM CUSTOMERS WHERE CUSTOMER_ID IN (SELECT DISTINCT CUSTOMER_ID FROM ORDERS WHERE PRODUCT_NAME = 'A') AND CUSTOMER_ID IN (SELECT DISTINCT CUSTOMER_ID FROM ORDERS WHERE PRODUCT_NAME = 'B') AND CUSTOMER_ID NOT IN (SELECT DISTINCT CUSTOMER_ID FROM ORDERS WHERE PRODUCT_NAME = 'C') ORDER BY CUSTOMER_ID"

# define z3 Sorts
__TupleSort = DeclareSort("TupleSort")  # define `Tuple` sort
__Int = IntSort()  # define `Int` sort
__String = StringSort()  # define `String` sort
__Boolean = BoolSort()  # define `Boolean` sort

# Special functions
DELETED = Function("DELETED", __TupleSort, __Boolean)  # define `DELETE` function to represent a tuple does not exist; Not(DELETE) means the existence of a tuple
NULL = Function("NULL", __TupleSort, __String, __Boolean)  # define `NULL` function
COUNT = Function("COUNT", __TupleSort, __String, __Int)  # define `COUNT` function
MAX = Function("MAX", __TupleSort, __String, __Int)  # define `MAX` function
MIN = Function("MIN", __TupleSort, __String, __Int)  # define `MIN` function
AVG = Function("AVG", __TupleSort, __String, __Int)  # define `AVG` function
SUM = Function("SUM", __TupleSort, __String, __Int)  # define `SUM` function
ROUND = Function("ROUND", __Int, __Int, __Int, __Int)  # define `ROUND` (uninterpreted) function
CUSTOMERS__CUSTOMER_ID = Function('CUSTOMERS__CUSTOMER_ID', __TupleSort, __Int)  # define `CUSTOMERS__CUSTOMER_ID` function to retrieve columns of tuples
CUSTOMERS__CUSTOMER_NAME = Function('CUSTOMERS__CUSTOMER_NAME', __TupleSort, __Int)  # define `CUSTOMERS__CUSTOMER_NAME` function to retrieve columns of tuples
ORDERS__ORDER_ID = Function('ORDERS__ORDER_ID', __TupleSort, __Int)  # define `ORDERS__ORDER_ID` function to retrieve columns of tuples
ORDERS__CUSTOMER_ID = Function('ORDERS__CUSTOMER_ID', __TupleSort, __Int)  # define `ORDERS__CUSTOMER_ID` function to retrieve columns of tuples
ORDERS__PRODUCT_NAME = Function('ORDERS__PRODUCT_NAME', __TupleSort, __Int)  # define `ORDERS__PRODUCT_NAME` function to retrieve columns of tuples
TABLE6__AB = Function('TABLE6__AB', __TupleSort, __Int)  # define `TABLE6__AB` function to retrieve columns of tuples
TABLE6__C = Function('TABLE6__C', __TupleSort, __Int)  # define `TABLE6__C` function to retrieve columns of tuples
Table7_GROUP_FUNC = Function('Table7_GROUP_FUNC', __TupleSort, __Int, __Boolean)  # define `Table7_GROUP_FUNC` function to partition tuples into groups

# Special Variables
NULL_VALUE = Const('NULL_VALUE', __Int)  # define NULL variable
POS_INF__Int = Const('POS_INF__Int', __Int)  # define +INF variable
NEG_INF__Int = Const('NEG_INF__Int', __Int)  # define -INF variable
COUNT_ALL__String = Const(f"COUNT_ALL__String", __String)  # define `COUNT(*)`
t1 = Const('t1', __TupleSort)  # define a tuple `t1`
CUSTOMERS__CUSTOMER_ID__String = Const('CUSTOMERS__CUSTOMER_ID__String', __String)  # define `CUSTOMERS__CUSTOMER_ID__String` for NULL function
String_x1__Int = Const('String_x1__Int', __Int)  # define `String_x1__Int` for NULL function
CUSTOMERS__CUSTOMER_NAME__String = Const('CUSTOMERS__CUSTOMER_NAME__String', __String)  # define `CUSTOMERS__CUSTOMER_NAME__String` for NULL function
String_x2__Int = Const('String_x2__Int', __Int)  # define `String_x2__Int` for NULL function
t2 = Const('t2', __TupleSort)  # define a tuple `t2`
String_x3__Int = Const('String_x3__Int', __Int)  # define `String_x3__Int` for NULL function
String_x4__Int = Const('String_x4__Int', __Int)  # define `String_x4__Int` for NULL function
t3 = Const('t3', __TupleSort)  # define a tuple `t3`
ORDERS__ORDER_ID__String = Const('ORDERS__ORDER_ID__String', __String)  # define `ORDERS__ORDER_ID__String` for NULL function
String_x5__Int = Const('String_x5__Int', __Int)  # define `String_x5__Int` for NULL function
ORDERS__CUSTOMER_ID__String = Const('ORDERS__CUSTOMER_ID__String', __String)  # define `ORDERS__CUSTOMER_ID__String` for NULL function
String_x6__Int = Const('String_x6__Int', __Int)  # define `String_x6__Int` for NULL function
ORDERS__PRODUCT_NAME__String = Const('ORDERS__PRODUCT_NAME__String', __String)  # define `ORDERS__PRODUCT_NAME__String` for NULL function
String_x7__Int = Const('String_x7__Int', __Int)  # define `String_x7__Int` for NULL function
t4 = Const('t4', __TupleSort)  # define a tuple `t4`
String_x8__Int = Const('String_x8__Int', __Int)  # define `String_x8__Int` for NULL function
String_x9__Int = Const('String_x9__Int', __Int)  # define `String_x9__Int` for NULL function
String_x10__Int = Const('String_x10__Int', __Int)  # define `String_x10__Int` for NULL function
t5 = Const('t5', __TupleSort)  # define a tuple `t5`
t6 = Const('t6', __TupleSort)  # define a tuple `t6`
t7 = Const('t7', __TupleSort)  # define a tuple `t7`
t8 = Const('t8', __TupleSort)  # define a tuple `t8`
t9 = Const('t9', __TupleSort)  # define a tuple `t9`
t10 = Const('t10', __TupleSort)  # define a tuple `t10`
t11 = Const('t11', __TupleSort)  # define a tuple `t11`
t12 = Const('t12', __TupleSort)  # define a tuple `t12`
String_A__Int = Const('String_A__Int', __Int)  # define `String_A__Int` for NULL function
String_B__Int = Const('String_B__Int', __Int)  # define `String_B__Int` for NULL function
TABLE6__AB__String = Const('TABLE6__AB__String', __String)  # define `TABLE6__AB__String` for NULL function
String_C__Int = Const('String_C__Int', __Int)  # define `String_C__Int` for NULL function
TABLE6__C__String = Const('TABLE6__C__String', __String)  # define `TABLE6__C__String` for NULL function
t13 = Const('t13', __TupleSort)  # define a tuple `t13`
t14 = Const('t14', __TupleSort)  # define a tuple `t14`
t15 = Const('t15', __TupleSort)  # define a tuple `t15`
t16 = Const('t16', __TupleSort)  # define a tuple `t16`
t17 = Const('t17', __TupleSort)  # define a tuple `t17`
t18 = Const('t18', __TupleSort)  # define a tuple `t18`
t19 = Const('t19', __TupleSort)  # define a tuple `t19`
t20 = Const('t20', __TupleSort)  # define a tuple `t20`
t21 = Const('t21', __TupleSort)  # define a tuple `t21`
t22 = Const('t22', __TupleSort)  # define a tuple `t22`
t23 = Const('t23', __TupleSort)  # define a tuple `t23`
t24 = Const('t24', __TupleSort)  # define a tuple `t24`
t25 = Const('t25', __TupleSort)  # define a tuple `t25`
t26 = Const('t26', __TupleSort)  # define a tuple `t26`
t27 = Const('t27', __TupleSort)  # define a tuple `t27`
t28 = Const('t28', __TupleSort)  # define a tuple `t28`
_find_1st_non_deleted_t33 = Const('_find_1st_non_deleted_t33', __TupleSort)  # define a tuple `_find_1st_non_deleted_t33`
_find_1st_non_deleted_t34 = Const('_find_1st_non_deleted_t34', __TupleSort)  # define a tuple `_find_1st_non_deleted_t34`
_find_1st_non_deleted_t35 = Const('_find_1st_non_deleted_t35', __TupleSort)  # define a tuple `_find_1st_non_deleted_t35`
_find_1st_non_deleted_t36 = Const('_find_1st_non_deleted_t36', __TupleSort)  # define a tuple `_find_1st_non_deleted_t36`
_find_1st_non_deleted_t37 = Const('_find_1st_non_deleted_t37', __TupleSort)  # define a tuple `_find_1st_non_deleted_t37`
_find_1st_non_deleted_t38 = Const('_find_1st_non_deleted_t38', __TupleSort)  # define a tuple `_find_1st_non_deleted_t38`
_find_1st_non_deleted_t39 = Const('_find_1st_non_deleted_t39', __TupleSort)  # define a tuple `_find_1st_non_deleted_t39`
_find_1st_non_deleted_t40 = Const('_find_1st_non_deleted_t40', __TupleSort)  # define a tuple `_find_1st_non_deleted_t40`
_find_1st_non_deleted_t41 = Const('_find_1st_non_deleted_t41', __TupleSort)  # define a tuple `_find_1st_non_deleted_t41`
_find_1st_non_deleted_t42 = Const('_find_1st_non_deleted_t42', __TupleSort)  # define a tuple `_find_1st_non_deleted_t42`
_find_1st_non_deleted_t43 = Const('_find_1st_non_deleted_t43', __TupleSort)  # define a tuple `_find_1st_non_deleted_t43`
_find_1st_non_deleted_t44 = Const('_find_1st_non_deleted_t44', __TupleSort)  # define a tuple `_find_1st_non_deleted_t44`
_find_1st_non_deleted_t45 = Const('_find_1st_non_deleted_t45', __TupleSort)  # define a tuple `_find_1st_non_deleted_t45`
_find_1st_non_deleted_t46 = Const('_find_1st_non_deleted_t46', __TupleSort)  # define a tuple `_find_1st_non_deleted_t46`
_find_1st_non_deleted_t47 = Const('_find_1st_non_deleted_t47', __TupleSort)  # define a tuple `_find_1st_non_deleted_t47`
_find_1st_non_deleted_t48 = Const('_find_1st_non_deleted_t48', __TupleSort)  # define a tuple `_find_1st_non_deleted_t48`
_find_1st_non_deleted_t49 = Const('_find_1st_non_deleted_t49', __TupleSort)  # define a tuple `_find_1st_non_deleted_t49`
_find_1st_non_deleted_t50 = Const('_find_1st_non_deleted_t50', __TupleSort)  # define a tuple `_find_1st_non_deleted_t50`
_find_1st_non_deleted_t51 = Const('_find_1st_non_deleted_t51', __TupleSort)  # define a tuple `_find_1st_non_deleted_t51`
_find_1st_non_deleted_t52 = Const('_find_1st_non_deleted_t52', __TupleSort)  # define a tuple `_find_1st_non_deleted_t52`
_find_1st_non_deleted_t53 = Const('_find_1st_non_deleted_t53', __TupleSort)  # define a tuple `_find_1st_non_deleted_t53`
_find_1st_non_deleted_t54 = Const('_find_1st_non_deleted_t54', __TupleSort)  # define a tuple `_find_1st_non_deleted_t54`
_find_1st_non_deleted_t55 = Const('_find_1st_non_deleted_t55', __TupleSort)  # define a tuple `_find_1st_non_deleted_t55`
_find_1st_non_deleted_t56 = Const('_find_1st_non_deleted_t56', __TupleSort)  # define a tuple `_find_1st_non_deleted_t56`
_find_1st_non_deleted_t57 = Const('_find_1st_non_deleted_t57', __TupleSort)  # define a tuple `_find_1st_non_deleted_t57`
_find_1st_non_deleted_t58 = Const('_find_1st_non_deleted_t58', __TupleSort)  # define a tuple `_find_1st_non_deleted_t58`
_find_1st_non_deleted_t59 = Const('_find_1st_non_deleted_t59', __TupleSort)  # define a tuple `_find_1st_non_deleted_t59`
_find_1st_non_deleted_t60 = Const('_find_1st_non_deleted_t60', __TupleSort)  # define a tuple `_find_1st_non_deleted_t60`
_find_1st_non_deleted_t61 = Const('_find_1st_non_deleted_t61', __TupleSort)  # define a tuple `_find_1st_non_deleted_t61`
_find_1st_non_deleted_t62 = Const('_find_1st_non_deleted_t62', __TupleSort)  # define a tuple `_find_1st_non_deleted_t62`
_find_1st_non_deleted_t63 = Const('_find_1st_non_deleted_t63', __TupleSort)  # define a tuple `_find_1st_non_deleted_t63`
_find_1st_non_deleted_t64 = Const('_find_1st_non_deleted_t64', __TupleSort)  # define a tuple `_find_1st_non_deleted_t64`
_find_1st_non_deleted_t65 = Const('_find_1st_non_deleted_t65', __TupleSort)  # define a tuple `_find_1st_non_deleted_t65`
_find_1st_non_deleted_t66 = Const('_find_1st_non_deleted_t66', __TupleSort)  # define a tuple `_find_1st_non_deleted_t66`
_find_1st_non_deleted_t67 = Const('_find_1st_non_deleted_t67', __TupleSort)  # define a tuple `_find_1st_non_deleted_t67`
_find_1st_non_deleted_t68 = Const('_find_1st_non_deleted_t68', __TupleSort)  # define a tuple `_find_1st_non_deleted_t68`
_find_1st_non_deleted_t69 = Const('_find_1st_non_deleted_t69', __TupleSort)  # define a tuple `_find_1st_non_deleted_t69`
_find_1st_non_deleted_t70 = Const('_find_1st_non_deleted_t70', __TupleSort)  # define a tuple `_find_1st_non_deleted_t70`
_find_1st_non_deleted_t71 = Const('_find_1st_non_deleted_t71', __TupleSort)  # define a tuple `_find_1st_non_deleted_t71`
_find_1st_non_deleted_t72 = Const('_find_1st_non_deleted_t72', __TupleSort)  # define a tuple `_find_1st_non_deleted_t72`
_find_1st_non_deleted_t73 = Const('_find_1st_non_deleted_t73', __TupleSort)  # define a tuple `_find_1st_non_deleted_t73`
_find_1st_non_deleted_t74 = Const('_find_1st_non_deleted_t74', __TupleSort)  # define a tuple `_find_1st_non_deleted_t74`
_find_1st_non_deleted_t75 = Const('_find_1st_non_deleted_t75', __TupleSort)  # define a tuple `_find_1st_non_deleted_t75`
_find_1st_non_deleted_t76 = Const('_find_1st_non_deleted_t76', __TupleSort)  # define a tuple `_find_1st_non_deleted_t76`
_find_1st_non_deleted_t77 = Const('_find_1st_non_deleted_t77', __TupleSort)  # define a tuple `_find_1st_non_deleted_t77`
String_A__Int = Const('String_A__Int', __Int)  # define `String_A__Int` for NULL function
t78 = Const('t78', __TupleSort)  # define a tuple `t78`
t79 = Const('t79', __TupleSort)  # define a tuple `t79`
t82 = Const('t82', __TupleSort)  # define a tuple `t82`
t83 = Const('t83', __TupleSort)  # define a tuple `t83`
String_B__Int = Const('String_B__Int', __Int)  # define `String_B__Int` for NULL function
t84 = Const('t84', __TupleSort)  # define a tuple `t84`
t85 = Const('t85', __TupleSort)  # define a tuple `t85`
t88 = Const('t88', __TupleSort)  # define a tuple `t88`
t89 = Const('t89', __TupleSort)  # define a tuple `t89`
String_C__Int = Const('String_C__Int', __Int)  # define `String_C__Int` for NULL function
t90 = Const('t90', __TupleSort)  # define a tuple `t90`
t91 = Const('t91', __TupleSort)  # define a tuple `t91`
t94 = Const('t94', __TupleSort)  # define a tuple `t94`
t95 = Const('t95', __TupleSort)  # define a tuple `t95`
t96 = Const('t96', __TupleSort)  # define a tuple `t96`
t97 = Const('t97', __TupleSort)  # define a tuple `t97`
t98 = Const('t98', __TupleSort)  # define a tuple `t98`
t99 = Const('t99', __TupleSort)  # define a tuple `t99`
_orderby_t102 = Const('_orderby_t102', __TupleSort)  # define a tuple `_orderby_t102`
_orderby_t103 = Const('_orderby_t103', __TupleSort)  # define a tuple `_orderby_t103`
_orderby_t104 = Const('_orderby_t104', __TupleSort)  # define a tuple `_orderby_t104`
_orderby_t105 = Const('_orderby_t105', __TupleSort)  # define a tuple `_orderby_t105`
_orderby_t106 = Const('_orderby_t106', __TupleSort)  # define a tuple `_orderby_t106`
_orderby_t107 = Const('_orderby_t107', __TupleSort)  # define a tuple `_orderby_t107`

def _MAX(*args):
    return functools.reduce(lambda x, y: If(x >= y, x, y), args)


def _MIN(*args):
    return functools.reduce(lambda x, y: If(x < y, x, y), args)

DBMS_facts = And(
# Database tuples
Not(DELETED(t1)),
CUSTOMERS__CUSTOMER_ID(t1) == String_x1__Int,
CUSTOMERS__CUSTOMER_NAME(t1) == String_x2__Int,
Not(DELETED(t2)),
CUSTOMERS__CUSTOMER_ID(t2) == String_x3__Int,
CUSTOMERS__CUSTOMER_NAME(t2) == String_x4__Int,
-2147483648 <= CUSTOMERS__CUSTOMER_ID(t1),
2147483647 >= CUSTOMERS__CUSTOMER_ID(t1),
2147483647 < CUSTOMERS__CUSTOMER_NAME(t1),
-2147483648 <= CUSTOMERS__CUSTOMER_ID(t2),
2147483647 >= CUSTOMERS__CUSTOMER_ID(t2),
2147483647 < CUSTOMERS__CUSTOMER_NAME(t2),
Not(DELETED(t3)),
ORDERS__ORDER_ID(t3) == String_x5__Int,
ORDERS__CUSTOMER_ID(t3) == String_x6__Int,
ORDERS__PRODUCT_NAME(t3) == String_x7__Int,
Not(DELETED(t4)),
ORDERS__ORDER_ID(t4) == String_x8__Int,
ORDERS__CUSTOMER_ID(t4) == String_x9__Int,
ORDERS__PRODUCT_NAME(t4) == String_x10__Int,
-2147483648 <= ORDERS__ORDER_ID(t3),
2147483647 >= ORDERS__ORDER_ID(t3),
-2147483648 <= ORDERS__CUSTOMER_ID(t3),
2147483647 >= ORDERS__CUSTOMER_ID(t3),
2147483647 < ORDERS__PRODUCT_NAME(t3),
-2147483648 <= ORDERS__ORDER_ID(t4),
2147483647 >= ORDERS__ORDER_ID(t4),
-2147483648 <= ORDERS__CUSTOMER_ID(t4),
2147483647 >= ORDERS__CUSTOMER_ID(t4),
2147483647 < ORDERS__PRODUCT_NAME(t4),
And(Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
    Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
    CUSTOMERS__CUSTOMER_ID(t1) != CUSTOMERS__CUSTOMER_ID(t2)),
And(Not(NULL(t3, ORDERS__ORDER_ID__String)),
    Not(NULL(t4, ORDERS__ORDER_ID__String)),
    ORDERS__ORDER_ID(t3) != ORDERS__ORDER_ID(t4)),
And(Or(And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
           Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
           ORDERS__CUSTOMER_ID(t3) ==
           CUSTOMERS__CUSTOMER_ID(t1)),
       And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
           Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
           ORDERS__CUSTOMER_ID(t3) ==
           CUSTOMERS__CUSTOMER_ID(t2))),
    Or(And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
           Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
           ORDERS__CUSTOMER_ID(t4) ==
           CUSTOMERS__CUSTOMER_ID(t1)),
       And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
           Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
           ORDERS__CUSTOMER_ID(t4) ==
           CUSTOMERS__CUSTOMER_ID(t2)))),
2226998246699711722 == String_A__Int,
3019904332333333563 == String_B__Int,
8181935414401778503 == String_C__Int,
2226998246699711722 == String_A__Int,
3019904332333333563 == String_B__Int,
8181935414401778503 == String_C__Int
)

premise1 = And(
# 1st SQL query formulas
# t5 := InnerJoin(t3, t1, None)
And(
    Implies(
        And(Not(DELETED(t3)), Not(DELETED(t1))),
        And(
            Not(DELETED(t5)),
            And(NULL(t5, ORDERS__ORDER_ID__String) ==
    NULL(t3, ORDERS__ORDER_ID__String),
    ORDERS__ORDER_ID(t5) == ORDERS__ORDER_ID(t3)),
And(NULL(t5, ORDERS__CUSTOMER_ID__String) ==
    NULL(t3, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t5) == ORDERS__CUSTOMER_ID(t3)),
And(NULL(t5, ORDERS__PRODUCT_NAME__String) ==
    NULL(t3, ORDERS__PRODUCT_NAME__String),
    ORDERS__PRODUCT_NAME(t5) == ORDERS__PRODUCT_NAME(t3)),
And(NULL(t5, CUSTOMERS__CUSTOMER_ID__String) ==
    NULL(t1, CUSTOMERS__CUSTOMER_ID__String),
    CUSTOMERS__CUSTOMER_ID(t5) == CUSTOMERS__CUSTOMER_ID(t1)),
And(NULL(t5, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t1, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t5) ==
    CUSTOMERS__CUSTOMER_NAME(t1)),
        )
    ),
    Implies(
        Not(And(Not(DELETED(t3)), Not(DELETED(t1)))),
        DELETED(t5),
    ),
),

# t6 := InnerJoin(t4, t1, None)
And(
    Implies(
        And(Not(DELETED(t4)), Not(DELETED(t1))),
        And(
            Not(DELETED(t6)),
            And(NULL(t6, ORDERS__ORDER_ID__String) ==
    NULL(t4, ORDERS__ORDER_ID__String),
    ORDERS__ORDER_ID(t6) == ORDERS__ORDER_ID(t4)),
And(NULL(t6, ORDERS__CUSTOMER_ID__String) ==
    NULL(t4, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t6) == ORDERS__CUSTOMER_ID(t4)),
And(NULL(t6, ORDERS__PRODUCT_NAME__String) ==
    NULL(t4, ORDERS__PRODUCT_NAME__String),
    ORDERS__PRODUCT_NAME(t6) == ORDERS__PRODUCT_NAME(t4)),
And(NULL(t6, CUSTOMERS__CUSTOMER_ID__String) ==
    NULL(t1, CUSTOMERS__CUSTOMER_ID__String),
    CUSTOMERS__CUSTOMER_ID(t6) == CUSTOMERS__CUSTOMER_ID(t1)),
And(NULL(t6, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t1, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t6) ==
    CUSTOMERS__CUSTOMER_NAME(t1)),
        )
    ),
    Implies(
        Not(And(Not(DELETED(t4)), Not(DELETED(t1)))),
        DELETED(t6),
    ),
),

# t7 := InnerJoin(t3, t2, None)
And(
    Implies(
        And(Not(DELETED(t3)), Not(DELETED(t2))),
        And(
            Not(DELETED(t7)),
            And(NULL(t7, ORDERS__ORDER_ID__String) ==
    NULL(t3, ORDERS__ORDER_ID__String),
    ORDERS__ORDER_ID(t7) == ORDERS__ORDER_ID(t3)),
And(NULL(t7, ORDERS__CUSTOMER_ID__String) ==
    NULL(t3, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t7) == ORDERS__CUSTOMER_ID(t3)),
And(NULL(t7, ORDERS__PRODUCT_NAME__String) ==
    NULL(t3, ORDERS__PRODUCT_NAME__String),
    ORDERS__PRODUCT_NAME(t7) == ORDERS__PRODUCT_NAME(t3)),
And(NULL(t7, CUSTOMERS__CUSTOMER_ID__String) ==
    NULL(t2, CUSTOMERS__CUSTOMER_ID__String),
    CUSTOMERS__CUSTOMER_ID(t7) == CUSTOMERS__CUSTOMER_ID(t2)),
And(NULL(t7, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t2, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t7) ==
    CUSTOMERS__CUSTOMER_NAME(t2)),
        )
    ),
    Implies(
        Not(And(Not(DELETED(t3)), Not(DELETED(t2)))),
        DELETED(t7),
    ),
),

# t8 := InnerJoin(t4, t2, None)
And(
    Implies(
        And(Not(DELETED(t4)), Not(DELETED(t2))),
        And(
            Not(DELETED(t8)),
            And(NULL(t8, ORDERS__ORDER_ID__String) ==
    NULL(t4, ORDERS__ORDER_ID__String),
    ORDERS__ORDER_ID(t8) == ORDERS__ORDER_ID(t4)),
And(NULL(t8, ORDERS__CUSTOMER_ID__String) ==
    NULL(t4, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t8) == ORDERS__CUSTOMER_ID(t4)),
And(NULL(t8, ORDERS__PRODUCT_NAME__String) ==
    NULL(t4, ORDERS__PRODUCT_NAME__String),
    ORDERS__PRODUCT_NAME(t8) == ORDERS__PRODUCT_NAME(t4)),
And(NULL(t8, CUSTOMERS__CUSTOMER_ID__String) ==
    NULL(t2, CUSTOMERS__CUSTOMER_ID__String),
    CUSTOMERS__CUSTOMER_ID(t8) == CUSTOMERS__CUSTOMER_ID(t2)),
And(NULL(t8, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t2, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t8) ==
    CUSTOMERS__CUSTOMER_NAME(t2)),
        )
    ),
    Implies(
        Not(And(Not(DELETED(t4)), Not(DELETED(t2)))),
        DELETED(t8),
    ),
),

# t9 := Filter(['t5'], Cond=(eq_FExpressionTuple(NULL=NULL(t3, ORDERS__CUSTOMER_ID__String), VALUE=ORDERS__CUSTOMER_ID(t3))_FExpressionTuple(NULL=NULL(t1, CUSTOMERS__CUSTOMER_ID__String), VALUE=CUSTOMERS__CUSTOMER_ID(t1))))
And(
    Implies(
        And(*[Not(DELETED(t5)), If(Or(NULL(t3, ORDERS__CUSTOMER_ID__String),
      NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t3) == CUSTOMERS__CUSTOMER_ID(t1)))]),
        And(Not(DELETED(t9)), t9 == t5),
    ),
    Implies(Not(And(*[Not(DELETED(t5)), If(Or(NULL(t3, ORDERS__CUSTOMER_ID__String),
      NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t3) == CUSTOMERS__CUSTOMER_ID(t1)))])), DELETED(t9)),
),

# t10 := Filter(['t6'], Cond=(eq_FExpressionTuple(NULL=NULL(t4, ORDERS__CUSTOMER_ID__String), VALUE=ORDERS__CUSTOMER_ID(t4))_FExpressionTuple(NULL=NULL(t1, CUSTOMERS__CUSTOMER_ID__String), VALUE=CUSTOMERS__CUSTOMER_ID(t1))))
And(
    Implies(
        And(*[Not(DELETED(t6)), If(Or(NULL(t4, ORDERS__CUSTOMER_ID__String),
      NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t4) == CUSTOMERS__CUSTOMER_ID(t1)))]),
        And(Not(DELETED(t10)), t10 == t6),
    ),
    Implies(Not(And(*[Not(DELETED(t6)), If(Or(NULL(t4, ORDERS__CUSTOMER_ID__String),
      NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t1, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t4) == CUSTOMERS__CUSTOMER_ID(t1)))])), DELETED(t10)),
),

# t11 := Filter(['t7'], Cond=(eq_FExpressionTuple(NULL=NULL(t3, ORDERS__CUSTOMER_ID__String), VALUE=ORDERS__CUSTOMER_ID(t3))_FExpressionTuple(NULL=NULL(t2, CUSTOMERS__CUSTOMER_ID__String), VALUE=CUSTOMERS__CUSTOMER_ID(t2))))
And(
    Implies(
        And(*[Not(DELETED(t7)), If(Or(NULL(t3, ORDERS__CUSTOMER_ID__String),
      NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t3) == CUSTOMERS__CUSTOMER_ID(t2)))]),
        And(Not(DELETED(t11)), t11 == t7),
    ),
    Implies(Not(And(*[Not(DELETED(t7)), If(Or(NULL(t3, ORDERS__CUSTOMER_ID__String),
      NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t3, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t3) == CUSTOMERS__CUSTOMER_ID(t2)))])), DELETED(t11)),
),

# t12 := Filter(['t8'], Cond=(eq_FExpressionTuple(NULL=NULL(t4, ORDERS__CUSTOMER_ID__String), VALUE=ORDERS__CUSTOMER_ID(t4))_FExpressionTuple(NULL=NULL(t2, CUSTOMERS__CUSTOMER_ID__String), VALUE=CUSTOMERS__CUSTOMER_ID(t2))))
And(
    Implies(
        And(*[Not(DELETED(t8)), If(Or(NULL(t4, ORDERS__CUSTOMER_ID__String),
      NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t4) == CUSTOMERS__CUSTOMER_ID(t2)))]),
        And(Not(DELETED(t12)), t12 == t8),
    ),
    Implies(Not(And(*[Not(DELETED(t8)), If(Or(NULL(t4, ORDERS__CUSTOMER_ID__String),
      NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
   False,
   And(Not(NULL(t4, ORDERS__CUSTOMER_ID__String)),
       Not(NULL(t2, CUSTOMERS__CUSTOMER_ID__String)),
       ORDERS__CUSTOMER_ID(t4) == CUSTOMERS__CUSTOMER_ID(t2)))])), DELETED(t12)),
),

# t13 := GroupReduce(['t9', 't10', 't11', 't12'])
And(
    Implies(
        Or(Table7_GROUP_FUNC(t9, 0),
   Table7_GROUP_FUNC(t10, 0),
   Table7_GROUP_FUNC(t11, 0),
   Table7_GROUP_FUNC(t12, 0)),
        And(
            Not(DELETED(t13)),
            And(
And(NULL(t13, ORDERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t39, ORDERS__CUSTOMER_ID__String),
ORDERS__CUSTOMER_ID(t13) ==
ORDERS__CUSTOMER_ID(_find_1st_non_deleted_t39)),
And(NULL(t13, CUSTOMERS__CUSTOMER_NAME__String) ==
NULL(_find_1st_non_deleted_t39,
     CUSTOMERS__CUSTOMER_NAME__String),
CUSTOMERS__CUSTOMER_NAME(t13) ==
CUSTOMERS__CUSTOMER_NAME(_find_1st_non_deleted_t39)),
And(NULL(t13, TABLE6__AB__String) ==
And(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
    Or(DELETED(t10), False, Not(Table7_GROUP_FUNC(t10, 0))),
    Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 0))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 0)))),
TABLE6__AB(t13) ==
If(And(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
       Or(DELETED(t10),
          False,
          Not(Table7_GROUP_FUNC(t10, 0))),
       Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 0))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 0)))),
   -10,
   If(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
      0,
      If(And(Not(If(And(Or(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                              False,
                              Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False))),
                           If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int))))),
                              False,
                              Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)))),
                        Or(If(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                                 False,
                                 Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                                 False,
                                 And(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int)))),
                           If(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int))))),
                                 False,
                                 Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int))))),
                                 False,
                                 And(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int)))))),
                    False,
                    Or(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t9,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t9,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))))),
             If(And(Or(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t9,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t9,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))),
                    Or(If(If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                       False,
                                       Not(And(Not(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t9) ==
                                        String_A__Int))))),
                             False,
                             Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
                                   False))),
                          False,
                          If(And(Or(Or(NULL(t9,
                                        ORDERS__PRODUCT_NAME__String),
...),
And(NULL(t13, TABLE6__C__String) ==
And(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
    Or(DELETED(t10), False, Not(Table7_GROUP_FUNC(t10, 0))),
    Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 0))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 0)))),
TABLE6__C(t13) ==
If(And(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
       Or(DELETED(t10),
          False,
          Not(Table7_GROUP_FUNC(t10, 0))),
       Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 0))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 0)))),
   -10,
   If(Or(DELETED(t9), False, Not(Table7_GROUP_FUNC(t9, 0))),
      0,
      If(And(Not(Or(NULL(t9, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t9, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t9) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t10),
         False,
         Not(Table7_GROUP_FUNC(t10, 0))),
      0,
      If(And(Not(Or(NULL(t10, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t10, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t10) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t11),
         False,
         Not(Table7_GROUP_FUNC(t11, 0))),
      0,
      If(And(Not(Or(NULL(t11, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t11, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t11) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t12),
         False,
         Not(Table7_GROUP_FUNC(t12, 0))),
      0,
      If(And(Not(Or(NULL(t12, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t12, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t12) == String_C__Int)),
         1,
         0)))),
And(NULL(t13, ORDERS__ORDER_ID__String) ==
NULL(_find_1st_non_deleted_t53, ORDERS__ORDER_ID__String),
ORDERS__ORDER_ID(t13) ==
ORDERS__ORDER_ID(_find_1st_non_deleted_t53)),
And(NULL(t13, ORDERS__PRODUCT_NAME__String) ==
NULL(_find_1st_non_deleted_t53,
     ORDERS__PRODUCT_NAME__String),
ORDERS__PRODUCT_NAME(t13) ==
ORDERS__PRODUCT_NAME(_find_1st_non_deleted_t53)),
And(NULL(t13, CUSTOMERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t53,
     CUSTOMERS__CUSTOMER_ID__String),
CUSTOMERS__CUSTOMER_ID(t13) ==
CUSTOMERS__CUSTOMER_ID(_find_1st_non_deleted_t53)),

            ),
        ),
    ),
    Implies(
        Not(Or(Table7_GROUP_FUNC(t9, 0),
   Table7_GROUP_FUNC(t10, 0),
   Table7_GROUP_FUNC(t11, 0),
   Table7_GROUP_FUNC(t12, 0))),
        DELETED(t13),
    ),
),

# t14 := GroupReduce(['t10', 't11', 't12'])
And(
    Implies(
        Or(Table7_GROUP_FUNC(t10, 1),
   Table7_GROUP_FUNC(t11, 1),
   Table7_GROUP_FUNC(t12, 1)),
        And(
            Not(DELETED(t14)),
            And(
And(NULL(t14, ORDERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t58, ORDERS__CUSTOMER_ID__String),
ORDERS__CUSTOMER_ID(t14) ==
ORDERS__CUSTOMER_ID(_find_1st_non_deleted_t58)),
And(NULL(t14, CUSTOMERS__CUSTOMER_NAME__String) ==
NULL(_find_1st_non_deleted_t58,
     CUSTOMERS__CUSTOMER_NAME__String),
CUSTOMERS__CUSTOMER_NAME(t14) ==
CUSTOMERS__CUSTOMER_NAME(_find_1st_non_deleted_t58)),
And(NULL(t14, TABLE6__AB__String) ==
And(Or(DELETED(t10), False, Not(Table7_GROUP_FUNC(t10, 1))),
    Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 1))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 1)))),
TABLE6__AB(t14) ==
If(And(Or(DELETED(t10),
          False,
          Not(Table7_GROUP_FUNC(t10, 1))),
       Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 1))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 1)))),
   -10,
   If(Or(DELETED(t10),
         False,
         Not(Table7_GROUP_FUNC(t10, 1))),
      0,
      If(And(Not(If(And(Or(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                              False,
                              Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False))),
                           If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int))))),
                              False,
                              Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)))),
                        Or(If(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                                 False,
                                 Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                                 False,
                                 And(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int)))),
                           If(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int))))),
                                 False,
                                 Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int))))),
                                 False,
                                 And(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int)))))),
                    False,
                    Or(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t10,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t10,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))))),
             If(And(Or(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t10,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t10,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))),
                    Or(If(If(And(Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                       False,
                                       Not(And(Not(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t10) ==
                                        String_A__Int))))),
                             False,
                             Or(Or(NULL(t10,
                                        ORDERS__PRODUCT_NAME__String),
                                   False))),
                          False,
                          If(And(Or(Or(NULL(t10,
...),
And(NULL(t14, TABLE6__C__String) ==
And(Or(DELETED(t10), False, Not(Table7_GROUP_FUNC(t10, 1))),
    Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 1))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 1)))),
TABLE6__C(t14) ==
If(And(Or(DELETED(t10),
          False,
          Not(Table7_GROUP_FUNC(t10, 1))),
       Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 1))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 1)))),
   -10,
   If(Or(DELETED(t10),
         False,
         Not(Table7_GROUP_FUNC(t10, 1))),
      0,
      If(And(Not(Or(NULL(t10, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t10, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t10) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t11),
         False,
         Not(Table7_GROUP_FUNC(t11, 1))),
      0,
      If(And(Not(Or(NULL(t11, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t11, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t11) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t12),
         False,
         Not(Table7_GROUP_FUNC(t12, 1))),
      0,
      If(And(Not(Or(NULL(t12, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t12, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t12) == String_C__Int)),
         1,
         0)))),
And(NULL(t14, ORDERS__ORDER_ID__String) ==
NULL(_find_1st_non_deleted_t68, ORDERS__ORDER_ID__String),
ORDERS__ORDER_ID(t14) ==
ORDERS__ORDER_ID(_find_1st_non_deleted_t68)),
And(NULL(t14, ORDERS__PRODUCT_NAME__String) ==
NULL(_find_1st_non_deleted_t68,
     ORDERS__PRODUCT_NAME__String),
ORDERS__PRODUCT_NAME(t14) ==
ORDERS__PRODUCT_NAME(_find_1st_non_deleted_t68)),
And(NULL(t14, CUSTOMERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t68,
     CUSTOMERS__CUSTOMER_ID__String),
CUSTOMERS__CUSTOMER_ID(t14) ==
CUSTOMERS__CUSTOMER_ID(_find_1st_non_deleted_t68)),

            ),
        ),
    ),
    Implies(
        Not(Or(Table7_GROUP_FUNC(t10, 1),
   Table7_GROUP_FUNC(t11, 1),
   Table7_GROUP_FUNC(t12, 1))),
        DELETED(t14),
    ),
),

# t15 := GroupReduce(['t11', 't12'])
And(
    Implies(
        Or(Table7_GROUP_FUNC(t11, 2), Table7_GROUP_FUNC(t12, 2)),
        And(
            Not(DELETED(t15)),
            And(
And(NULL(t15, ORDERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t71, ORDERS__CUSTOMER_ID__String),
ORDERS__CUSTOMER_ID(t15) ==
ORDERS__CUSTOMER_ID(_find_1st_non_deleted_t71)),
And(NULL(t15, CUSTOMERS__CUSTOMER_NAME__String) ==
NULL(_find_1st_non_deleted_t71,
     CUSTOMERS__CUSTOMER_NAME__String),
CUSTOMERS__CUSTOMER_NAME(t15) ==
CUSTOMERS__CUSTOMER_NAME(_find_1st_non_deleted_t71)),
And(NULL(t15, TABLE6__AB__String) ==
And(Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 2))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 2)))),
TABLE6__AB(t15) ==
If(And(Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 2))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 2)))),
   -10,
   If(Or(DELETED(t11),
         False,
         Not(Table7_GROUP_FUNC(t11, 2))),
      0,
      If(And(Not(If(And(Or(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                              False,
                              Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False))),
                           If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int))))),
                              False,
                              Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)))),
                        Or(If(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                                 False,
                                 Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                                 False,
                                 And(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int)))),
                           If(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int))))),
                                 False,
                                 Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int))))),
                                 False,
                                 And(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int)))))),
                    False,
                    Or(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t11,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t11,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))))),
             If(And(Or(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t11,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t11,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))),
                    Or(If(If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                       False,
                                       Not(And(Not(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t11) ==
                                        String_A__Int))))),
                             False,
                             Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                   False))),
                          False,
                          If(And(Or(Or(NULL(t11,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t11,
...),
And(NULL(t15, TABLE6__C__String) ==
And(Or(DELETED(t11), False, Not(Table7_GROUP_FUNC(t11, 2))),
    Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 2)))),
TABLE6__C(t15) ==
If(And(Or(DELETED(t11),
          False,
          Not(Table7_GROUP_FUNC(t11, 2))),
       Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 2)))),
   -10,
   If(Or(DELETED(t11),
         False,
         Not(Table7_GROUP_FUNC(t11, 2))),
      0,
      If(And(Not(Or(NULL(t11, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t11, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t11) == String_C__Int)),
         1,
         0)) +
   If(Or(DELETED(t12),
         False,
         Not(Table7_GROUP_FUNC(t12, 2))),
      0,
      If(And(Not(Or(NULL(t12, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t12, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t12) == String_C__Int)),
         1,
         0)))),
And(NULL(t15, ORDERS__ORDER_ID__String) ==
NULL(_find_1st_non_deleted_t77, ORDERS__ORDER_ID__String),
ORDERS__ORDER_ID(t15) ==
ORDERS__ORDER_ID(_find_1st_non_deleted_t77)),
And(NULL(t15, ORDERS__PRODUCT_NAME__String) ==
NULL(_find_1st_non_deleted_t77,
     ORDERS__PRODUCT_NAME__String),
ORDERS__PRODUCT_NAME(t15) ==
ORDERS__PRODUCT_NAME(_find_1st_non_deleted_t77)),
And(NULL(t15, CUSTOMERS__CUSTOMER_ID__String) ==
NULL(_find_1st_non_deleted_t77,
     CUSTOMERS__CUSTOMER_ID__String),
CUSTOMERS__CUSTOMER_ID(t15) ==
CUSTOMERS__CUSTOMER_ID(_find_1st_non_deleted_t77)),

            ),
        ),
    ),
    Implies(
        Not(Or(Table7_GROUP_FUNC(t11, 2), Table7_GROUP_FUNC(t12, 2))),
        DELETED(t15),
    ),
),

# t16 := GroupReduce(['t12'])
And(
    Implies(
        Or(Table7_GROUP_FUNC(t12, 3)),
        And(
            Not(DELETED(t16)),
            And(
And(NULL(t16, ORDERS__CUSTOMER_ID__String) ==
NULL(t12, ORDERS__CUSTOMER_ID__String),
ORDERS__CUSTOMER_ID(t16) == ORDERS__CUSTOMER_ID(t12)),
And(NULL(t16, CUSTOMERS__CUSTOMER_NAME__String) ==
NULL(t12, CUSTOMERS__CUSTOMER_NAME__String),
CUSTOMERS__CUSTOMER_NAME(t16) ==
CUSTOMERS__CUSTOMER_NAME(t12)),
And(NULL(t16, TABLE6__AB__String) ==
And(Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 3)))),
TABLE6__AB(t16) ==
If(And(Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 3)))),
   -10,
   If(Or(DELETED(t12),
         False,
         Not(Table7_GROUP_FUNC(t12, 3))),
      0,
      If(And(Not(If(And(Or(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                              False,
                              Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False))),
                           If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                  Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int))))),
                              False,
                              Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)))),
                        Or(If(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                                 False,
                                 Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                                 False,
                                 And(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int)))),
                           If(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int))))),
                                 False,
                                 Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False))),
                              False,
                              If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False)),
                                     Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                        False,
                                        Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int))))),
                                 False,
                                 And(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int)))))),
                    False,
                    Or(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t12,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t12,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))))),
             If(And(Or(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                          False,
                          Or(Or(NULL(t12,
                                     ORDERS__PRODUCT_NAME__String),
                                False))),
                       If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                    False)),
                              Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False),
                                    False,
                                    Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_B__Int))))),
                          False,
                          Or(Or(NULL(t12,
                                     ORDERS__PRODUCT_NAME__String),
                                False)))),
                    Or(If(If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                       False,
                                       Not(And(Not(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String)),
                                        Not(False),
                                        ORDERS__PRODUCT_NAME(t12) ==
                                        String_A__Int))))),
                             False,
                             Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                   False))),
                          False,
                          If(And(Or(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                       False)),
                                 Or(If(Or(NULL(t12,
                                        ORDERS__PRODUCT_NAME__String),
                                        False),
                                       False,
...),
And(NULL(t16, TABLE6__C__String) ==
And(Or(DELETED(t12), False, Not(Table7_GROUP_FUNC(t12, 3)))),
TABLE6__C(t16) ==
If(And(Or(DELETED(t12),
          False,
          Not(Table7_GROUP_FUNC(t12, 3)))),
   -10,
   If(Or(DELETED(t12),
         False,
         Not(Table7_GROUP_FUNC(t12, 3))),
      0,
      If(And(Not(Or(NULL(t12, ORDERS__PRODUCT_NAME__String),
                    False)),
             And(Not(NULL(t12, ORDERS__PRODUCT_NAME__String)),
                 Not(False),
                 ORDERS__PRODUCT_NAME(t12) == String_C__Int)),
         1,
         0)))),
And(NULL(t16, ORDERS__ORDER_ID__String) ==
NULL(t12, ORDERS__ORDER_ID__String),
ORDERS__ORDER_ID(t16) == ORDERS__ORDER_ID(t12)),
And(NULL(t16, ORDERS__PRODUCT_NAME__String) ==
NULL(t12, ORDERS__PRODUCT_NAME__String),
ORDERS__PRODUCT_NAME(t16) == ORDERS__PRODUCT_NAME(t12)),
And(NULL(t16, CUSTOMERS__CUSTOMER_ID__String) ==
NULL(t12, CUSTOMERS__CUSTOMER_ID__String),
CUSTOMERS__CUSTOMER_ID(t16) == CUSTOMERS__CUSTOMER_ID(t12)),

            ),
        ),
    ),
    Implies(
        Not(Or(Table7_GROUP_FUNC(t12, 3))),
        DELETED(t16),
    ),
),

# Table7 GroupBy constraint
    And(
    If(Table7_GROUP_FUNC(t9, 0), 1, 0) == If(DELETED(t9), 0, 1),
If(Table7_GROUP_FUNC(t10, 0), 1, 0) +
If(Table7_GROUP_FUNC(t10, 1), 1, 0) ==
If(DELETED(t10), 0, 1),
Table7_GROUP_FUNC(t10, 0) ==
And(Not(DELETED(t10)),
    Table7_GROUP_FUNC(t9, 0),
    And(Or(And(NULL(t10, ORDERS__CUSTOMER_ID__String),
               NULL(t9, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t10, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t9, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t10) ==
               ORDERS__CUSTOMER_ID(t9))))),
If(Table7_GROUP_FUNC(t11, 0), 1, 0) +
If(Table7_GROUP_FUNC(t11, 1), 1, 0) +
If(Table7_GROUP_FUNC(t11, 2), 1, 0) ==
If(DELETED(t11), 0, 1),
Table7_GROUP_FUNC(t11, 0) ==
And(Not(DELETED(t11)),
    Table7_GROUP_FUNC(t9, 0),
    And(Or(And(NULL(t11, ORDERS__CUSTOMER_ID__String),
               NULL(t9, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t11, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t9, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t11) ==
               ORDERS__CUSTOMER_ID(t9))))),
Table7_GROUP_FUNC(t11, 1) ==
And(Not(DELETED(t11)),
    Table7_GROUP_FUNC(t10, 1),
    And(Or(And(NULL(t11, ORDERS__CUSTOMER_ID__String),
               NULL(t10, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t11, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t10, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t11) ==
               ORDERS__CUSTOMER_ID(t10))))),
If(Table7_GROUP_FUNC(t12, 0), 1, 0) +
If(Table7_GROUP_FUNC(t12, 1), 1, 0) +
If(Table7_GROUP_FUNC(t12, 2), 1, 0) +
If(Table7_GROUP_FUNC(t12, 3), 1, 0) ==
If(DELETED(t12), 0, 1),
Table7_GROUP_FUNC(t12, 0) ==
And(Not(DELETED(t12)),
    Table7_GROUP_FUNC(t9, 0),
    And(Or(And(NULL(t12, ORDERS__CUSTOMER_ID__String),
               NULL(t9, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t12, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t9, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t12) ==
               ORDERS__CUSTOMER_ID(t9))))),
Table7_GROUP_FUNC(t12, 1) ==
And(Not(DELETED(t12)),
    Table7_GROUP_FUNC(t10, 1),
    And(Or(And(NULL(t12, ORDERS__CUSTOMER_ID__String),
               NULL(t10, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t12, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t10, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t12) ==
               ORDERS__CUSTOMER_ID(t10))))),
Table7_GROUP_FUNC(t12, 2) ==
And(Not(DELETED(t12)),
    Table7_GROUP_FUNC(t11, 2),
    And(Or(And(NULL(t12, ORDERS__CUSTOMER_ID__String),
               NULL(t11, ORDERS__CUSTOMER_ID__String)),
           And(Not(NULL(t12, ORDERS__CUSTOMER_ID__String)),
               Not(NULL(t11, ORDERS__CUSTOMER_ID__String)),
               ORDERS__CUSTOMER_ID(t12) ==
               ORDERS__CUSTOMER_ID(t11))))),
And(_find_1st_non_deleted_t33 == t9,
    _find_1st_non_deleted_t34 == t10,
    _find_1st_non_deleted_t35 == t11,
    _find_1st_non_deleted_t36 == t12,
    If(And(DELETED(_find_1st_non_deleted_t33),
           Not(DELETED(_find_1st_non_deleted_t34))),
       _find_1st_non_deleted_t37 ==
       _find_1st_non_deleted_t34,
       _find_1st_non_deleted_t37 ==
       _find_1st_non_deleted_t33),
    If(And(DELETED(_find_1st_non_deleted_t37),
           Not(DELETED(_find_1st_non_deleted_t35))),
       _find_1st_non_deleted_t38 ==
       _find_1st_non_deleted_t35,
       _find_1st_non_deleted_t38 ==
       _find_1st_non_deleted_t37),
    If(And(DELETED(_find_1st_non_deleted_t38),
           Not(DELETED(_find_1st_non_deleted_t36))),
       _find_1st_non_deleted_t39 ==
       _find_1st_non_deleted_t36,
       _find_1st_non_deleted_t39 ==
       _find_1st_non_deleted_t38)),
And(_find_1st_non_deleted_t40 == t9,
    _find_1st_non_deleted_t41 == t10,
    _find_1st_non_deleted_t42 == t11,
    _find_1st_non_deleted_t43 == t12,
    If(And(DELETED(_find_1st_non_deleted_t40),
           Not(DELETED(_find_1st_non_deleted_t41))),
       _find_1st_non_deleted_t44 ==
       _find_1st_non_deleted_t41,
       _find_1st_non_deleted_t44 ==
       _find_1st_non_deleted_t40),
    If(And(DELETED(_find_1st_non_deleted_t44),
           Not(DELETED(_find_1st_non_deleted_t42))),
       _find_1st_non_deleted_t45 ==
       _find_1st_non_deleted_t42,
       _find_1st_non_deleted_t45 ==
       _find_1st_non_deleted_t44),
    If(And(DELETED(_find_1st_non_deleted_t45),
           Not(DELETED(_find_1st_non_deleted_t43))),
       _find_1st_non_deleted_t46 ==
       _find_1st_non_deleted_t43,
       _find_1st_non_deleted_t46 ==
       _find_1st_non_deleted_t45)),
And(_find_1st_non_deleted_t47 == t9,
    _find_1st_non_deleted_t48 == t10,
    _find_1st_non_deleted_t49 == t11,
    _find_1st_non_deleted_t50 == t12,
    If(And(DELETED(_find_1st_non_deleted_t47),
           Not(DELETED(_find_1st_non_deleted_t48))),
       _find_1st_non_deleted_t51 ==
       _find_1st_non_deleted_t48,
       _find_1st_non_deleted_t51 ==
       _find_1st_non_deleted_t47),
    If(And(DELETED(_find_1st_non_deleted_t51),
           Not(DELETED(_find_1st_non_deleted_t49))),
       _find_1st_non_deleted_t52 ==
       _find_1st_non_deleted_t49,
       _find_1st_non_deleted_t52 ==
       _find_1st_non_deleted_t51),
    If(And(DELETED(_find_1st_non_deleted_t52),
           Not(DELETED(_find_1st_non_deleted_t50))),
       _find_1st_non_deleted_t53 ==
       _find_1st_non_deleted_t50,
       _find_1st_non_deleted_t53 ==
       _find_1st_non_deleted_t52)),
And(_find_1st_non_deleted_t54 == t10,
    _find_1st_non_deleted_t55 == t11,
    _find_1st_non_deleted_t56 == t12,
    If(And(DELETED(_find_1st_non_deleted_t54),
           Not(DELETED(_find_1st_non_deleted_t55))),
       _find_1st_non_deleted_t57 ==
       _find_1st_non_deleted_t55,
       _find_1st_non_deleted_t57 ==
       _find_1st_non_deleted_t54),
    If(And(DELETED(_find_1st_non_deleted_t57),
           Not(DELETED(_find_1st_non_deleted_t56))),
       _find_1st_non_deleted_t58 ==
       _find_1st_non_deleted_t56,
       _find_1st_non_deleted_t58 ==
       _find_1st_non_deleted_t57)),
And(_find_1st_non_deleted_t59 == t10,
    _find_1st_non_deleted_t60 == t11,
    _find_1st_non_deleted_t61 == t12,
    If(And(DELETED(_find_1st_non_deleted_t59),
           Not(DELETED(_find_1st_non_deleted_t60))),
       _find_1st_non_deleted_t62 ==
       _find_1st_non_deleted_t60,
       _find_1st_non_deleted_t62 ==
       _find_1st_non_deleted_t59),
    If(And(DELETED(_find_1st_non_deleted_t62),
           Not(DELETED(_find_1st_non_deleted_t61))),
       _find_1st_non_deleted_t63 ==
       _find_1st_non_deleted_t61,
       _find_1st_non_deleted_t63 ==
       _find_1st_non_deleted_t62)),
And(_find_1st_non_deleted_t64 == t10,
    _find_1st_non_deleted_t65 == t11,
    _find_1st_non_deleted_t66 == t12,
    If(And(DELETED(_find_1st_non_deleted_t64),
           Not(DELETED(_find_1st_non_deleted_t65))),
       _find_1st_non_deleted_t67 ==
       _find_1st_non_deleted_t65,
       _find_1st_non_deleted_t67 ==
       _find_1st_non_deleted_t64),
    If(And(DELETED(_find_1st_non_deleted_t67),
           Not(DELETED(_find_1st_non_deleted_t66))),
       _find_1st_non_deleted_t68 ==
       _find_1st_non_deleted_t66,
       _find_1st_non_deleted_t68 ==
       _find_1st_non_deleted_t67)),
And(_find_1st_non_deleted_t69 == t11,
    _find_1st_non_deleted_t70 == t12,
    If(And(DELETED(_find_1st_non_deleted_t69),
           Not(DELETED(_find_1st_non_deleted_t70))),
       _find_1st_non_deleted_t71 ==
       _find_1st_non_deleted_t70,
       _find_1st_non_deleted_t71 ==
       _find_1st_non_deleted_t69)),
And(_find_1st_non_deleted_t72 == t11,
    _find_1st_non_deleted_t73 == t12,
    If(And(DELETED(_find_1st_non_deleted_t72),
           Not(DELETED(_find_1st_non_deleted_t73))),
       _find_1st_non_deleted_t74 ==
       _find_1st_non_deleted_t73,
       _find_1st_non_deleted_t74 ==
       _find_1st_non_deleted_t72)),
And(_find_1st_non_deleted_t75 == t11,
    _find_1st_non_deleted_t76 == t12,
    If(And(DELETED(_find_1st_non_deleted_t75),
           Not(DELETED(_find_1st_non_deleted_t76))),
       _find_1st_non_deleted_t77 ==
       _find_1st_non_deleted_t76,
       _find_1st_non_deleted_t77 ==
       _find_1st_non_deleted_t75))
    )
    ,

# t17 := Projection(['t13'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(*[
    Implies(
        Not(DELETED(t13)),
        And(
Not(DELETED(t17)),
And(NULL(t17, ORDERS__CUSTOMER_ID__String) ==
    NULL(t13, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t17) == ORDERS__CUSTOMER_ID(t13)),
And(NULL(t17, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t13, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t17) ==
    CUSTOMERS__CUSTOMER_NAME(t13)),
And(NULL(t17, TABLE6__AB__String) ==
    NULL(t13, TABLE6__AB__String),
    TABLE6__AB(t17) == TABLE6__AB(t13)),
And(NULL(t17, TABLE6__C__String) ==
    NULL(t13, TABLE6__C__String),
    TABLE6__C(t17) == TABLE6__C(t13)),
        ),
    ),
    Implies(DELETED(t13), DELETED(t17)),
]),

# t18 := Projection(['t14'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(*[
    Implies(
        Not(DELETED(t14)),
        And(
Not(DELETED(t18)),
And(NULL(t18, ORDERS__CUSTOMER_ID__String) ==
    NULL(t14, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t18) == ORDERS__CUSTOMER_ID(t14)),
And(NULL(t18, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t14, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t18) ==
    CUSTOMERS__CUSTOMER_NAME(t14)),
And(NULL(t18, TABLE6__AB__String) ==
    NULL(t14, TABLE6__AB__String),
    TABLE6__AB(t18) == TABLE6__AB(t14)),
And(NULL(t18, TABLE6__C__String) ==
    NULL(t14, TABLE6__C__String),
    TABLE6__C(t18) == TABLE6__C(t14)),
        ),
    ),
    Implies(DELETED(t14), DELETED(t18)),
]),

# t19 := Projection(['t15'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(*[
    Implies(
        Not(DELETED(t15)),
        And(
Not(DELETED(t19)),
And(NULL(t19, ORDERS__CUSTOMER_ID__String) ==
    NULL(t15, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t19) == ORDERS__CUSTOMER_ID(t15)),
And(NULL(t19, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t15, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t19) ==
    CUSTOMERS__CUSTOMER_NAME(t15)),
And(NULL(t19, TABLE6__AB__String) ==
    NULL(t15, TABLE6__AB__String),
    TABLE6__AB(t19) == TABLE6__AB(t15)),
And(NULL(t19, TABLE6__C__String) ==
    NULL(t15, TABLE6__C__String),
    TABLE6__C(t19) == TABLE6__C(t15)),
        ),
    ),
    Implies(DELETED(t15), DELETED(t19)),
]),

# t20 := Projection(['t16'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(*[
    Implies(
        Not(DELETED(t16)),
        And(
Not(DELETED(t20)),
And(NULL(t20, ORDERS__CUSTOMER_ID__String) ==
    NULL(t16, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t20) == ORDERS__CUSTOMER_ID(t16)),
And(NULL(t20, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t16, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t20) ==
    CUSTOMERS__CUSTOMER_NAME(t16)),
And(NULL(t20, TABLE6__AB__String) ==
    NULL(t16, TABLE6__AB__String),
    TABLE6__AB(t20) == TABLE6__AB(t16)),
And(NULL(t20, TABLE6__C__String) ==
    NULL(t16, TABLE6__C__String),
    TABLE6__C(t20) == TABLE6__C(t16)),
        ),
    ),
    Implies(DELETED(t16), DELETED(t20)),
]),

# t21 := DistinctProjection(['t17'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(
    Implies(
        And(
Not(DELETED(t17))
),
        And(
            Not(DELETED(t21)),
            And(NULL(t21, ORDERS__CUSTOMER_ID__String) ==
    NULL(t17, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t21) == ORDERS__CUSTOMER_ID(t17)),
And(NULL(t21, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t17, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t21) ==
    CUSTOMERS__CUSTOMER_NAME(t17)),
And(NULL(t21, TABLE6__AB__String) ==
    NULL(t17, TABLE6__AB__String),
    TABLE6__AB(t21) == TABLE6__AB(t17)),
And(NULL(t21, TABLE6__C__String) ==
    NULL(t17, TABLE6__C__String),
    TABLE6__C(t21) == TABLE6__C(t17)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t17))
)), DELETED(t21)),
),

# t22 := DistinctProjection(['t18'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(
    Implies(
        And(
Not(DELETED(t18)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t18,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t18) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t18) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t18, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t18, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t18) == TABLE6__AB(t17))),
                Or(And(NULL(t18, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t18, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t18) == TABLE6__C(t17))))))
),
        And(
            Not(DELETED(t22)),
            And(NULL(t22, ORDERS__CUSTOMER_ID__String) ==
    NULL(t18, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t22) == ORDERS__CUSTOMER_ID(t18)),
And(NULL(t22, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t18, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t22) ==
    CUSTOMERS__CUSTOMER_NAME(t18)),
And(NULL(t22, TABLE6__AB__String) ==
    NULL(t18, TABLE6__AB__String),
    TABLE6__AB(t22) == TABLE6__AB(t18)),
And(NULL(t22, TABLE6__C__String) ==
    NULL(t18, TABLE6__C__String),
    TABLE6__C(t22) == TABLE6__C(t18)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t18)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t18,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t18) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t18) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t18, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t18, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t18) == TABLE6__AB(t17))),
                Or(And(NULL(t18, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t18, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t18) == TABLE6__C(t17))))))
)), DELETED(t22)),
),

# t23 := DistinctProjection(['t19'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(
    Implies(
        And(
Not(DELETED(t19)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t19,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t19) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t19) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t19, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t19, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t19) == TABLE6__AB(t17))),
                Or(And(NULL(t19, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t19, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t19) == TABLE6__C(t17)))))),
Implies(Not(DELETED(t18)),
        Not(And(Or(And(NULL(t19,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t18,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t19) ==
                       ORDERS__CUSTOMER_ID(t18))),
                Or(And(NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t19) ==
                       CUSTOMERS__CUSTOMER_NAME(t18))),
                Or(And(NULL(t19, TABLE6__AB__String),
                       NULL(t18, TABLE6__AB__String)),
                   And(Not(NULL(t19, TABLE6__AB__String)),
                       Not(NULL(t18, TABLE6__AB__String)),
                       TABLE6__AB(t19) == TABLE6__AB(t18))),
                Or(And(NULL(t19, TABLE6__C__String),
                       NULL(t18, TABLE6__C__String)),
                   And(Not(NULL(t19, TABLE6__C__String)),
                       Not(NULL(t18, TABLE6__C__String)),
                       TABLE6__C(t19) == TABLE6__C(t18))))))
),
        And(
            Not(DELETED(t23)),
            And(NULL(t23, ORDERS__CUSTOMER_ID__String) ==
    NULL(t19, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t23) == ORDERS__CUSTOMER_ID(t19)),
And(NULL(t23, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t19, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t23) ==
    CUSTOMERS__CUSTOMER_NAME(t19)),
And(NULL(t23, TABLE6__AB__String) ==
    NULL(t19, TABLE6__AB__String),
    TABLE6__AB(t23) == TABLE6__AB(t19)),
And(NULL(t23, TABLE6__C__String) ==
    NULL(t19, TABLE6__C__String),
    TABLE6__C(t23) == TABLE6__C(t19)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t19)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t19,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t19) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t19) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t19, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t19, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t19) == TABLE6__AB(t17))),
                Or(And(NULL(t19, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t19, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t19) == TABLE6__C(t17)))))),
Implies(Not(DELETED(t18)),
        Not(And(Or(And(NULL(t19,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t18,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t19) ==
                       ORDERS__CUSTOMER_ID(t18))),
                Or(And(NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t19) ==
                       CUSTOMERS__CUSTOMER_NAME(t18))),
                Or(And(NULL(t19, TABLE6__AB__String),
                       NULL(t18, TABLE6__AB__String)),
                   And(Not(NULL(t19, TABLE6__AB__String)),
                       Not(NULL(t18, TABLE6__AB__String)),
                       TABLE6__AB(t19) == TABLE6__AB(t18))),
                Or(And(NULL(t19, TABLE6__C__String),
                       NULL(t18, TABLE6__C__String)),
                   And(Not(NULL(t19, TABLE6__C__String)),
                       Not(NULL(t18, TABLE6__C__String)),
                       TABLE6__C(t19) == TABLE6__C(t18))))))
)), DELETED(t23)),
),

# t24 := DistinctProjection(['t20'], Cond=[A__CUSTOMER_ID, B__CUSTOMER_NAME, TABLE6__AB, TABLE6__C])
And(
    Implies(
        And(
Not(DELETED(t20)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t17))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t17)))))),
Implies(Not(DELETED(t18)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t18,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t18))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t18))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t18, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t18, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t18))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t18, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t18, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t18)))))),
Implies(Not(DELETED(t19)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t19,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t19))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t19))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t19, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t19, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t19))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t19, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t19, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t19))))))
),
        And(
            Not(DELETED(t24)),
            And(NULL(t24, ORDERS__CUSTOMER_ID__String) ==
    NULL(t20, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t24) == ORDERS__CUSTOMER_ID(t20)),
And(NULL(t24, CUSTOMERS__CUSTOMER_NAME__String) ==
    NULL(t20, CUSTOMERS__CUSTOMER_NAME__String),
    CUSTOMERS__CUSTOMER_NAME(t24) ==
    CUSTOMERS__CUSTOMER_NAME(t20)),
And(NULL(t24, TABLE6__AB__String) ==
    NULL(t20, TABLE6__AB__String),
    TABLE6__AB(t24) == TABLE6__AB(t20)),
And(NULL(t24, TABLE6__C__String) ==
    NULL(t20, TABLE6__C__String),
    TABLE6__C(t24) == TABLE6__C(t20)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t20)),
Implies(Not(DELETED(t17)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t17,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t17,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t17))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t17,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t17,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t17))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t17, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t17, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t17))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t17, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t17, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t17)))))),
Implies(Not(DELETED(t18)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t18,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t18,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t18))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t18,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t18,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t18))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t18, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t18, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t18))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t18, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t18, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t18)))))),
Implies(Not(DELETED(t19)),
        Not(And(Or(And(NULL(t20,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t19,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t20,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t19,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t20) ==
                       ORDERS__CUSTOMER_ID(t19))),
                Or(And(NULL(t20,
                            CUSTOMERS__CUSTOMER_NAME__String),
                       NULL(t19,
                            CUSTOMERS__CUSTOMER_NAME__String)),
                   And(Not(NULL(t20,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       Not(NULL(t19,
                                CUSTOMERS__CUSTOMER_NAME__String)),
                       CUSTOMERS__CUSTOMER_NAME(t20) ==
                       CUSTOMERS__CUSTOMER_NAME(t19))),
                Or(And(NULL(t20, TABLE6__AB__String),
                       NULL(t19, TABLE6__AB__String)),
                   And(Not(NULL(t20, TABLE6__AB__String)),
                       Not(NULL(t19, TABLE6__AB__String)),
                       TABLE6__AB(t20) == TABLE6__AB(t19))),
                Or(And(NULL(t20, TABLE6__C__String),
                       NULL(t19, TABLE6__C__String)),
                   And(Not(NULL(t20, TABLE6__C__String)),
                       Not(NULL(t19, TABLE6__C__String)),
                       TABLE6__C(t20) == TABLE6__C(t19))))))
)), DELETED(t24)),
),

# t25 := Filter(['t21'], Cond=(and_gte_TEMP__AB_Digits_2_eq_TEMP__C_Digits_0))
And(
    Implies(
        And(*[Not(DELETED(t21)), If(If(And(Or(Or(NULL(t21, TABLE6__AB__String), False),
             Or(NULL(t21, TABLE6__C__String), False)),
          Or(If(Or(NULL(t21, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t21))),
             If(Or(NULL(t21, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t21, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t21)))))),
      False,
      Or(Or(NULL(t21, TABLE6__AB__String), False),
         Or(NULL(t21, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t21, TABLE6__AB__String), False),
             Or(NULL(t21, TABLE6__C__String), False)),
          Or(If(Or(NULL(t21, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t21))),
             If(Or(NULL(t21, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t21, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t21)))))),
      False,
      And(2 <= TABLE6__AB(t21),
          And(Not(NULL(t21, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t21)))))]),
        And(Not(DELETED(t25)), t25 == t21),
    ),
    Implies(Not(And(*[Not(DELETED(t21)), If(If(And(Or(Or(NULL(t21, TABLE6__AB__String), False),
             Or(NULL(t21, TABLE6__C__String), False)),
          Or(If(Or(NULL(t21, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t21))),
             If(Or(NULL(t21, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t21, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t21)))))),
      False,
      Or(Or(NULL(t21, TABLE6__AB__String), False),
         Or(NULL(t21, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t21, TABLE6__AB__String), False),
             Or(NULL(t21, TABLE6__C__String), False)),
          Or(If(Or(NULL(t21, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t21))),
             If(Or(NULL(t21, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t21, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t21)))))),
      False,
      And(2 <= TABLE6__AB(t21),
          And(Not(NULL(t21, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t21)))))])), DELETED(t25)),
),

# t26 := Filter(['t22'], Cond=(and_gte_TEMP__AB_Digits_2_eq_TEMP__C_Digits_0))
And(
    Implies(
        And(*[Not(DELETED(t22)), If(If(And(Or(Or(NULL(t22, TABLE6__AB__String), False),
             Or(NULL(t22, TABLE6__C__String), False)),
          Or(If(Or(NULL(t22, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t22))),
             If(Or(NULL(t22, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t22, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t22)))))),
      False,
      Or(Or(NULL(t22, TABLE6__AB__String), False),
         Or(NULL(t22, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t22, TABLE6__AB__String), False),
             Or(NULL(t22, TABLE6__C__String), False)),
          Or(If(Or(NULL(t22, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t22))),
             If(Or(NULL(t22, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t22, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t22)))))),
      False,
      And(2 <= TABLE6__AB(t22),
          And(Not(NULL(t22, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t22)))))]),
        And(Not(DELETED(t26)), t26 == t22),
    ),
    Implies(Not(And(*[Not(DELETED(t22)), If(If(And(Or(Or(NULL(t22, TABLE6__AB__String), False),
             Or(NULL(t22, TABLE6__C__String), False)),
          Or(If(Or(NULL(t22, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t22))),
             If(Or(NULL(t22, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t22, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t22)))))),
      False,
      Or(Or(NULL(t22, TABLE6__AB__String), False),
         Or(NULL(t22, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t22, TABLE6__AB__String), False),
             Or(NULL(t22, TABLE6__C__String), False)),
          Or(If(Or(NULL(t22, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t22))),
             If(Or(NULL(t22, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t22, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t22)))))),
      False,
      And(2 <= TABLE6__AB(t22),
          And(Not(NULL(t22, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t22)))))])), DELETED(t26)),
),

# t27 := Filter(['t23'], Cond=(and_gte_TEMP__AB_Digits_2_eq_TEMP__C_Digits_0))
And(
    Implies(
        And(*[Not(DELETED(t23)), If(If(And(Or(Or(NULL(t23, TABLE6__AB__String), False),
             Or(NULL(t23, TABLE6__C__String), False)),
          Or(If(Or(NULL(t23, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t23))),
             If(Or(NULL(t23, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t23, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t23)))))),
      False,
      Or(Or(NULL(t23, TABLE6__AB__String), False),
         Or(NULL(t23, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t23, TABLE6__AB__String), False),
             Or(NULL(t23, TABLE6__C__String), False)),
          Or(If(Or(NULL(t23, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t23))),
             If(Or(NULL(t23, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t23, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t23)))))),
      False,
      And(2 <= TABLE6__AB(t23),
          And(Not(NULL(t23, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t23)))))]),
        And(Not(DELETED(t27)), t27 == t23),
    ),
    Implies(Not(And(*[Not(DELETED(t23)), If(If(And(Or(Or(NULL(t23, TABLE6__AB__String), False),
             Or(NULL(t23, TABLE6__C__String), False)),
          Or(If(Or(NULL(t23, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t23))),
             If(Or(NULL(t23, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t23, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t23)))))),
      False,
      Or(Or(NULL(t23, TABLE6__AB__String), False),
         Or(NULL(t23, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t23, TABLE6__AB__String), False),
             Or(NULL(t23, TABLE6__C__String), False)),
          Or(If(Or(NULL(t23, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t23))),
             If(Or(NULL(t23, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t23, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t23)))))),
      False,
      And(2 <= TABLE6__AB(t23),
          And(Not(NULL(t23, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t23)))))])), DELETED(t27)),
),

# t28 := Filter(['t24'], Cond=(and_gte_TEMP__AB_Digits_2_eq_TEMP__C_Digits_0))
And(
    Implies(
        And(*[Not(DELETED(t24)), If(If(And(Or(Or(NULL(t24, TABLE6__AB__String), False),
             Or(NULL(t24, TABLE6__C__String), False)),
          Or(If(Or(NULL(t24, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t24))),
             If(Or(NULL(t24, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t24, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t24)))))),
      False,
      Or(Or(NULL(t24, TABLE6__AB__String), False),
         Or(NULL(t24, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t24, TABLE6__AB__String), False),
             Or(NULL(t24, TABLE6__C__String), False)),
          Or(If(Or(NULL(t24, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t24))),
             If(Or(NULL(t24, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t24, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t24)))))),
      False,
      And(2 <= TABLE6__AB(t24),
          And(Not(NULL(t24, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t24)))))]),
        And(Not(DELETED(t28)), t28 == t24),
    ),
    Implies(Not(And(*[Not(DELETED(t24)), If(If(And(Or(Or(NULL(t24, TABLE6__AB__String), False),
             Or(NULL(t24, TABLE6__C__String), False)),
          Or(If(Or(NULL(t24, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t24))),
             If(Or(NULL(t24, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t24, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t24)))))),
      False,
      Or(Or(NULL(t24, TABLE6__AB__String), False),
         Or(NULL(t24, TABLE6__C__String), False))),
   False,
   If(And(Or(Or(NULL(t24, TABLE6__AB__String), False),
             Or(NULL(t24, TABLE6__C__String), False)),
          Or(If(Or(NULL(t24, TABLE6__AB__String), False),
                False,
                Not(2 <= TABLE6__AB(t24))),
             If(Or(NULL(t24, TABLE6__C__String), False),
                False,
                Not(And(Not(NULL(t24, TABLE6__C__String)),
                        Not(False),
                        0 == TABLE6__C(t24)))))),
      False,
      And(2 <= TABLE6__AB(t24),
          And(Not(NULL(t24, TABLE6__C__String)),
              Not(False),
              0 == TABLE6__C(t24)))))])), DELETED(t28)),
)
)

premise2 = And(
# 2nd SQL query formulas
# t78 := Filter(['t3'], Cond=(eq_ORDERS__PRODUCT_NAME_String_A__Int))
And(
    Implies(
        And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_A__Int))]),
        And(Not(DELETED(t78)), t78 == t3),
    ),
    Implies(Not(And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_A__Int))])), DELETED(t78)),
),

# t79 := Filter(['t4'], Cond=(eq_ORDERS__PRODUCT_NAME_String_A__Int))
And(
    Implies(
        And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_A__Int))]),
        And(Not(DELETED(t79)), t79 == t4),
    ),
    Implies(Not(And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_A__Int))])), DELETED(t79)),
),

# t82 := DistinctProjection(['t80'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t78))
),
        And(
            Not(DELETED(t82)),
            And(NULL(t82, ORDERS__CUSTOMER_ID__String) ==
    NULL(t78, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t82) == ORDERS__CUSTOMER_ID(t78)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t78))
)), DELETED(t82)),
),

# t83 := DistinctProjection(['t81'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t79)),
Implies(Not(DELETED(t78)),
        Not(And(Or(And(NULL(t79,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t78,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t79,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t78,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t79) ==
                       ORDERS__CUSTOMER_ID(t78))))))
),
        And(
            Not(DELETED(t83)),
            And(NULL(t83, ORDERS__CUSTOMER_ID__String) ==
    NULL(t79, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t83) == ORDERS__CUSTOMER_ID(t79)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t79)),
Implies(Not(DELETED(t78)),
        Not(And(Or(And(NULL(t79,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t78,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t79,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t78,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t79) ==
                       ORDERS__CUSTOMER_ID(t78))))))
)), DELETED(t83)),
),

# t84 := Filter(['t3'], Cond=(eq_ORDERS__PRODUCT_NAME_String_B__Int))
And(
    Implies(
        And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_B__Int))]),
        And(Not(DELETED(t84)), t84 == t3),
    ),
    Implies(Not(And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_B__Int))])), DELETED(t84)),
),

# t85 := Filter(['t4'], Cond=(eq_ORDERS__PRODUCT_NAME_String_B__Int))
And(
    Implies(
        And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_B__Int))]),
        And(Not(DELETED(t85)), t85 == t4),
    ),
    Implies(Not(And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_B__Int))])), DELETED(t85)),
),

# t88 := DistinctProjection(['t86'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t84))
),
        And(
            Not(DELETED(t88)),
            And(NULL(t88, ORDERS__CUSTOMER_ID__String) ==
    NULL(t84, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t88) == ORDERS__CUSTOMER_ID(t84)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t84))
)), DELETED(t88)),
),

# t89 := DistinctProjection(['t87'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t85)),
Implies(Not(DELETED(t84)),
        Not(And(Or(And(NULL(t85,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t84,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t85,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t84,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t85) ==
                       ORDERS__CUSTOMER_ID(t84))))))
),
        And(
            Not(DELETED(t89)),
            And(NULL(t89, ORDERS__CUSTOMER_ID__String) ==
    NULL(t85, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t89) == ORDERS__CUSTOMER_ID(t85)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t85)),
Implies(Not(DELETED(t84)),
        Not(And(Or(And(NULL(t85,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t84,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t85,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t84,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t85) ==
                       ORDERS__CUSTOMER_ID(t84))))))
)), DELETED(t89)),
),

# t90 := Filter(['t3'], Cond=(eq_ORDERS__PRODUCT_NAME_String_C__Int))
And(
    Implies(
        And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_C__Int))]),
        And(Not(DELETED(t90)), t90 == t3),
    ),
    Implies(Not(And(*[Not(DELETED(t3)), If(Or(NULL(t3, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t3, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t3) == String_C__Int))])), DELETED(t90)),
),

# t91 := Filter(['t4'], Cond=(eq_ORDERS__PRODUCT_NAME_String_C__Int))
And(
    Implies(
        And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_C__Int))]),
        And(Not(DELETED(t91)), t91 == t4),
    ),
    Implies(Not(And(*[Not(DELETED(t4)), If(Or(NULL(t4, ORDERS__PRODUCT_NAME__String), False),
   False,
   And(Not(NULL(t4, ORDERS__PRODUCT_NAME__String)),
       Not(False),
       ORDERS__PRODUCT_NAME(t4) == String_C__Int))])), DELETED(t91)),
),

# t94 := DistinctProjection(['t92'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t90))
),
        And(
            Not(DELETED(t94)),
            And(NULL(t94, ORDERS__CUSTOMER_ID__String) ==
    NULL(t90, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t94) == ORDERS__CUSTOMER_ID(t90)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t90))
)), DELETED(t94)),
),

# t95 := DistinctProjection(['t93'], Cond=[ORDERS__CUSTOMER_ID])
And(
    Implies(
        And(
Not(DELETED(t91)),
Implies(Not(DELETED(t90)),
        Not(And(Or(And(NULL(t91,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t90,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t91,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t90,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t91) ==
                       ORDERS__CUSTOMER_ID(t90))))))
),
        And(
            Not(DELETED(t95)),
            And(NULL(t95, ORDERS__CUSTOMER_ID__String) ==
    NULL(t91, ORDERS__CUSTOMER_ID__String),
    ORDERS__CUSTOMER_ID(t95) == ORDERS__CUSTOMER_ID(t91)),
        ),
    ),
    Implies(Not(And(
Not(DELETED(t91)),
Implies(Not(DELETED(t90)),
        Not(And(Or(And(NULL(t91,
                            ORDERS__CUSTOMER_ID__String),
                       NULL(t90,
                            ORDERS__CUSTOMER_ID__String)),
                   And(Not(NULL(t91,
                                ORDERS__CUSTOMER_ID__String)),
                       Not(NULL(t90,
                                ORDERS__CUSTOMER_ID__String)),
                       ORDERS__CUSTOMER_ID(t91) ==
                       ORDERS__CUSTOMER_ID(t90))))))
)), DELETED(t95)),
),

# t96 := Filter(['t1'], Cond=(and_[CUSTOMERS__CUSTOMER_ID]_in_False_[CUSTOMERS__CUSTOMER_ID]_in_False_[CUSTOMERS__CUSTOMER_ID]_nin_False))
And(
    Implies(
        And(*[Not(DELETED(t1)), If(If(And(Or(And(Not(And(DELETED(t82), DELETED(t83))),
                 Or(Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                        Or(And(Not(DELETED(t82)),
                               NULL(t82,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t83)),
                               NULL(t83,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t88), DELETED(t89))),
                 Or(Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                        Or(And(Not(DELETED(t88)),
                               NULL(t88,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t89)),
                               NULL(t89,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t94), DELETED(t95))),
                 If(Or(And(And(Not(DELETED(t94)),
                               Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t1) ==
                                      ORDERS__CUSTOMER_ID(t94))))),
                       And(And(Not(DELETED(t95)),
                               Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t1) ==
                                      ORDERS__CUSTOMER_ID(t95)))))),
                    Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    Or(And(NULL(t1,
                                CUSTOMERS__CUSTOMER_ID__String)),
                       And(And(Not(DELETED(t94)),
                               NULL(t94,
                                    ORDERS__CUSTOMER_ID__String))),
                       And(And(Not(DELETED(t95)),
                               NULL(t95,
                                    ORDERS__CUSTOMER_ID__String))))))),
          Or(If(And(Not(And(DELETED(t82), DELETED(t83))),
                    Or(Or(NULL(t1,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t82)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                                  And(And(Not(DELETED(t83)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                           Or(And(Not(DELETED(t82)),
                                  NULL(t82,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t83)),
                                  NULL(t83,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t82), DELETED(t83))),
                        And(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83)))))),
                            Not(Or(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String))))))),
             If(And(Not(And(DELETED(t88), DELETED(t89))),
                    Or(Or(NULL(t1,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t88)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                                  And(And(Not(DELETED(t89)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                           Or(And(Not(DELETED(t88)),
                                  NULL(t88,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t89)),
                                  NULL(t89,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t88), DELETED(t89))),
                        And(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
...]),
        And(Not(DELETED(t96)), t96 == t1),
    ),
    Implies(Not(And(*[Not(DELETED(t1)), If(If(And(Or(And(Not(And(DELETED(t82), DELETED(t83))),
                 Or(Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                        Or(And(Not(DELETED(t82)),
                               NULL(t82,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t83)),
                               NULL(t83,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t88), DELETED(t89))),
                 Or(Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                        Or(And(Not(DELETED(t88)),
                               NULL(t88,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t89)),
                               NULL(t89,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t94), DELETED(t95))),
                 If(Or(And(And(Not(DELETED(t94)),
                               Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t1) ==
                                      ORDERS__CUSTOMER_ID(t94))))),
                       And(And(Not(DELETED(t95)),
                               Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t1) ==
                                      ORDERS__CUSTOMER_ID(t95)))))),
                    Or(NULL(t1,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    Or(And(NULL(t1,
                                CUSTOMERS__CUSTOMER_ID__String)),
                       And(And(Not(DELETED(t94)),
                               NULL(t94,
                                    ORDERS__CUSTOMER_ID__String))),
                       And(And(Not(DELETED(t95)),
                               NULL(t95,
                                    ORDERS__CUSTOMER_ID__String))))))),
          Or(If(And(Not(And(DELETED(t82), DELETED(t83))),
                    Or(Or(NULL(t1,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t82)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                                  And(And(Not(DELETED(t83)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                           Or(And(Not(DELETED(t82)),
                                  NULL(t82,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t83)),
                                  NULL(t83,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t82), DELETED(t83))),
                        And(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t83)))))),
                            Not(Or(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String))))))),
             If(And(Not(And(DELETED(t88), DELETED(t89))),
                    Or(Or(NULL(t1,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t88)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                                  And(And(Not(DELETED(t89)),
                                        Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                           Or(And(Not(DELETED(t88)),
                                  NULL(t88,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t89)),
                                  NULL(t89,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t88), DELETED(t89))),
                        And(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t1) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t1,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
...])), DELETED(t96)),
),

# t97 := Filter(['t2'], Cond=(and_[CUSTOMERS__CUSTOMER_ID]_in_False_[CUSTOMERS__CUSTOMER_ID]_in_False_[CUSTOMERS__CUSTOMER_ID]_nin_False))
And(
    Implies(
        And(*[Not(DELETED(t2)), If(If(And(Or(And(Not(And(DELETED(t82), DELETED(t83))),
                 Or(Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                        Or(And(Not(DELETED(t82)),
                               NULL(t82,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t83)),
                               NULL(t83,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t88), DELETED(t89))),
                 Or(Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                        Or(And(Not(DELETED(t88)),
                               NULL(t88,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t89)),
                               NULL(t89,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t94), DELETED(t95))),
                 If(Or(And(And(Not(DELETED(t94)),
                               Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t2) ==
                                      ORDERS__CUSTOMER_ID(t94))))),
                       And(And(Not(DELETED(t95)),
                               Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t2) ==
                                      ORDERS__CUSTOMER_ID(t95)))))),
                    Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    Or(And(NULL(t2,
                                CUSTOMERS__CUSTOMER_ID__String)),
                       And(And(Not(DELETED(t94)),
                               NULL(t94,
                                    ORDERS__CUSTOMER_ID__String))),
                       And(And(Not(DELETED(t95)),
                               NULL(t95,
                                    ORDERS__CUSTOMER_ID__String))))))),
          Or(If(And(Not(And(DELETED(t82), DELETED(t83))),
                    Or(Or(NULL(t2,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t82)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                                  And(And(Not(DELETED(t83)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                           Or(And(Not(DELETED(t82)),
                                  NULL(t82,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t83)),
                                  NULL(t83,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t82), DELETED(t83))),
                        And(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83)))))),
                            Not(Or(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String))))))),
             If(And(Not(And(DELETED(t88), DELETED(t89))),
                    Or(Or(NULL(t2,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t88)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                                  And(And(Not(DELETED(t89)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                           Or(And(Not(DELETED(t88)),
                                  NULL(t88,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t89)),
                                  NULL(t89,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t88), DELETED(t89))),
                        And(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
...]),
        And(Not(DELETED(t97)), t97 == t2),
    ),
    Implies(Not(And(*[Not(DELETED(t2)), If(If(And(Or(And(Not(And(DELETED(t82), DELETED(t83))),
                 Or(Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                        Or(And(Not(DELETED(t82)),
                               NULL(t82,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t83)),
                               NULL(t83,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t88), DELETED(t89))),
                 Or(Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    And(Not(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                        Or(And(Not(DELETED(t88)),
                               NULL(t88,
                                    ORDERS__CUSTOMER_ID__String)),
                           And(Not(DELETED(t89)),
                               NULL(t89,
                                    ORDERS__CUSTOMER_ID__String)))))),
             And(Not(And(DELETED(t94), DELETED(t95))),
                 If(Or(And(And(Not(DELETED(t94)),
                               Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t94,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t2) ==
                                      ORDERS__CUSTOMER_ID(t94))))),
                       And(And(Not(DELETED(t95)),
                               Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                      NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                  And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                      Not(NULL(t95,
                                        ORDERS__CUSTOMER_ID__String)),
                                      CUSTOMERS__CUSTOMER_ID(t2) ==
                                      ORDERS__CUSTOMER_ID(t95)))))),
                    Or(NULL(t2,
                            CUSTOMERS__CUSTOMER_ID__String)),
                    Or(And(NULL(t2,
                                CUSTOMERS__CUSTOMER_ID__String)),
                       And(And(Not(DELETED(t94)),
                               NULL(t94,
                                    ORDERS__CUSTOMER_ID__String))),
                       And(And(Not(DELETED(t95)),
                               NULL(t95,
                                    ORDERS__CUSTOMER_ID__String))))))),
          Or(If(And(Not(And(DELETED(t82), DELETED(t83))),
                    Or(Or(NULL(t2,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t82)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                                  And(And(Not(DELETED(t83)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83))))))),
                           Or(And(Not(DELETED(t82)),
                                  NULL(t82,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t83)),
                                  NULL(t83,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t82), DELETED(t83))),
                        And(Or(And(And(Not(DELETED(t82)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t82,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t82))))),
                               And(And(Not(DELETED(t83)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t83,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t83)))))),
                            Not(Or(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String))))))),
             If(And(Not(And(DELETED(t88), DELETED(t89))),
                    Or(Or(NULL(t2,
                               CUSTOMERS__CUSTOMER_ID__String)),
                       And(Not(Or(And(And(Not(DELETED(t88)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                                  And(And(Not(DELETED(t89)),
                                        Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t89,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t89))))))),
                           Or(And(Not(DELETED(t88)),
                                  NULL(t88,
                                       ORDERS__CUSTOMER_ID__String)),
                              And(Not(DELETED(t89)),
                                  NULL(t89,
                                       ORDERS__CUSTOMER_ID__String)))))),
                False,
                Not(And(Not(And(DELETED(t88), DELETED(t89))),
                        And(Or(And(And(Not(DELETED(t88)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        And(Not(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String)),
                                        Not(NULL(t88,
                                        ORDERS__CUSTOMER_ID__String)),
                                        CUSTOMERS__CUSTOMER_ID(t2) ==
                                        ORDERS__CUSTOMER_ID(t88))))),
                               And(And(Not(DELETED(t89)),
                                       Or(And(NULL(t2,
                                        CUSTOMERS__CUSTOMER_ID__String),
                                        NULL(t89,
...])), DELETED(t97)),
),

# Table21 OrderBy constraint
And(
_orderby_t102 == t96,
_orderby_t103 == t97,
If(And(DELETED(_orderby_t102), Not(DELETED(_orderby_t103))),
   And(_orderby_t104 == _orderby_t103,
       _orderby_t105 == _orderby_t102),
   And(_orderby_t104 == _orderby_t102,
       _orderby_t105 == _orderby_t103)),
If(Or(And(Not(DELETED(_orderby_t104)),
          Not(DELETED(_orderby_t105)),
          Or(And(Not(NULL(_orderby_t104,
                          CUSTOMERS__CUSTOMER_ID__String)),
                 NULL(_orderby_t105,
                      CUSTOMERS__CUSTOMER_ID__String)),
             And(Not(NULL(_orderby_t104,
                          CUSTOMERS__CUSTOMER_ID__String)),
                 Not(NULL(_orderby_t105,
                          CUSTOMERS__CUSTOMER_ID__String)),
                 CUSTOMERS__CUSTOMER_ID(_orderby_t104) >
                 CUSTOMERS__CUSTOMER_ID(_orderby_t105))))),
   And(_orderby_t106 == _orderby_t105,
       _orderby_t107 == _orderby_t104),
   And(_orderby_t106 == _orderby_t104,
       _orderby_t107 == _orderby_t105))
),

# t98 := OrderBy(['t96'], [(CUSTOMERS__CUSTOMER_ID, 'ASC')])
t98 == _orderby_t106,

# t99 := OrderBy(['t97'], [(CUSTOMERS__CUSTOMER_ID, 'ASC')])
t99 == _orderby_t107
)

premise = And(DBMS_facts, premise1, premise2)

def equals(ltuples, rtuples):
    left_left_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, ORDERS__CUSTOMER_ID__String), NULL(tuple2, ORDERS__CUSTOMER_ID__String)), And(Not(NULL(tuple1, ORDERS__CUSTOMER_ID__String)), Not(NULL(tuple2, ORDERS__CUSTOMER_ID__String)), ORDERS__CUSTOMER_ID(tuple1) == ORDERS__CUSTOMER_ID(tuple2))),
Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String), NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), CUSTOMERS__CUSTOMER_NAME(tuple1) == CUSTOMERS__CUSTOMER_NAME(tuple2))),
    )
)
    left_right_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, ORDERS__CUSTOMER_ID__String), NULL(tuple2, CUSTOMERS__CUSTOMER_ID__String)), And(Not(NULL(tuple1, ORDERS__CUSTOMER_ID__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_ID__String)), ORDERS__CUSTOMER_ID(tuple1) == CUSTOMERS__CUSTOMER_ID(tuple2))),
Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String), NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), CUSTOMERS__CUSTOMER_NAME(tuple1) == CUSTOMERS__CUSTOMER_NAME(tuple2))),
    )
)
    right_left_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_ID__String), NULL(tuple2, ORDERS__CUSTOMER_ID__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_ID__String)), Not(NULL(tuple2, ORDERS__CUSTOMER_ID__String)), CUSTOMERS__CUSTOMER_ID(tuple1) == ORDERS__CUSTOMER_ID(tuple2))),
Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String), NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), CUSTOMERS__CUSTOMER_NAME(tuple1) == CUSTOMERS__CUSTOMER_NAME(tuple2))),
    )
)
    right_right_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_ID__String), NULL(tuple2, CUSTOMERS__CUSTOMER_ID__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_ID__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_ID__String)), CUSTOMERS__CUSTOMER_ID(tuple1) == CUSTOMERS__CUSTOMER_ID(tuple2))),
Or(And(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String), NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), And(Not(NULL(tuple1, CUSTOMERS__CUSTOMER_NAME__String)), Not(NULL(tuple2, CUSTOMERS__CUSTOMER_NAME__String)), CUSTOMERS__CUSTOMER_NAME(tuple1) == CUSTOMERS__CUSTOMER_NAME(tuple2))),
    )
)

    formulas = [
        Sum([If(DELETED(tuple_sort), 0, 1) for tuple_sort in ltuples]) ==         Sum([If(DELETED(tuple_sort), 0, 1) for tuple_sort in rtuples])
    ]
    for tuple_sort in ltuples:
        count_in_ltuples = Sum([If(left_left_function(tuple_sort, t), 1, 0) for t in ltuples])
        count_in_rtuples = Sum([If(left_right_function(tuple_sort, t), 1, 0) for t in rtuples])
        formulas.append(
            Implies(
                Not(DELETED(tuple_sort)),
                count_in_ltuples == count_in_rtuples,
            )
        )
    for tuple_sort in rtuples:
        count_in_ltuples = Sum([If(right_left_function(tuple_sort, t), 1, 0) for t in ltuples])
        count_in_rtuples = Sum([If(right_right_function(tuple_sort, t), 1, 0) for t in rtuples])
        formulas.append(
            Implies(
                Not(DELETED(tuple_sort)),
                count_in_ltuples == count_in_rtuples,
            )
        )

    formulas = And(formulas)
    return formulas

conclusion = equals(ltuples=[t25, t26, t27, t28], rtuples=[t98, t99])

solver = Solver()

solver.add(Not(Implies(premise, conclusion)))
print(f'Symbolic Reasoning Output: ==> {solver.check()} <==')
model = solver.model()
#print(model)
for t in [t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t78, t79, t82, t83, t84, t85, t88, t89, t90, t91, t94, t95, t96, t97, t98, t99]:
	print(str(t), model.eval(DELETED(t)))
def _f(null, value, out_str=False, data_preix=None, type=None):
    if not isinstance(null, bool):
        null = eval(str(model.eval(null, model_completion=True)))
    if null:
        value = 99999
    else:
        if not isinstance(value, int | float):
            value = eval(str(model.eval(value, model_completion=False)))
    
    if value == 99999:
        return 'NULL'
    else:
        if out_str:
            return f"'{value}'"
        else:
            value = value if data_preix is None else f"'{data_preix + str(value)}'"
            if type == 'boolean':
                return value != 0
            else:
                return value

print(
	_f(NULL(t1, CUSTOMERS__CUSTOMER_ID__String), CUSTOMERS__CUSTOMER_ID(t1)),
',',
	_f(NULL(t1, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t1)),
)
print(
	_f(NULL(t2, CUSTOMERS__CUSTOMER_ID__String), CUSTOMERS__CUSTOMER_ID(t2)),
',',
	_f(NULL(t2, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t2)),
)
print(
	_f(NULL(t3, ORDERS__ORDER_ID__String), ORDERS__ORDER_ID(t3)),
',',
	_f(NULL(t3, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t3)),
',',
	_f(NULL(t3, ORDERS__PRODUCT_NAME__String), ORDERS__PRODUCT_NAME(t3)),
)
print(
	_f(NULL(t4, ORDERS__ORDER_ID__String), ORDERS__ORDER_ID(t4)),
',',
	_f(NULL(t4, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t4)),
',',
	_f(NULL(t4, ORDERS__PRODUCT_NAME__String), ORDERS__PRODUCT_NAME(t4)),
)

print('--------sql1--------')
if model.eval(Not(DELETED(t25))):
	print(
	_f(NULL(t25, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t25)),
',',
	_f(NULL(t25, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t25)),
	)
if model.eval(Not(DELETED(t26))):
	print(
	_f(NULL(t26, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t26)),
',',
	_f(NULL(t26, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t26)),
	)
if model.eval(Not(DELETED(t27))):
	print(
	_f(NULL(t27, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t27)),
',',
	_f(NULL(t27, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t27)),
	)
if model.eval(Not(DELETED(t28))):
	print(
	_f(NULL(t28, ORDERS__CUSTOMER_ID__String), ORDERS__CUSTOMER_ID(t28)),
',',
	_f(NULL(t28, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t28)),
	)
print('--------sql2--------')
if model.eval(Not(DELETED(t98))):
	print(
	_f(NULL(t98, CUSTOMERS__CUSTOMER_ID__String), CUSTOMERS__CUSTOMER_ID(t98)),
',',
	_f(NULL(t98, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t98)),
	)
if model.eval(Not(DELETED(t99))):
	print(
	_f(NULL(t99, CUSTOMERS__CUSTOMER_ID__String), CUSTOMERS__CUSTOMER_ID(t99)),
',',
	_f(NULL(t99, CUSTOMERS__CUSTOMER_NAME__String), CUSTOMERS__CUSTOMER_NAME(t99)),
	)

