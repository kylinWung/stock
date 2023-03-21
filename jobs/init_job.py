#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import logging
import pymysql
import libs.database as mdb

__author__ = 'myh '
__date__ = '2023/3/10 '


# 创建新数据库。
def create_new_database():
    _MYSQL_CONN_DBAPI = mdb.MYSQL_CONN_DBAPI.copy()
    _MYSQL_CONN_DBAPI['database'] = "mysql"
    with pymysql.connect(**_MYSQL_CONN_DBAPI) as db:
        try:
            create_sql = " CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci " % mdb.db_database
            db.cursor().execute(create_sql)
        except Exception as e:
            logging.debug("{}处理异常：{}".format('init_job.create_new_database', e))


def main():
    # 检查，如果执行 select 1 失败，说明数据库不存在，然后创建一个新的数据库。
    try:
        with pymysql.connect(**mdb.MYSQL_CONN_DBAPI) as db:
            db.cursor().execute(" select 1 ")
    except Exception as e:
        logging.info("{}执行信息：{}".format('数据库不存在，将创建。', e))
        # 检查数据库失败，
        create_new_database()
    # 执行数据初始化。


# main函数入口
if __name__ == '__main__':
    main()
