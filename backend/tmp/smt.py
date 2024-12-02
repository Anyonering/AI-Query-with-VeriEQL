# -*- coding:utf-8 -*-
from z3 import *
import itertools
import functools

sql1 = "SELECT SUM(L_EXTENDEDPRICE * L_DISCOUNT) AS REVENUE FROM LINEITEM WHERE L_SHIPDATE >= DATE '1993-01-01' AND L_DISCOUNT > 0.08 AND L_QUANTITY < 26 LIMIT 1;"
sql2 = "SELECT SUM(L_EXTENDEDPRICE * L_DISCOUNT) AS REVENUE FROM LINEITEM WHERE L_SHIPDATE >= DATE '1993-01-01' AND L_DISCOUNT > 0.08 AND L_QUANTITY >41 LIMIT 1;"

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
LINEITEM__L_ORDERKEY = Function('LINEITEM__L_ORDERKEY', __TupleSort, __Int)  # define `LINEITEM__L_ORDERKEY` function to retrieve columns of tuples
LINEITEM__L_PARTKEY = Function('LINEITEM__L_PARTKEY', __TupleSort, __Int)  # define `LINEITEM__L_PARTKEY` function to retrieve columns of tuples
LINEITEM__L_SUPPKEY = Function('LINEITEM__L_SUPPKEY', __TupleSort, __Int)  # define `LINEITEM__L_SUPPKEY` function to retrieve columns of tuples
LINEITEM__L_LINENUMBER = Function('LINEITEM__L_LINENUMBER', __TupleSort, __Int)  # define `LINEITEM__L_LINENUMBER` function to retrieve columns of tuples
LINEITEM__L_QUANTITY = Function('LINEITEM__L_QUANTITY', __TupleSort, __Int)  # define `LINEITEM__L_QUANTITY` function to retrieve columns of tuples
LINEITEM__L_EXTENDEDPRICE = Function('LINEITEM__L_EXTENDEDPRICE', __TupleSort, __Int)  # define `LINEITEM__L_EXTENDEDPRICE` function to retrieve columns of tuples
LINEITEM__L_DISCOUNT = Function('LINEITEM__L_DISCOUNT', __TupleSort, __Int)  # define `LINEITEM__L_DISCOUNT` function to retrieve columns of tuples
LINEITEM__L_TAX = Function('LINEITEM__L_TAX', __TupleSort, __Int)  # define `LINEITEM__L_TAX` function to retrieve columns of tuples
LINEITEM__L_RETURNFLAG = Function('LINEITEM__L_RETURNFLAG', __TupleSort, __Int)  # define `LINEITEM__L_RETURNFLAG` function to retrieve columns of tuples
LINEITEM__L_LINESTATUS = Function('LINEITEM__L_LINESTATUS', __TupleSort, __Int)  # define `LINEITEM__L_LINESTATUS` function to retrieve columns of tuples
LINEITEM__L_SHIPDATE = Function('LINEITEM__L_SHIPDATE', __TupleSort, __Int)  # define `LINEITEM__L_SHIPDATE` function to retrieve columns of tuples
LINEITEM__L_COMMITDATE = Function('LINEITEM__L_COMMITDATE', __TupleSort, __Int)  # define `LINEITEM__L_COMMITDATE` function to retrieve columns of tuples
LINEITEM__L_RECEIPTDATE = Function('LINEITEM__L_RECEIPTDATE', __TupleSort, __Int)  # define `LINEITEM__L_RECEIPTDATE` function to retrieve columns of tuples
LINEITEM__L_SHIPINSTRUCT = Function('LINEITEM__L_SHIPINSTRUCT', __TupleSort, __Int)  # define `LINEITEM__L_SHIPINSTRUCT` function to retrieve columns of tuples
LINEITEM__L_SHIPMODE = Function('LINEITEM__L_SHIPMODE', __TupleSort, __Int)  # define `LINEITEM__L_SHIPMODE` function to retrieve columns of tuples
LINEITEM__L_COMMENT = Function('LINEITEM__L_COMMENT', __TupleSort, __Int)  # define `LINEITEM__L_COMMENT` function to retrieve columns of tuples
NATION__N_NATIONKEY = Function('NATION__N_NATIONKEY', __TupleSort, __Int)  # define `NATION__N_NATIONKEY` function to retrieve columns of tuples
NATION__N_NAME = Function('NATION__N_NAME', __TupleSort, __Int)  # define `NATION__N_NAME` function to retrieve columns of tuples
NATION__N_REGIONKEY = Function('NATION__N_REGIONKEY', __TupleSort, __Int)  # define `NATION__N_REGIONKEY` function to retrieve columns of tuples
NATION__N_COMMENT = Function('NATION__N_COMMENT', __TupleSort, __Int)  # define `NATION__N_COMMENT` function to retrieve columns of tuples
TABLE3__REVENUE = Function('TABLE3__REVENUE', __TupleSort, __Int)  # define `TABLE3__REVENUE` function to retrieve columns of tuples
TABLE6__REVENUE = Function('TABLE6__REVENUE', __TupleSort, __Int)  # define `TABLE6__REVENUE` function to retrieve columns of tuples

# Special Variables
NULL_VALUE = Const('NULL_VALUE', __Int)  # define NULL variable
POS_INF__Int = Const('POS_INF__Int', __Int)  # define +INF variable
NEG_INF__Int = Const('NEG_INF__Int', __Int)  # define -INF variable
COUNT_ALL__String = Const(f"COUNT_ALL__String", __String)  # define `COUNT(*)`
t1 = Const('t1', __TupleSort)  # define a tuple `t1`
LINEITEM__L_ORDERKEY__String = Const('LINEITEM__L_ORDERKEY__String', __String)  # define `LINEITEM__L_ORDERKEY__String` for NULL function
String_x1__Int = Const('String_x1__Int', __Int)  # define `String_x1__Int` for NULL function
LINEITEM__L_PARTKEY__String = Const('LINEITEM__L_PARTKEY__String', __String)  # define `LINEITEM__L_PARTKEY__String` for NULL function
String_x2__Int = Const('String_x2__Int', __Int)  # define `String_x2__Int` for NULL function
LINEITEM__L_SUPPKEY__String = Const('LINEITEM__L_SUPPKEY__String', __String)  # define `LINEITEM__L_SUPPKEY__String` for NULL function
String_x3__Int = Const('String_x3__Int', __Int)  # define `String_x3__Int` for NULL function
LINEITEM__L_LINENUMBER__String = Const('LINEITEM__L_LINENUMBER__String', __String)  # define `LINEITEM__L_LINENUMBER__String` for NULL function
String_x4__Int = Const('String_x4__Int', __Int)  # define `String_x4__Int` for NULL function
LINEITEM__L_QUANTITY__String = Const('LINEITEM__L_QUANTITY__String', __String)  # define `LINEITEM__L_QUANTITY__String` for NULL function
String_x5__Int = Const('String_x5__Int', __Int)  # define `String_x5__Int` for NULL function
LINEITEM__L_EXTENDEDPRICE__String = Const('LINEITEM__L_EXTENDEDPRICE__String', __String)  # define `LINEITEM__L_EXTENDEDPRICE__String` for NULL function
String_x6__Int = Const('String_x6__Int', __Int)  # define `String_x6__Int` for NULL function
LINEITEM__L_DISCOUNT__String = Const('LINEITEM__L_DISCOUNT__String', __String)  # define `LINEITEM__L_DISCOUNT__String` for NULL function
String_x7__Int = Const('String_x7__Int', __Int)  # define `String_x7__Int` for NULL function
LINEITEM__L_TAX__String = Const('LINEITEM__L_TAX__String', __String)  # define `LINEITEM__L_TAX__String` for NULL function
String_x8__Int = Const('String_x8__Int', __Int)  # define `String_x8__Int` for NULL function
LINEITEM__L_RETURNFLAG__String = Const('LINEITEM__L_RETURNFLAG__String', __String)  # define `LINEITEM__L_RETURNFLAG__String` for NULL function
String_x9__Int = Const('String_x9__Int', __Int)  # define `String_x9__Int` for NULL function
LINEITEM__L_LINESTATUS__String = Const('LINEITEM__L_LINESTATUS__String', __String)  # define `LINEITEM__L_LINESTATUS__String` for NULL function
String_x10__Int = Const('String_x10__Int', __Int)  # define `String_x10__Int` for NULL function
LINEITEM__L_SHIPDATE__String = Const('LINEITEM__L_SHIPDATE__String', __String)  # define `LINEITEM__L_SHIPDATE__String` for NULL function
String_x11__Int = Const('String_x11__Int', __Int)  # define `String_x11__Int` for NULL function
LINEITEM__L_COMMITDATE__String = Const('LINEITEM__L_COMMITDATE__String', __String)  # define `LINEITEM__L_COMMITDATE__String` for NULL function
String_x12__Int = Const('String_x12__Int', __Int)  # define `String_x12__Int` for NULL function
LINEITEM__L_RECEIPTDATE__String = Const('LINEITEM__L_RECEIPTDATE__String', __String)  # define `LINEITEM__L_RECEIPTDATE__String` for NULL function
String_x13__Int = Const('String_x13__Int', __Int)  # define `String_x13__Int` for NULL function
LINEITEM__L_SHIPINSTRUCT__String = Const('LINEITEM__L_SHIPINSTRUCT__String', __String)  # define `LINEITEM__L_SHIPINSTRUCT__String` for NULL function
String_x14__Int = Const('String_x14__Int', __Int)  # define `String_x14__Int` for NULL function
LINEITEM__L_SHIPMODE__String = Const('LINEITEM__L_SHIPMODE__String', __String)  # define `LINEITEM__L_SHIPMODE__String` for NULL function
String_x15__Int = Const('String_x15__Int', __Int)  # define `String_x15__Int` for NULL function
LINEITEM__L_COMMENT__String = Const('LINEITEM__L_COMMENT__String', __String)  # define `LINEITEM__L_COMMENT__String` for NULL function
String_x16__Int = Const('String_x16__Int', __Int)  # define `String_x16__Int` for NULL function
t2 = Const('t2', __TupleSort)  # define a tuple `t2`
String_x17__Int = Const('String_x17__Int', __Int)  # define `String_x17__Int` for NULL function
String_x18__Int = Const('String_x18__Int', __Int)  # define `String_x18__Int` for NULL function
String_x19__Int = Const('String_x19__Int', __Int)  # define `String_x19__Int` for NULL function
String_x20__Int = Const('String_x20__Int', __Int)  # define `String_x20__Int` for NULL function
String_x21__Int = Const('String_x21__Int', __Int)  # define `String_x21__Int` for NULL function
String_x22__Int = Const('String_x22__Int', __Int)  # define `String_x22__Int` for NULL function
String_x23__Int = Const('String_x23__Int', __Int)  # define `String_x23__Int` for NULL function
String_x24__Int = Const('String_x24__Int', __Int)  # define `String_x24__Int` for NULL function
String_x25__Int = Const('String_x25__Int', __Int)  # define `String_x25__Int` for NULL function
String_x26__Int = Const('String_x26__Int', __Int)  # define `String_x26__Int` for NULL function
String_x27__Int = Const('String_x27__Int', __Int)  # define `String_x27__Int` for NULL function
String_x28__Int = Const('String_x28__Int', __Int)  # define `String_x28__Int` for NULL function
String_x29__Int = Const('String_x29__Int', __Int)  # define `String_x29__Int` for NULL function
String_x30__Int = Const('String_x30__Int', __Int)  # define `String_x30__Int` for NULL function
String_x31__Int = Const('String_x31__Int', __Int)  # define `String_x31__Int` for NULL function
String_x32__Int = Const('String_x32__Int', __Int)  # define `String_x32__Int` for NULL function
t3 = Const('t3', __TupleSort)  # define a tuple `t3`
String_x33__Int = Const('String_x33__Int', __Int)  # define `String_x33__Int` for NULL function
String_x34__Int = Const('String_x34__Int', __Int)  # define `String_x34__Int` for NULL function
String_x35__Int = Const('String_x35__Int', __Int)  # define `String_x35__Int` for NULL function
String_x36__Int = Const('String_x36__Int', __Int)  # define `String_x36__Int` for NULL function
String_x37__Int = Const('String_x37__Int', __Int)  # define `String_x37__Int` for NULL function
String_x38__Int = Const('String_x38__Int', __Int)  # define `String_x38__Int` for NULL function
String_x39__Int = Const('String_x39__Int', __Int)  # define `String_x39__Int` for NULL function
String_x40__Int = Const('String_x40__Int', __Int)  # define `String_x40__Int` for NULL function
String_x41__Int = Const('String_x41__Int', __Int)  # define `String_x41__Int` for NULL function
String_x42__Int = Const('String_x42__Int', __Int)  # define `String_x42__Int` for NULL function
String_x43__Int = Const('String_x43__Int', __Int)  # define `String_x43__Int` for NULL function
String_x44__Int = Const('String_x44__Int', __Int)  # define `String_x44__Int` for NULL function
String_x45__Int = Const('String_x45__Int', __Int)  # define `String_x45__Int` for NULL function
String_x46__Int = Const('String_x46__Int', __Int)  # define `String_x46__Int` for NULL function
String_x47__Int = Const('String_x47__Int', __Int)  # define `String_x47__Int` for NULL function
String_x48__Int = Const('String_x48__Int', __Int)  # define `String_x48__Int` for NULL function
t4 = Const('t4', __TupleSort)  # define a tuple `t4`
String_x49__Int = Const('String_x49__Int', __Int)  # define `String_x49__Int` for NULL function
String_x50__Int = Const('String_x50__Int', __Int)  # define `String_x50__Int` for NULL function
String_x51__Int = Const('String_x51__Int', __Int)  # define `String_x51__Int` for NULL function
String_x52__Int = Const('String_x52__Int', __Int)  # define `String_x52__Int` for NULL function
String_x53__Int = Const('String_x53__Int', __Int)  # define `String_x53__Int` for NULL function
String_x54__Int = Const('String_x54__Int', __Int)  # define `String_x54__Int` for NULL function
String_x55__Int = Const('String_x55__Int', __Int)  # define `String_x55__Int` for NULL function
String_x56__Int = Const('String_x56__Int', __Int)  # define `String_x56__Int` for NULL function
String_x57__Int = Const('String_x57__Int', __Int)  # define `String_x57__Int` for NULL function
String_x58__Int = Const('String_x58__Int', __Int)  # define `String_x58__Int` for NULL function
String_x59__Int = Const('String_x59__Int', __Int)  # define `String_x59__Int` for NULL function
String_x60__Int = Const('String_x60__Int', __Int)  # define `String_x60__Int` for NULL function
String_x61__Int = Const('String_x61__Int', __Int)  # define `String_x61__Int` for NULL function
String_x62__Int = Const('String_x62__Int', __Int)  # define `String_x62__Int` for NULL function
String_x63__Int = Const('String_x63__Int', __Int)  # define `String_x63__Int` for NULL function
String_x64__Int = Const('String_x64__Int', __Int)  # define `String_x64__Int` for NULL function
t5 = Const('t5', __TupleSort)  # define a tuple `t5`
String_x65__Int = Const('String_x65__Int', __Int)  # define `String_x65__Int` for NULL function
String_x66__Int = Const('String_x66__Int', __Int)  # define `String_x66__Int` for NULL function
String_x67__Int = Const('String_x67__Int', __Int)  # define `String_x67__Int` for NULL function
String_x68__Int = Const('String_x68__Int', __Int)  # define `String_x68__Int` for NULL function
String_x69__Int = Const('String_x69__Int', __Int)  # define `String_x69__Int` for NULL function
String_x70__Int = Const('String_x70__Int', __Int)  # define `String_x70__Int` for NULL function
String_x71__Int = Const('String_x71__Int', __Int)  # define `String_x71__Int` for NULL function
String_x72__Int = Const('String_x72__Int', __Int)  # define `String_x72__Int` for NULL function
String_x73__Int = Const('String_x73__Int', __Int)  # define `String_x73__Int` for NULL function
String_x74__Int = Const('String_x74__Int', __Int)  # define `String_x74__Int` for NULL function
String_x75__Int = Const('String_x75__Int', __Int)  # define `String_x75__Int` for NULL function
String_x76__Int = Const('String_x76__Int', __Int)  # define `String_x76__Int` for NULL function
String_x77__Int = Const('String_x77__Int', __Int)  # define `String_x77__Int` for NULL function
String_x78__Int = Const('String_x78__Int', __Int)  # define `String_x78__Int` for NULL function
String_x79__Int = Const('String_x79__Int', __Int)  # define `String_x79__Int` for NULL function
String_x80__Int = Const('String_x80__Int', __Int)  # define `String_x80__Int` for NULL function
t6 = Const('t6', __TupleSort)  # define a tuple `t6`
NATION__N_NATIONKEY__String = Const('NATION__N_NATIONKEY__String', __String)  # define `NATION__N_NATIONKEY__String` for NULL function
String_x81__Int = Const('String_x81__Int', __Int)  # define `String_x81__Int` for NULL function
NATION__N_NAME__String = Const('NATION__N_NAME__String', __String)  # define `NATION__N_NAME__String` for NULL function
String_x82__Int = Const('String_x82__Int', __Int)  # define `String_x82__Int` for NULL function
NATION__N_REGIONKEY__String = Const('NATION__N_REGIONKEY__String', __String)  # define `NATION__N_REGIONKEY__String` for NULL function
String_x83__Int = Const('String_x83__Int', __Int)  # define `String_x83__Int` for NULL function
NATION__N_COMMENT__String = Const('NATION__N_COMMENT__String', __String)  # define `NATION__N_COMMENT__String` for NULL function
String_x84__Int = Const('String_x84__Int', __Int)  # define `String_x84__Int` for NULL function
t7 = Const('t7', __TupleSort)  # define a tuple `t7`
String_x85__Int = Const('String_x85__Int', __Int)  # define `String_x85__Int` for NULL function
String_x86__Int = Const('String_x86__Int', __Int)  # define `String_x86__Int` for NULL function
String_x87__Int = Const('String_x87__Int', __Int)  # define `String_x87__Int` for NULL function
String_x88__Int = Const('String_x88__Int', __Int)  # define `String_x88__Int` for NULL function
t8 = Const('t8', __TupleSort)  # define a tuple `t8`
String_x89__Int = Const('String_x89__Int', __Int)  # define `String_x89__Int` for NULL function
String_x90__Int = Const('String_x90__Int', __Int)  # define `String_x90__Int` for NULL function
String_x91__Int = Const('String_x91__Int', __Int)  # define `String_x91__Int` for NULL function
String_x92__Int = Const('String_x92__Int', __Int)  # define `String_x92__Int` for NULL function
t9 = Const('t9', __TupleSort)  # define a tuple `t9`
String_x93__Int = Const('String_x93__Int', __Int)  # define `String_x93__Int` for NULL function
String_x94__Int = Const('String_x94__Int', __Int)  # define `String_x94__Int` for NULL function
String_x95__Int = Const('String_x95__Int', __Int)  # define `String_x95__Int` for NULL function
String_x96__Int = Const('String_x96__Int', __Int)  # define `String_x96__Int` for NULL function
t10 = Const('t10', __TupleSort)  # define a tuple `t10`
String_x97__Int = Const('String_x97__Int', __Int)  # define `String_x97__Int` for NULL function
String_x98__Int = Const('String_x98__Int', __Int)  # define `String_x98__Int` for NULL function
String_x99__Int = Const('String_x99__Int', __Int)  # define `String_x99__Int` for NULL function
String_x100__Int = Const('String_x100__Int', __Int)  # define `String_x100__Int` for NULL function
t11 = Const('t11', __TupleSort)  # define a tuple `t11`
t12 = Const('t12', __TupleSort)  # define a tuple `t12`
t13 = Const('t13', __TupleSort)  # define a tuple `t13`
t14 = Const('t14', __TupleSort)  # define a tuple `t14`
t15 = Const('t15', __TupleSort)  # define a tuple `t15`
TABLE3__REVENUE__String = Const('TABLE3__REVENUE__String', __String)  # define `TABLE3__REVENUE__String` for NULL function
t16 = Const('t16', __TupleSort)  # define a tuple `t16`
pity_tuple_of_Table4 = Const('pity_tuple_of_Table4', __TupleSort)  # define a tuple `pity_tuple_of_Table4`
t18 = Const('t18', __TupleSort)  # define a tuple `t18`
_find_1st_non_deleted_t19 = Const('_find_1st_non_deleted_t19', __TupleSort)  # define a tuple `_find_1st_non_deleted_t19`
_find_1st_non_deleted_t20 = Const('_find_1st_non_deleted_t20', __TupleSort)  # define a tuple `_find_1st_non_deleted_t20`
_find_1st_non_deleted_t21 = Const('_find_1st_non_deleted_t21', __TupleSort)  # define a tuple `_find_1st_non_deleted_t21`
_find_1st_non_deleted_t22 = Const('_find_1st_non_deleted_t22', __TupleSort)  # define a tuple `_find_1st_non_deleted_t22`
_find_1st_non_deleted_t23 = Const('_find_1st_non_deleted_t23', __TupleSort)  # define a tuple `_find_1st_non_deleted_t23`
_find_1st_non_deleted_t24 = Const('_find_1st_non_deleted_t24', __TupleSort)  # define a tuple `_find_1st_non_deleted_t24`
_find_1st_non_deleted_t25 = Const('_find_1st_non_deleted_t25', __TupleSort)  # define a tuple `_find_1st_non_deleted_t25`
_find_1st_non_deleted_t26 = Const('_find_1st_non_deleted_t26', __TupleSort)  # define a tuple `_find_1st_non_deleted_t26`
_find_1st_non_deleted_t27 = Const('_find_1st_non_deleted_t27', __TupleSort)  # define a tuple `_find_1st_non_deleted_t27`
_limit_t28 = Const('_limit_t28', __TupleSort)  # define a tuple `_limit_t28`
_limit_t29 = Const('_limit_t29', __TupleSort)  # define a tuple `_limit_t29`
_limit_t30 = Const('_limit_t30', __TupleSort)  # define a tuple `_limit_t30`
_limit_t31 = Const('_limit_t31', __TupleSort)  # define a tuple `_limit_t31`
t32 = Const('t32', __TupleSort)  # define a tuple `t32`
t33 = Const('t33', __TupleSort)  # define a tuple `t33`
t34 = Const('t34', __TupleSort)  # define a tuple `t34`
t35 = Const('t35', __TupleSort)  # define a tuple `t35`
t36 = Const('t36', __TupleSort)  # define a tuple `t36`
TABLE6__REVENUE__String = Const('TABLE6__REVENUE__String', __String)  # define `TABLE6__REVENUE__String` for NULL function
t37 = Const('t37', __TupleSort)  # define a tuple `t37`
pity_tuple_of_Table7 = Const('pity_tuple_of_Table7', __TupleSort)  # define a tuple `pity_tuple_of_Table7`
t39 = Const('t39', __TupleSort)  # define a tuple `t39`
_find_1st_non_deleted_t40 = Const('_find_1st_non_deleted_t40', __TupleSort)  # define a tuple `_find_1st_non_deleted_t40`
_find_1st_non_deleted_t41 = Const('_find_1st_non_deleted_t41', __TupleSort)  # define a tuple `_find_1st_non_deleted_t41`
_find_1st_non_deleted_t42 = Const('_find_1st_non_deleted_t42', __TupleSort)  # define a tuple `_find_1st_non_deleted_t42`
_find_1st_non_deleted_t43 = Const('_find_1st_non_deleted_t43', __TupleSort)  # define a tuple `_find_1st_non_deleted_t43`
_find_1st_non_deleted_t44 = Const('_find_1st_non_deleted_t44', __TupleSort)  # define a tuple `_find_1st_non_deleted_t44`
_find_1st_non_deleted_t45 = Const('_find_1st_non_deleted_t45', __TupleSort)  # define a tuple `_find_1st_non_deleted_t45`
_find_1st_non_deleted_t46 = Const('_find_1st_non_deleted_t46', __TupleSort)  # define a tuple `_find_1st_non_deleted_t46`
_find_1st_non_deleted_t47 = Const('_find_1st_non_deleted_t47', __TupleSort)  # define a tuple `_find_1st_non_deleted_t47`
_find_1st_non_deleted_t48 = Const('_find_1st_non_deleted_t48', __TupleSort)  # define a tuple `_find_1st_non_deleted_t48`
_limit_t49 = Const('_limit_t49', __TupleSort)  # define a tuple `_limit_t49`
_limit_t50 = Const('_limit_t50', __TupleSort)  # define a tuple `_limit_t50`
_limit_t51 = Const('_limit_t51', __TupleSort)  # define a tuple `_limit_t51`
_limit_t52 = Const('_limit_t52', __TupleSort)  # define a tuple `_limit_t52`

def _MAX(*args):
    return functools.reduce(lambda x, y: If(x >= y, x, y), args)


def _MIN(*args):
    return functools.reduce(lambda x, y: If(x < y, x, y), args)

DBMS_facts = And(
# Database tuples
Not(DELETED(t1)),
LINEITEM__L_ORDERKEY(t1) == String_x1__Int,
LINEITEM__L_PARTKEY(t1) == String_x2__Int,
LINEITEM__L_SUPPKEY(t1) == String_x3__Int,
LINEITEM__L_LINENUMBER(t1) == String_x4__Int,
LINEITEM__L_QUANTITY(t1) == String_x5__Int,
LINEITEM__L_EXTENDEDPRICE(t1) == String_x6__Int,
LINEITEM__L_DISCOUNT(t1) == String_x7__Int,
LINEITEM__L_TAX(t1) == String_x8__Int,
LINEITEM__L_RETURNFLAG(t1) == String_x9__Int,
LINEITEM__L_LINESTATUS(t1) == String_x10__Int,
LINEITEM__L_SHIPDATE(t1) == String_x11__Int,
LINEITEM__L_COMMITDATE(t1) == String_x12__Int,
LINEITEM__L_RECEIPTDATE(t1) == String_x13__Int,
LINEITEM__L_SHIPINSTRUCT(t1) == String_x14__Int,
LINEITEM__L_SHIPMODE(t1) == String_x15__Int,
LINEITEM__L_COMMENT(t1) == String_x16__Int,
Not(DELETED(t2)),
LINEITEM__L_ORDERKEY(t2) == String_x17__Int,
LINEITEM__L_PARTKEY(t2) == String_x18__Int,
LINEITEM__L_SUPPKEY(t2) == String_x19__Int,
LINEITEM__L_LINENUMBER(t2) == String_x20__Int,
LINEITEM__L_QUANTITY(t2) == String_x21__Int,
LINEITEM__L_EXTENDEDPRICE(t2) == String_x22__Int,
LINEITEM__L_DISCOUNT(t2) == String_x23__Int,
LINEITEM__L_TAX(t2) == String_x24__Int,
LINEITEM__L_RETURNFLAG(t2) == String_x25__Int,
LINEITEM__L_LINESTATUS(t2) == String_x26__Int,
LINEITEM__L_SHIPDATE(t2) == String_x27__Int,
LINEITEM__L_COMMITDATE(t2) == String_x28__Int,
LINEITEM__L_RECEIPTDATE(t2) == String_x29__Int,
LINEITEM__L_SHIPINSTRUCT(t2) == String_x30__Int,
LINEITEM__L_SHIPMODE(t2) == String_x31__Int,
LINEITEM__L_COMMENT(t2) == String_x32__Int,
Not(DELETED(t3)),
LINEITEM__L_ORDERKEY(t3) == String_x33__Int,
LINEITEM__L_PARTKEY(t3) == String_x34__Int,
LINEITEM__L_SUPPKEY(t3) == String_x35__Int,
LINEITEM__L_LINENUMBER(t3) == String_x36__Int,
LINEITEM__L_QUANTITY(t3) == String_x37__Int,
LINEITEM__L_EXTENDEDPRICE(t3) == String_x38__Int,
LINEITEM__L_DISCOUNT(t3) == String_x39__Int,
LINEITEM__L_TAX(t3) == String_x40__Int,
LINEITEM__L_RETURNFLAG(t3) == String_x41__Int,
LINEITEM__L_LINESTATUS(t3) == String_x42__Int,
LINEITEM__L_SHIPDATE(t3) == String_x43__Int,
LINEITEM__L_COMMITDATE(t3) == String_x44__Int,
LINEITEM__L_RECEIPTDATE(t3) == String_x45__Int,
LINEITEM__L_SHIPINSTRUCT(t3) == String_x46__Int,
LINEITEM__L_SHIPMODE(t3) == String_x47__Int,
LINEITEM__L_COMMENT(t3) == String_x48__Int,
Not(DELETED(t4)),
LINEITEM__L_ORDERKEY(t4) == String_x49__Int,
LINEITEM__L_PARTKEY(t4) == String_x50__Int,
LINEITEM__L_SUPPKEY(t4) == String_x51__Int,
LINEITEM__L_LINENUMBER(t4) == String_x52__Int,
LINEITEM__L_QUANTITY(t4) == String_x53__Int,
LINEITEM__L_EXTENDEDPRICE(t4) == String_x54__Int,
LINEITEM__L_DISCOUNT(t4) == String_x55__Int,
LINEITEM__L_TAX(t4) == String_x56__Int,
LINEITEM__L_RETURNFLAG(t4) == String_x57__Int,
LINEITEM__L_LINESTATUS(t4) == String_x58__Int,
LINEITEM__L_SHIPDATE(t4) == String_x59__Int,
LINEITEM__L_COMMITDATE(t4) == String_x60__Int,
LINEITEM__L_RECEIPTDATE(t4) == String_x61__Int,
LINEITEM__L_SHIPINSTRUCT(t4) == String_x62__Int,
LINEITEM__L_SHIPMODE(t4) == String_x63__Int,
LINEITEM__L_COMMENT(t4) == String_x64__Int,
Not(DELETED(t5)),
LINEITEM__L_ORDERKEY(t5) == String_x65__Int,
LINEITEM__L_PARTKEY(t5) == String_x66__Int,
LINEITEM__L_SUPPKEY(t5) == String_x67__Int,
LINEITEM__L_LINENUMBER(t5) == String_x68__Int,
LINEITEM__L_QUANTITY(t5) == String_x69__Int,
LINEITEM__L_EXTENDEDPRICE(t5) == String_x70__Int,
LINEITEM__L_DISCOUNT(t5) == String_x71__Int,
LINEITEM__L_TAX(t5) == String_x72__Int,
LINEITEM__L_RETURNFLAG(t5) == String_x73__Int,
LINEITEM__L_LINESTATUS(t5) == String_x74__Int,
LINEITEM__L_SHIPDATE(t5) == String_x75__Int,
LINEITEM__L_COMMITDATE(t5) == String_x76__Int,
LINEITEM__L_RECEIPTDATE(t5) == String_x77__Int,
LINEITEM__L_SHIPINSTRUCT(t5) == String_x78__Int,
LINEITEM__L_SHIPMODE(t5) == String_x79__Int,
LINEITEM__L_COMMENT(t5) == String_x80__Int,
-2147483648 <= LINEITEM__L_ORDERKEY(t1),
2147483647 >= LINEITEM__L_ORDERKEY(t1),
-2147483648 <= LINEITEM__L_PARTKEY(t1),
2147483647 >= LINEITEM__L_PARTKEY(t1),
-2147483648 <= LINEITEM__L_SUPPKEY(t1),
2147483647 >= LINEITEM__L_SUPPKEY(t1),
-2147483648 <= LINEITEM__L_LINENUMBER(t1),
2147483647 >= LINEITEM__L_LINENUMBER(t1),
2147483647 < LINEITEM__L_RETURNFLAG(t1),
2147483647 < LINEITEM__L_LINESTATUS(t1),
1 <= LINEITEM__L_SHIPDATE(t1),
2932897 >= LINEITEM__L_SHIPDATE(t1),
1 <= LINEITEM__L_COMMITDATE(t1),
2932897 >= LINEITEM__L_COMMITDATE(t1),
1 <= LINEITEM__L_RECEIPTDATE(t1),
2932897 >= LINEITEM__L_RECEIPTDATE(t1),
2147483647 < LINEITEM__L_SHIPINSTRUCT(t1),
2147483647 < LINEITEM__L_SHIPMODE(t1),
2147483647 < LINEITEM__L_COMMENT(t1),
-2147483648 <= LINEITEM__L_ORDERKEY(t2),
2147483647 >= LINEITEM__L_ORDERKEY(t2),
-2147483648 <= LINEITEM__L_PARTKEY(t2),
2147483647 >= LINEITEM__L_PARTKEY(t2),
-2147483648 <= LINEITEM__L_SUPPKEY(t2),
2147483647 >= LINEITEM__L_SUPPKEY(t2),
-2147483648 <= LINEITEM__L_LINENUMBER(t2),
2147483647 >= LINEITEM__L_LINENUMBER(t2),
2147483647 < LINEITEM__L_RETURNFLAG(t2),
2147483647 < LINEITEM__L_LINESTATUS(t2),
1 <= LINEITEM__L_SHIPDATE(t2),
2932897 >= LINEITEM__L_SHIPDATE(t2),
1 <= LINEITEM__L_COMMITDATE(t2),
2932897 >= LINEITEM__L_COMMITDATE(t2),
1 <= LINEITEM__L_RECEIPTDATE(t2),
2932897 >= LINEITEM__L_RECEIPTDATE(t2),
2147483647 < LINEITEM__L_SHIPINSTRUCT(t2),
2147483647 < LINEITEM__L_SHIPMODE(t2),
2147483647 < LINEITEM__L_COMMENT(t2),
-2147483648 <= LINEITEM__L_ORDERKEY(t3),
2147483647 >= LINEITEM__L_ORDERKEY(t3),
-2147483648 <= LINEITEM__L_PARTKEY(t3),
2147483647 >= LINEITEM__L_PARTKEY(t3),
-2147483648 <= LINEITEM__L_SUPPKEY(t3),
2147483647 >= LINEITEM__L_SUPPKEY(t3),
-2147483648 <= LINEITEM__L_LINENUMBER(t3),
2147483647 >= LINEITEM__L_LINENUMBER(t3),
2147483647 < LINEITEM__L_RETURNFLAG(t3),
2147483647 < LINEITEM__L_LINESTATUS(t3),
1 <= LINEITEM__L_SHIPDATE(t3),
2932897 >= LINEITEM__L_SHIPDATE(t3),
1 <= LINEITEM__L_COMMITDATE(t3),
2932897 >= LINEITEM__L_COMMITDATE(t3),
1 <= LINEITEM__L_RECEIPTDATE(t3),
2932897 >= LINEITEM__L_RECEIPTDATE(t3),
2147483647 < LINEITEM__L_SHIPINSTRUCT(t3),
2147483647 < LINEITEM__L_SHIPMODE(t3),
2147483647 < LINEITEM__L_COMMENT(t3),
-2147483648 <= LINEITEM__L_ORDERKEY(t4),
2147483647 >= LINEITEM__L_ORDERKEY(t4),
-2147483648 <= LINEITEM__L_PARTKEY(t4),
2147483647 >= LINEITEM__L_PARTKEY(t4),
-2147483648 <= LINEITEM__L_SUPPKEY(t4),
2147483647 >= LINEITEM__L_SUPPKEY(t4),
-2147483648 <= LINEITEM__L_LINENUMBER(t4),
2147483647 >= LINEITEM__L_LINENUMBER(t4),
2147483647 < LINEITEM__L_RETURNFLAG(t4),
2147483647 < LINEITEM__L_LINESTATUS(t4),
1 <= LINEITEM__L_SHIPDATE(t4),
2932897 >= LINEITEM__L_SHIPDATE(t4),
1 <= LINEITEM__L_COMMITDATE(t4),
2932897 >= LINEITEM__L_COMMITDATE(t4),
1 <= LINEITEM__L_RECEIPTDATE(t4),
2932897 >= LINEITEM__L_RECEIPTDATE(t4),
2147483647 < LINEITEM__L_SHIPINSTRUCT(t4),
2147483647 < LINEITEM__L_SHIPMODE(t4),
2147483647 < LINEITEM__L_COMMENT(t4),
-2147483648 <= LINEITEM__L_ORDERKEY(t5),
2147483647 >= LINEITEM__L_ORDERKEY(t5),
-2147483648 <= LINEITEM__L_PARTKEY(t5),
2147483647 >= LINEITEM__L_PARTKEY(t5),
-2147483648 <= LINEITEM__L_SUPPKEY(t5),
2147483647 >= LINEITEM__L_SUPPKEY(t5),
-2147483648 <= LINEITEM__L_LINENUMBER(t5),
2147483647 >= LINEITEM__L_LINENUMBER(t5),
2147483647 < LINEITEM__L_RETURNFLAG(t5),
2147483647 < LINEITEM__L_LINESTATUS(t5),
1 <= LINEITEM__L_SHIPDATE(t5),
2932897 >= LINEITEM__L_SHIPDATE(t5),
1 <= LINEITEM__L_COMMITDATE(t5),
2932897 >= LINEITEM__L_COMMITDATE(t5),
1 <= LINEITEM__L_RECEIPTDATE(t5),
2932897 >= LINEITEM__L_RECEIPTDATE(t5),
2147483647 < LINEITEM__L_SHIPINSTRUCT(t5),
2147483647 < LINEITEM__L_SHIPMODE(t5),
2147483647 < LINEITEM__L_COMMENT(t5),
Not(DELETED(t6)),
NATION__N_NATIONKEY(t6) == String_x81__Int,
NATION__N_NAME(t6) == String_x82__Int,
NATION__N_REGIONKEY(t6) == String_x83__Int,
NATION__N_COMMENT(t6) == String_x84__Int,
Not(DELETED(t7)),
NATION__N_NATIONKEY(t7) == String_x85__Int,
NATION__N_NAME(t7) == String_x86__Int,
NATION__N_REGIONKEY(t7) == String_x87__Int,
NATION__N_COMMENT(t7) == String_x88__Int,
Not(DELETED(t8)),
NATION__N_NATIONKEY(t8) == String_x89__Int,
NATION__N_NAME(t8) == String_x90__Int,
NATION__N_REGIONKEY(t8) == String_x91__Int,
NATION__N_COMMENT(t8) == String_x92__Int,
Not(DELETED(t9)),
NATION__N_NATIONKEY(t9) == String_x93__Int,
NATION__N_NAME(t9) == String_x94__Int,
NATION__N_REGIONKEY(t9) == String_x95__Int,
NATION__N_COMMENT(t9) == String_x96__Int,
Not(DELETED(t10)),
NATION__N_NATIONKEY(t10) == String_x97__Int,
NATION__N_NAME(t10) == String_x98__Int,
NATION__N_REGIONKEY(t10) == String_x99__Int,
NATION__N_COMMENT(t10) == String_x100__Int,
2147483647 < NATION__N_NAME(t6),
-2147483648 <= NATION__N_REGIONKEY(t6),
2147483647 >= NATION__N_REGIONKEY(t6),
2147483647 < NATION__N_COMMENT(t6),
2147483647 < NATION__N_NAME(t7),
-2147483648 <= NATION__N_REGIONKEY(t7),
2147483647 >= NATION__N_REGIONKEY(t7),
2147483647 < NATION__N_COMMENT(t7),
2147483647 < NATION__N_NAME(t8),
-2147483648 <= NATION__N_REGIONKEY(t8),
2147483647 >= NATION__N_REGIONKEY(t8),
2147483647 < NATION__N_COMMENT(t8),
2147483647 < NATION__N_NAME(t9),
-2147483648 <= NATION__N_REGIONKEY(t9),
2147483647 >= NATION__N_REGIONKEY(t9),
2147483647 < NATION__N_COMMENT(t9),
2147483647 < NATION__N_NAME(t10),
-2147483648 <= NATION__N_REGIONKEY(t10),
2147483647 >= NATION__N_REGIONKEY(t10),
2147483647 < NATION__N_COMMENT(t10),
And(Not(NULL(t1, LINEITEM__L_ORDERKEY__String)),
    Not(NULL(t2, LINEITEM__L_ORDERKEY__String)),
    Not(NULL(t3, LINEITEM__L_ORDERKEY__String)),
    Not(NULL(t4, LINEITEM__L_ORDERKEY__String)),
    Not(NULL(t5, LINEITEM__L_ORDERKEY__String)),
    LINEITEM__L_ORDERKEY(t1) != LINEITEM__L_ORDERKEY(t2),
    LINEITEM__L_ORDERKEY(t1) != LINEITEM__L_ORDERKEY(t3),
    LINEITEM__L_ORDERKEY(t1) != LINEITEM__L_ORDERKEY(t4),
    LINEITEM__L_ORDERKEY(t1) != LINEITEM__L_ORDERKEY(t5),
    LINEITEM__L_ORDERKEY(t2) != LINEITEM__L_ORDERKEY(t3),
    LINEITEM__L_ORDERKEY(t2) != LINEITEM__L_ORDERKEY(t4),
    LINEITEM__L_ORDERKEY(t2) != LINEITEM__L_ORDERKEY(t5),
    LINEITEM__L_ORDERKEY(t3) != LINEITEM__L_ORDERKEY(t4),
    LINEITEM__L_ORDERKEY(t3) != LINEITEM__L_ORDERKEY(t5),
    LINEITEM__L_ORDERKEY(t4) != LINEITEM__L_ORDERKEY(t5)),
And(Not(NULL(t6, NATION__N_NATIONKEY__String)),
    Not(NULL(t7, NATION__N_NATIONKEY__String)),
    Not(NULL(t8, NATION__N_NATIONKEY__String)),
    Not(NULL(t9, NATION__N_NATIONKEY__String)),
    Not(NULL(t10, NATION__N_NATIONKEY__String)),
    NATION__N_NATIONKEY(t6) != NATION__N_NATIONKEY(t7),
    NATION__N_NATIONKEY(t6) != NATION__N_NATIONKEY(t8),
    NATION__N_NATIONKEY(t6) != NATION__N_NATIONKEY(t9),
    NATION__N_NATIONKEY(t6) != NATION__N_NATIONKEY(t10),
    NATION__N_NATIONKEY(t7) != NATION__N_NATIONKEY(t8),
    NATION__N_NATIONKEY(t7) != NATION__N_NATIONKEY(t9),
    NATION__N_NATIONKEY(t7) != NATION__N_NATIONKEY(t10),
    NATION__N_NATIONKEY(t8) != NATION__N_NATIONKEY(t9),
    NATION__N_NATIONKEY(t8) != NATION__N_NATIONKEY(t10),
    NATION__N_NATIONKEY(t9) != NATION__N_NATIONKEY(t10))
)

premise1 = And(
# 1st SQL query formulas
# t11 := Filter(['t1'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_lt_LINEITEM__L_QUANTITY_Digits_26))
And(
    Implies(
        And(*[Not(DELETED(t1)), If(If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t1))))),
      False,
      Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t1, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t1, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t1))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t1),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)),
          26 > LINEITEM__L_QUANTITY(t1))))]),
        And(Not(DELETED(t11)), t11 == t1),
    ),
    Implies(Not(And(*[Not(DELETED(t1)), If(If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t1))))),
      False,
      Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t1, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t1, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t1))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t1),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)),
          26 > LINEITEM__L_QUANTITY(t1))))])), DELETED(t11)),
),

# t12 := Filter(['t2'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_lt_LINEITEM__L_QUANTITY_Digits_26))
And(
    Implies(
        And(*[Not(DELETED(t2)), If(If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t2))))),
      False,
      Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t2, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t2, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t2))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t2),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)),
          26 > LINEITEM__L_QUANTITY(t2))))]),
        And(Not(DELETED(t12)), t12 == t2),
    ),
    Implies(Not(And(*[Not(DELETED(t2)), If(If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t2))))),
      False,
      Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t2, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t2, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t2))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t2),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)),
          26 > LINEITEM__L_QUANTITY(t2))))])), DELETED(t12)),
),

# t13 := Filter(['t3'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_lt_LINEITEM__L_QUANTITY_Digits_26))
And(
    Implies(
        And(*[Not(DELETED(t3)), If(If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t3))))),
      False,
      Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t3, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t3, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t3))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t3),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)),
          26 > LINEITEM__L_QUANTITY(t3))))]),
        And(Not(DELETED(t13)), t13 == t3),
    ),
    Implies(Not(And(*[Not(DELETED(t3)), If(If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t3))))),
      False,
      Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t3, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t3, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t3))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t3),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)),
          26 > LINEITEM__L_QUANTITY(t3))))])), DELETED(t13)),
),

# t14 := Filter(['t4'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_lt_LINEITEM__L_QUANTITY_Digits_26))
And(
    Implies(
        And(*[Not(DELETED(t4)), If(If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t4))))),
      False,
      Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t4, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t4, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t4))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t4),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)),
          26 > LINEITEM__L_QUANTITY(t4))))]),
        And(Not(DELETED(t14)), t14 == t4),
    ),
    Implies(Not(And(*[Not(DELETED(t4)), If(If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t4))))),
      False,
      Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t4, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t4, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t4))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t4),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)),
          26 > LINEITEM__L_QUANTITY(t4))))])), DELETED(t14)),
),

# t15 := Filter(['t5'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_lt_LINEITEM__L_QUANTITY_Digits_26))
And(
    Implies(
        And(*[Not(DELETED(t5)), If(If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t5))))),
      False,
      Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t5, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t5, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t5))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t5),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)),
          26 > LINEITEM__L_QUANTITY(t5))))]),
        And(Not(DELETED(t15)), t15 == t5),
    ),
    Implies(Not(And(*[Not(DELETED(t5)), If(If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t5))))),
      False,
      Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t5, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t5, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(26 > LINEITEM__L_QUANTITY(t5))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t5),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)),
          26 > LINEITEM__L_QUANTITY(t5))))])), DELETED(t15)),
),

# t16 := Projection(['t11', 't12', 't13', 't14', 't15'], Cond=[TABLE3__REVENUE])
And(*[
    Implies(
        Or(Not(DELETED(t11)),
   Not(DELETED(t12)),
   Not(DELETED(t13)),
   Not(DELETED(t14)),
   Not(DELETED(t15))),
        And(
Not(DELETED(t16)),
And(_find_1st_non_deleted_t19 == t11,
    _find_1st_non_deleted_t20 == t12,
    _find_1st_non_deleted_t21 == t13,
    _find_1st_non_deleted_t22 == t14,
    _find_1st_non_deleted_t23 == t15,
    If(And(DELETED(_find_1st_non_deleted_t19),
           Not(DELETED(_find_1st_non_deleted_t20))),
       _find_1st_non_deleted_t24 ==
       _find_1st_non_deleted_t20,
       _find_1st_non_deleted_t24 ==
       _find_1st_non_deleted_t19),
    If(And(DELETED(_find_1st_non_deleted_t24),
           Not(DELETED(_find_1st_non_deleted_t21))),
       _find_1st_non_deleted_t25 ==
       _find_1st_non_deleted_t21,
       _find_1st_non_deleted_t25 ==
       _find_1st_non_deleted_t24),
    If(And(DELETED(_find_1st_non_deleted_t25),
           Not(DELETED(_find_1st_non_deleted_t22))),
       _find_1st_non_deleted_t26 ==
       _find_1st_non_deleted_t22,
       _find_1st_non_deleted_t26 ==
       _find_1st_non_deleted_t25),
    If(And(DELETED(_find_1st_non_deleted_t26),
           Not(DELETED(_find_1st_non_deleted_t23))),
       _find_1st_non_deleted_t27 ==
       _find_1st_non_deleted_t23,
       _find_1st_non_deleted_t27 ==
       _find_1st_non_deleted_t26)),
And(NULL(t16, TABLE3__REVENUE__String) ==
    And(Or(DELETED(t11),
           Or(NULL(t11, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t11, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t12),
           Or(NULL(t12, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t12, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t13),
           Or(NULL(t13, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t13, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t14),
           Or(NULL(t14, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t14, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t15),
           Or(NULL(t15, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t15, LINEITEM__L_DISCOUNT__String)))),
    TABLE3__REVENUE(t16) ==
    If(And(Or(DELETED(t11),
              Or(NULL(t11,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t11, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t12),
              Or(NULL(t12,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t12, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t13),
              Or(NULL(t13,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t13, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t14),
              Or(NULL(t14,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t14, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t15),
              Or(NULL(t15,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t15, LINEITEM__L_DISCOUNT__String)))),
       -10,
       If(Or(DELETED(t11),
             Or(NULL(t11, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t11, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t11)*
          LINEITEM__L_DISCOUNT(t11)) +
       If(Or(DELETED(t12),
             Or(NULL(t12, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t12, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t12)*
          LINEITEM__L_DISCOUNT(t12)) +
       If(Or(DELETED(t13),
             Or(NULL(t13, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t13, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t13)*
          LINEITEM__L_DISCOUNT(t13)) +
       If(Or(DELETED(t14),
             Or(NULL(t14, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t14, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t14)*
          LINEITEM__L_DISCOUNT(t14)) +
       If(Or(DELETED(t15),
             Or(NULL(t15, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t15, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t15)*
          LINEITEM__L_DISCOUNT(t15)))),
        ),
    ),
    Implies(Not(Or(Not(DELETED(t11)),
   Not(DELETED(t12)),
   Not(DELETED(t13)),
   Not(DELETED(t14)),
   Not(DELETED(t15)))), DELETED(t16)),
]),

# pity_tuple_of_Table4 := ProjectionPity(['t11', 't12', 't13', 't14', 't15'], Cond=[TABLE3__REVENUE])
And(
Implies(And(DELETED(t11),
    DELETED(t12),
    DELETED(t13),
    DELETED(t14),
    DELETED(t15)), And(
    Not(DELETED(pity_tuple_of_Table4)),
    And(NULL(pity_tuple_of_Table4, TABLE3__REVENUE__String) ==
    And(Or(DELETED(t11),
           Or(NULL(t11, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t11, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t12),
           Or(NULL(t12, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t12, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t13),
           Or(NULL(t13, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t13, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t14),
           Or(NULL(t14, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t14, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t15),
           Or(NULL(t15, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t15, LINEITEM__L_DISCOUNT__String)))),
    TABLE3__REVENUE(pity_tuple_of_Table4) ==
    If(And(Or(DELETED(t11),
              Or(NULL(t11,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t11, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t12),
              Or(NULL(t12,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t12, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t13),
              Or(NULL(t13,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t13, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t14),
              Or(NULL(t14,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t14, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t15),
              Or(NULL(t15,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t15, LINEITEM__L_DISCOUNT__String)))),
       -10,
       If(Or(DELETED(t11),
             Or(NULL(t11, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t11, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t11)*
          LINEITEM__L_DISCOUNT(t11)) +
       If(Or(DELETED(t12),
             Or(NULL(t12, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t12, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t12)*
          LINEITEM__L_DISCOUNT(t12)) +
       If(Or(DELETED(t13),
             Or(NULL(t13, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t13, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t13)*
          LINEITEM__L_DISCOUNT(t13)) +
       If(Or(DELETED(t14),
             Or(NULL(t14, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t14, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t14)*
          LINEITEM__L_DISCOUNT(t14)) +
       If(Or(DELETED(t15),
             Or(NULL(t15, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t15, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t15)*
          LINEITEM__L_DISCOUNT(t15)))),
)),
Implies(Not(And(DELETED(t11),
    DELETED(t12),
    DELETED(t13),
    DELETED(t14),
    DELETED(t15))), DELETED(pity_tuple_of_Table4)),
),

# __Table4_LIMIT_0_1__ LIMIT constraint of dropping the deleted tuples to the end of the table
And(
_limit_t28 == t16,
_limit_t29 == pity_tuple_of_Table4,
If(And(DELETED(_limit_t28), Not(DELETED(_limit_t29))),
   And(_limit_t30 == _limit_t29, _limit_t31 == _limit_t28),
   And(_limit_t30 == _limit_t28, _limit_t31 == _limit_t29))
),

# t18 := Limit(['t16'])
t18 == _limit_t30
)

premise2 = And(
# 2nd SQL query formulas
# t32 := Filter(['t1'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_gt_LINEITEM__L_QUANTITY_Digits_41))
And(
    Implies(
        And(*[Not(DELETED(t1)), If(If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t1))))),
      False,
      Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t1, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t1, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t1))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t1),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)),
          41 < LINEITEM__L_QUANTITY(t1))))]),
        And(Not(DELETED(t32)), t32 == t1),
    ),
    Implies(Not(And(*[Not(DELETED(t1)), If(If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t1))))),
      False,
      Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t1, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t1, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t1, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t1))),
             If(Or(NULL(t1, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)))),
             If(Or(NULL(t1, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t1))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t1),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t1)),
          41 < LINEITEM__L_QUANTITY(t1))))])), DELETED(t32)),
),

# t33 := Filter(['t2'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_gt_LINEITEM__L_QUANTITY_Digits_41))
And(
    Implies(
        And(*[Not(DELETED(t2)), If(If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t2))))),
      False,
      Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t2, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t2, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t2))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t2),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)),
          41 < LINEITEM__L_QUANTITY(t2))))]),
        And(Not(DELETED(t33)), t33 == t2),
    ),
    Implies(Not(And(*[Not(DELETED(t2)), If(If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t2))))),
      False,
      Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t2, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t2, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t2, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t2))),
             If(Or(NULL(t2, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)))),
             If(Or(NULL(t2, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t2))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t2),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t2)),
          41 < LINEITEM__L_QUANTITY(t2))))])), DELETED(t33)),
),

# t34 := Filter(['t3'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_gt_LINEITEM__L_QUANTITY_Digits_41))
And(
    Implies(
        And(*[Not(DELETED(t3)), If(If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t3))))),
      False,
      Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t3, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t3, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t3))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t3),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)),
          41 < LINEITEM__L_QUANTITY(t3))))]),
        And(Not(DELETED(t34)), t34 == t3),
    ),
    Implies(Not(And(*[Not(DELETED(t3)), If(If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t3))))),
      False,
      Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t3, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t3, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t3, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t3))),
             If(Or(NULL(t3, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)))),
             If(Or(NULL(t3, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t3))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t3),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t3)),
          41 < LINEITEM__L_QUANTITY(t3))))])), DELETED(t34)),
),

# t35 := Filter(['t4'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_gt_LINEITEM__L_QUANTITY_Digits_41))
And(
    Implies(
        And(*[Not(DELETED(t4)), If(If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t4))))),
      False,
      Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t4, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t4, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t4))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t4),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)),
          41 < LINEITEM__L_QUANTITY(t4))))]),
        And(Not(DELETED(t35)), t35 == t4),
    ),
    Implies(Not(And(*[Not(DELETED(t4)), If(If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t4))))),
      False,
      Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t4, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t4, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t4, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t4))),
             If(Or(NULL(t4, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)))),
             If(Or(NULL(t4, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t4))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t4),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t4)),
          41 < LINEITEM__L_QUANTITY(t4))))])), DELETED(t35)),
),

# t36 := Filter(['t5'], Cond=(and_gte_LINEITEM__L_SHIPDATE_Digits_8402_gt_LINEITEM__L_DISCOUNT_Digits_0.08_gt_LINEITEM__L_QUANTITY_Digits_41))
And(
    Implies(
        And(*[Not(DELETED(t5)), If(If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t5))))),
      False,
      Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t5, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t5, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t5))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t5),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)),
          41 < LINEITEM__L_QUANTITY(t5))))]),
        And(Not(DELETED(t36)), t36 == t5),
    ),
    Implies(Not(And(*[Not(DELETED(t5)), If(If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t5))))),
      False,
      Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String), False),
         Or(NULL(t5, LINEITEM__L_DISCOUNT__String), False),
         Or(NULL(t5, LINEITEM__L_QUANTITY__String), False))),
   False,
   If(And(Or(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                False),
             Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                False),
             Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                False)),
          Or(If(Or(NULL(t5, LINEITEM__L_SHIPDATE__String),
                   False),
                False,
                Not(8402 <= LINEITEM__L_SHIPDATE(t5))),
             If(Or(NULL(t5, LINEITEM__L_DISCOUNT__String),
                   False),
                False,
                Not(2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)))),
             If(Or(NULL(t5, LINEITEM__L_QUANTITY__String),
                   False),
                False,
                Not(41 < LINEITEM__L_QUANTITY(t5))))),
      False,
      And(8402 <= LINEITEM__L_SHIPDATE(t5),
          2/25 < ToReal(LINEITEM__L_DISCOUNT(t5)),
          41 < LINEITEM__L_QUANTITY(t5))))])), DELETED(t36)),
),

# t37 := Projection(['t32', 't33', 't34', 't35', 't36'], Cond=[TABLE6__REVENUE])
And(*[
    Implies(
        Or(Not(DELETED(t32)),
   Not(DELETED(t33)),
   Not(DELETED(t34)),
   Not(DELETED(t35)),
   Not(DELETED(t36))),
        And(
Not(DELETED(t37)),
And(_find_1st_non_deleted_t40 == t32,
    _find_1st_non_deleted_t41 == t33,
    _find_1st_non_deleted_t42 == t34,
    _find_1st_non_deleted_t43 == t35,
    _find_1st_non_deleted_t44 == t36,
    If(And(DELETED(_find_1st_non_deleted_t40),
           Not(DELETED(_find_1st_non_deleted_t41))),
       _find_1st_non_deleted_t45 ==
       _find_1st_non_deleted_t41,
       _find_1st_non_deleted_t45 ==
       _find_1st_non_deleted_t40),
    If(And(DELETED(_find_1st_non_deleted_t45),
           Not(DELETED(_find_1st_non_deleted_t42))),
       _find_1st_non_deleted_t46 ==
       _find_1st_non_deleted_t42,
       _find_1st_non_deleted_t46 ==
       _find_1st_non_deleted_t45),
    If(And(DELETED(_find_1st_non_deleted_t46),
           Not(DELETED(_find_1st_non_deleted_t43))),
       _find_1st_non_deleted_t47 ==
       _find_1st_non_deleted_t43,
       _find_1st_non_deleted_t47 ==
       _find_1st_non_deleted_t46),
    If(And(DELETED(_find_1st_non_deleted_t47),
           Not(DELETED(_find_1st_non_deleted_t44))),
       _find_1st_non_deleted_t48 ==
       _find_1st_non_deleted_t44,
       _find_1st_non_deleted_t48 ==
       _find_1st_non_deleted_t47)),
And(NULL(t37, TABLE6__REVENUE__String) ==
    And(Or(DELETED(t32),
           Or(NULL(t32, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t32, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t33),
           Or(NULL(t33, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t33, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t34),
           Or(NULL(t34, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t34, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t35),
           Or(NULL(t35, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t35, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t36),
           Or(NULL(t36, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t36, LINEITEM__L_DISCOUNT__String)))),
    TABLE6__REVENUE(t37) ==
    If(And(Or(DELETED(t32),
              Or(NULL(t32,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t32, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t33),
              Or(NULL(t33,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t33, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t34),
              Or(NULL(t34,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t34, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t35),
              Or(NULL(t35,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t35, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t36),
              Or(NULL(t36,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t36, LINEITEM__L_DISCOUNT__String)))),
       -10,
       If(Or(DELETED(t32),
             Or(NULL(t32, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t32, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t32)*
          LINEITEM__L_DISCOUNT(t32)) +
       If(Or(DELETED(t33),
             Or(NULL(t33, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t33, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t33)*
          LINEITEM__L_DISCOUNT(t33)) +
       If(Or(DELETED(t34),
             Or(NULL(t34, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t34, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t34)*
          LINEITEM__L_DISCOUNT(t34)) +
       If(Or(DELETED(t35),
             Or(NULL(t35, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t35, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t35)*
          LINEITEM__L_DISCOUNT(t35)) +
       If(Or(DELETED(t36),
             Or(NULL(t36, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t36, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t36)*
          LINEITEM__L_DISCOUNT(t36)))),
        ),
    ),
    Implies(Not(Or(Not(DELETED(t32)),
   Not(DELETED(t33)),
   Not(DELETED(t34)),
   Not(DELETED(t35)),
   Not(DELETED(t36)))), DELETED(t37)),
]),

# pity_tuple_of_Table7 := ProjectionPity(['t32', 't33', 't34', 't35', 't36'], Cond=[TABLE6__REVENUE])
And(
Implies(And(DELETED(t32),
    DELETED(t33),
    DELETED(t34),
    DELETED(t35),
    DELETED(t36)), And(
    Not(DELETED(pity_tuple_of_Table7)),
    And(NULL(pity_tuple_of_Table7, TABLE6__REVENUE__String) ==
    And(Or(DELETED(t32),
           Or(NULL(t32, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t32, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t33),
           Or(NULL(t33, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t33, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t34),
           Or(NULL(t34, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t34, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t35),
           Or(NULL(t35, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t35, LINEITEM__L_DISCOUNT__String))),
        Or(DELETED(t36),
           Or(NULL(t36, LINEITEM__L_EXTENDEDPRICE__String),
              NULL(t36, LINEITEM__L_DISCOUNT__String)))),
    TABLE6__REVENUE(pity_tuple_of_Table7) ==
    If(And(Or(DELETED(t32),
              Or(NULL(t32,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t32, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t33),
              Or(NULL(t33,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t33, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t34),
              Or(NULL(t34,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t34, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t35),
              Or(NULL(t35,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t35, LINEITEM__L_DISCOUNT__String))),
           Or(DELETED(t36),
              Or(NULL(t36,
                      LINEITEM__L_EXTENDEDPRICE__String),
                 NULL(t36, LINEITEM__L_DISCOUNT__String)))),
       -10,
       If(Or(DELETED(t32),
             Or(NULL(t32, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t32, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t32)*
          LINEITEM__L_DISCOUNT(t32)) +
       If(Or(DELETED(t33),
             Or(NULL(t33, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t33, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t33)*
          LINEITEM__L_DISCOUNT(t33)) +
       If(Or(DELETED(t34),
             Or(NULL(t34, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t34, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t34)*
          LINEITEM__L_DISCOUNT(t34)) +
       If(Or(DELETED(t35),
             Or(NULL(t35, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t35, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t35)*
          LINEITEM__L_DISCOUNT(t35)) +
       If(Or(DELETED(t36),
             Or(NULL(t36, LINEITEM__L_EXTENDEDPRICE__String),
                NULL(t36, LINEITEM__L_DISCOUNT__String))),
          0,
          LINEITEM__L_EXTENDEDPRICE(t36)*
          LINEITEM__L_DISCOUNT(t36)))),
)),
Implies(Not(And(DELETED(t32),
    DELETED(t33),
    DELETED(t34),
    DELETED(t35),
    DELETED(t36))), DELETED(pity_tuple_of_Table7)),
),

# __Table7_LIMIT_0_1__ LIMIT constraint of dropping the deleted tuples to the end of the table
And(
_limit_t49 == t37,
_limit_t50 == pity_tuple_of_Table7,
If(And(DELETED(_limit_t49), Not(DELETED(_limit_t50))),
   And(_limit_t51 == _limit_t50, _limit_t52 == _limit_t49),
   And(_limit_t51 == _limit_t49, _limit_t52 == _limit_t50))
),

# t39 := Limit(['t37'])
t39 == _limit_t51
)

premise = And(DBMS_facts, premise1, premise2)

def equals(ltuples, rtuples):
    left_left_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, TABLE3__REVENUE__String), NULL(tuple2, TABLE3__REVENUE__String)), And(Not(NULL(tuple1, TABLE3__REVENUE__String)), Not(NULL(tuple2, TABLE3__REVENUE__String)), TABLE3__REVENUE(tuple1) == TABLE3__REVENUE(tuple2))),
    )
)
    left_right_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, TABLE3__REVENUE__String), NULL(tuple2, TABLE6__REVENUE__String)), And(Not(NULL(tuple1, TABLE3__REVENUE__String)), Not(NULL(tuple2, TABLE6__REVENUE__String)), TABLE3__REVENUE(tuple1) == TABLE6__REVENUE(tuple2))),
    )
)
    right_left_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, TABLE6__REVENUE__String), NULL(tuple2, TABLE3__REVENUE__String)), And(Not(NULL(tuple1, TABLE6__REVENUE__String)), Not(NULL(tuple2, TABLE3__REVENUE__String)), TABLE6__REVENUE(tuple1) == TABLE3__REVENUE(tuple2))),
    )
)
    right_right_function = lambda tuple1, tuple2: Or(
    And(DELETED(tuple1), DELETED(tuple2)),
    And(
        Not(DELETED(tuple1)),
        Not(DELETED(tuple2)),
        Or(And(NULL(tuple1, TABLE6__REVENUE__String), NULL(tuple2, TABLE6__REVENUE__String)), And(Not(NULL(tuple1, TABLE6__REVENUE__String)), Not(NULL(tuple2, TABLE6__REVENUE__String)), TABLE6__REVENUE(tuple1) == TABLE6__REVENUE(tuple2))),
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

conclusion = equals(ltuples=[t18], rtuples=[t39])

solver = Solver()

solver.add(Not(Implies(premise, conclusion)))
print(f'Symbolic Reasoning Output: ==> {solver.check()} <==')
model = solver.model()
#print(model)
for t in [t11, t12, t13, t14, t15, t16, pity_tuple_of_Table4, t18, t32, t33, t34, t35, t36, t37, pity_tuple_of_Table7, t39]:
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
	_f(NULL(t1, LINEITEM__L_ORDERKEY__String), LINEITEM__L_ORDERKEY(t1)),
',',
	_f(NULL(t1, LINEITEM__L_PARTKEY__String), LINEITEM__L_PARTKEY(t1)),
',',
	_f(NULL(t1, LINEITEM__L_SUPPKEY__String), LINEITEM__L_SUPPKEY(t1)),
',',
	_f(NULL(t1, LINEITEM__L_LINENUMBER__String), LINEITEM__L_LINENUMBER(t1)),
',',
	_f(NULL(t1, LINEITEM__L_QUANTITY__String), LINEITEM__L_QUANTITY(t1)),
',',
	_f(NULL(t1, LINEITEM__L_EXTENDEDPRICE__String), LINEITEM__L_EXTENDEDPRICE(t1)),
',',
	_f(NULL(t1, LINEITEM__L_DISCOUNT__String), LINEITEM__L_DISCOUNT(t1)),
',',
	_f(NULL(t1, LINEITEM__L_TAX__String), LINEITEM__L_TAX(t1)),
',',
	_f(NULL(t1, LINEITEM__L_RETURNFLAG__String), LINEITEM__L_RETURNFLAG(t1)),
',',
	_f(NULL(t1, LINEITEM__L_LINESTATUS__String), LINEITEM__L_LINESTATUS(t1)),
',',
	_f(NULL(t1, LINEITEM__L_SHIPDATE__String), LINEITEM__L_SHIPDATE(t1)),
',',
	_f(NULL(t1, LINEITEM__L_COMMITDATE__String), LINEITEM__L_COMMITDATE(t1)),
',',
	_f(NULL(t1, LINEITEM__L_RECEIPTDATE__String), LINEITEM__L_RECEIPTDATE(t1)),
',',
	_f(NULL(t1, LINEITEM__L_SHIPINSTRUCT__String), LINEITEM__L_SHIPINSTRUCT(t1)),
',',
	_f(NULL(t1, LINEITEM__L_SHIPMODE__String), LINEITEM__L_SHIPMODE(t1)),
',',
	_f(NULL(t1, LINEITEM__L_COMMENT__String), LINEITEM__L_COMMENT(t1)),
)
print(
	_f(NULL(t2, LINEITEM__L_ORDERKEY__String), LINEITEM__L_ORDERKEY(t2)),
',',
	_f(NULL(t2, LINEITEM__L_PARTKEY__String), LINEITEM__L_PARTKEY(t2)),
',',
	_f(NULL(t2, LINEITEM__L_SUPPKEY__String), LINEITEM__L_SUPPKEY(t2)),
',',
	_f(NULL(t2, LINEITEM__L_LINENUMBER__String), LINEITEM__L_LINENUMBER(t2)),
',',
	_f(NULL(t2, LINEITEM__L_QUANTITY__String), LINEITEM__L_QUANTITY(t2)),
',',
	_f(NULL(t2, LINEITEM__L_EXTENDEDPRICE__String), LINEITEM__L_EXTENDEDPRICE(t2)),
',',
	_f(NULL(t2, LINEITEM__L_DISCOUNT__String), LINEITEM__L_DISCOUNT(t2)),
',',
	_f(NULL(t2, LINEITEM__L_TAX__String), LINEITEM__L_TAX(t2)),
',',
	_f(NULL(t2, LINEITEM__L_RETURNFLAG__String), LINEITEM__L_RETURNFLAG(t2)),
',',
	_f(NULL(t2, LINEITEM__L_LINESTATUS__String), LINEITEM__L_LINESTATUS(t2)),
',',
	_f(NULL(t2, LINEITEM__L_SHIPDATE__String), LINEITEM__L_SHIPDATE(t2)),
',',
	_f(NULL(t2, LINEITEM__L_COMMITDATE__String), LINEITEM__L_COMMITDATE(t2)),
',',
	_f(NULL(t2, LINEITEM__L_RECEIPTDATE__String), LINEITEM__L_RECEIPTDATE(t2)),
',',
	_f(NULL(t2, LINEITEM__L_SHIPINSTRUCT__String), LINEITEM__L_SHIPINSTRUCT(t2)),
',',
	_f(NULL(t2, LINEITEM__L_SHIPMODE__String), LINEITEM__L_SHIPMODE(t2)),
',',
	_f(NULL(t2, LINEITEM__L_COMMENT__String), LINEITEM__L_COMMENT(t2)),
)
print(
	_f(NULL(t3, LINEITEM__L_ORDERKEY__String), LINEITEM__L_ORDERKEY(t3)),
',',
	_f(NULL(t3, LINEITEM__L_PARTKEY__String), LINEITEM__L_PARTKEY(t3)),
',',
	_f(NULL(t3, LINEITEM__L_SUPPKEY__String), LINEITEM__L_SUPPKEY(t3)),
',',
	_f(NULL(t3, LINEITEM__L_LINENUMBER__String), LINEITEM__L_LINENUMBER(t3)),
',',
	_f(NULL(t3, LINEITEM__L_QUANTITY__String), LINEITEM__L_QUANTITY(t3)),
',',
	_f(NULL(t3, LINEITEM__L_EXTENDEDPRICE__String), LINEITEM__L_EXTENDEDPRICE(t3)),
',',
	_f(NULL(t3, LINEITEM__L_DISCOUNT__String), LINEITEM__L_DISCOUNT(t3)),
',',
	_f(NULL(t3, LINEITEM__L_TAX__String), LINEITEM__L_TAX(t3)),
',',
	_f(NULL(t3, LINEITEM__L_RETURNFLAG__String), LINEITEM__L_RETURNFLAG(t3)),
',',
	_f(NULL(t3, LINEITEM__L_LINESTATUS__String), LINEITEM__L_LINESTATUS(t3)),
',',
	_f(NULL(t3, LINEITEM__L_SHIPDATE__String), LINEITEM__L_SHIPDATE(t3)),
',',
	_f(NULL(t3, LINEITEM__L_COMMITDATE__String), LINEITEM__L_COMMITDATE(t3)),
',',
	_f(NULL(t3, LINEITEM__L_RECEIPTDATE__String), LINEITEM__L_RECEIPTDATE(t3)),
',',
	_f(NULL(t3, LINEITEM__L_SHIPINSTRUCT__String), LINEITEM__L_SHIPINSTRUCT(t3)),
',',
	_f(NULL(t3, LINEITEM__L_SHIPMODE__String), LINEITEM__L_SHIPMODE(t3)),
',',
	_f(NULL(t3, LINEITEM__L_COMMENT__String), LINEITEM__L_COMMENT(t3)),
)
print(
	_f(NULL(t4, LINEITEM__L_ORDERKEY__String), LINEITEM__L_ORDERKEY(t4)),
',',
	_f(NULL(t4, LINEITEM__L_PARTKEY__String), LINEITEM__L_PARTKEY(t4)),
',',
	_f(NULL(t4, LINEITEM__L_SUPPKEY__String), LINEITEM__L_SUPPKEY(t4)),
',',
	_f(NULL(t4, LINEITEM__L_LINENUMBER__String), LINEITEM__L_LINENUMBER(t4)),
',',
	_f(NULL(t4, LINEITEM__L_QUANTITY__String), LINEITEM__L_QUANTITY(t4)),
',',
	_f(NULL(t4, LINEITEM__L_EXTENDEDPRICE__String), LINEITEM__L_EXTENDEDPRICE(t4)),
',',
	_f(NULL(t4, LINEITEM__L_DISCOUNT__String), LINEITEM__L_DISCOUNT(t4)),
',',
	_f(NULL(t4, LINEITEM__L_TAX__String), LINEITEM__L_TAX(t4)),
',',
	_f(NULL(t4, LINEITEM__L_RETURNFLAG__String), LINEITEM__L_RETURNFLAG(t4)),
',',
	_f(NULL(t4, LINEITEM__L_LINESTATUS__String), LINEITEM__L_LINESTATUS(t4)),
',',
	_f(NULL(t4, LINEITEM__L_SHIPDATE__String), LINEITEM__L_SHIPDATE(t4)),
',',
	_f(NULL(t4, LINEITEM__L_COMMITDATE__String), LINEITEM__L_COMMITDATE(t4)),
',',
	_f(NULL(t4, LINEITEM__L_RECEIPTDATE__String), LINEITEM__L_RECEIPTDATE(t4)),
',',
	_f(NULL(t4, LINEITEM__L_SHIPINSTRUCT__String), LINEITEM__L_SHIPINSTRUCT(t4)),
',',
	_f(NULL(t4, LINEITEM__L_SHIPMODE__String), LINEITEM__L_SHIPMODE(t4)),
',',
	_f(NULL(t4, LINEITEM__L_COMMENT__String), LINEITEM__L_COMMENT(t4)),
)
print(
	_f(NULL(t5, LINEITEM__L_ORDERKEY__String), LINEITEM__L_ORDERKEY(t5)),
',',
	_f(NULL(t5, LINEITEM__L_PARTKEY__String), LINEITEM__L_PARTKEY(t5)),
',',
	_f(NULL(t5, LINEITEM__L_SUPPKEY__String), LINEITEM__L_SUPPKEY(t5)),
',',
	_f(NULL(t5, LINEITEM__L_LINENUMBER__String), LINEITEM__L_LINENUMBER(t5)),
',',
	_f(NULL(t5, LINEITEM__L_QUANTITY__String), LINEITEM__L_QUANTITY(t5)),
',',
	_f(NULL(t5, LINEITEM__L_EXTENDEDPRICE__String), LINEITEM__L_EXTENDEDPRICE(t5)),
',',
	_f(NULL(t5, LINEITEM__L_DISCOUNT__String), LINEITEM__L_DISCOUNT(t5)),
',',
	_f(NULL(t5, LINEITEM__L_TAX__String), LINEITEM__L_TAX(t5)),
',',
	_f(NULL(t5, LINEITEM__L_RETURNFLAG__String), LINEITEM__L_RETURNFLAG(t5)),
',',
	_f(NULL(t5, LINEITEM__L_LINESTATUS__String), LINEITEM__L_LINESTATUS(t5)),
',',
	_f(NULL(t5, LINEITEM__L_SHIPDATE__String), LINEITEM__L_SHIPDATE(t5)),
',',
	_f(NULL(t5, LINEITEM__L_COMMITDATE__String), LINEITEM__L_COMMITDATE(t5)),
',',
	_f(NULL(t5, LINEITEM__L_RECEIPTDATE__String), LINEITEM__L_RECEIPTDATE(t5)),
',',
	_f(NULL(t5, LINEITEM__L_SHIPINSTRUCT__String), LINEITEM__L_SHIPINSTRUCT(t5)),
',',
	_f(NULL(t5, LINEITEM__L_SHIPMODE__String), LINEITEM__L_SHIPMODE(t5)),
',',
	_f(NULL(t5, LINEITEM__L_COMMENT__String), LINEITEM__L_COMMENT(t5)),
)
print(
	_f(NULL(t6, NATION__N_NATIONKEY__String), NATION__N_NATIONKEY(t6)),
',',
	_f(NULL(t6, NATION__N_NAME__String), NATION__N_NAME(t6)),
',',
	_f(NULL(t6, NATION__N_REGIONKEY__String), NATION__N_REGIONKEY(t6)),
',',
	_f(NULL(t6, NATION__N_COMMENT__String), NATION__N_COMMENT(t6)),
)
print(
	_f(NULL(t7, NATION__N_NATIONKEY__String), NATION__N_NATIONKEY(t7)),
',',
	_f(NULL(t7, NATION__N_NAME__String), NATION__N_NAME(t7)),
',',
	_f(NULL(t7, NATION__N_REGIONKEY__String), NATION__N_REGIONKEY(t7)),
',',
	_f(NULL(t7, NATION__N_COMMENT__String), NATION__N_COMMENT(t7)),
)
print(
	_f(NULL(t8, NATION__N_NATIONKEY__String), NATION__N_NATIONKEY(t8)),
',',
	_f(NULL(t8, NATION__N_NAME__String), NATION__N_NAME(t8)),
',',
	_f(NULL(t8, NATION__N_REGIONKEY__String), NATION__N_REGIONKEY(t8)),
',',
	_f(NULL(t8, NATION__N_COMMENT__String), NATION__N_COMMENT(t8)),
)
print(
	_f(NULL(t9, NATION__N_NATIONKEY__String), NATION__N_NATIONKEY(t9)),
',',
	_f(NULL(t9, NATION__N_NAME__String), NATION__N_NAME(t9)),
',',
	_f(NULL(t9, NATION__N_REGIONKEY__String), NATION__N_REGIONKEY(t9)),
',',
	_f(NULL(t9, NATION__N_COMMENT__String), NATION__N_COMMENT(t9)),
)
print(
	_f(NULL(t10, NATION__N_NATIONKEY__String), NATION__N_NATIONKEY(t10)),
',',
	_f(NULL(t10, NATION__N_NAME__String), NATION__N_NAME(t10)),
',',
	_f(NULL(t10, NATION__N_REGIONKEY__String), NATION__N_REGIONKEY(t10)),
',',
	_f(NULL(t10, NATION__N_COMMENT__String), NATION__N_COMMENT(t10)),
)

print('--------sql1--------')
if model.eval(Not(DELETED(t18))):
	print(
	_f(NULL(t18, TABLE3__REVENUE__String), TABLE3__REVENUE(t18)),
	)
print('--------sql2--------')
if model.eval(Not(DELETED(t39))):
	print(
	_f(NULL(t39, TABLE6__REVENUE__String), TABLE6__REVENUE(t39)),
	)

