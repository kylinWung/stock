#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import time
import datetime
import concurrent.futures

# 在项目运行时，临时将项目路径添加到环境变量
cpath = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath)
logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(cpath, 'logs', 'stock_execute_job.log'))
logging.getLogger().setLevel(logging.DEBUG)

import init_job as bj
import basic_data_daily_job as hdj
import indicators_data_daily_job as gdj
import strategy_data_daily_job as sdj
import backtest_data_daily_job as bdj

__author__ = 'myh '
__date__ = '2023/3/10 '


def main():
    start = time.time()
    _start = datetime.datetime.now()
    logging.info("######## 任务执行时间: %s #######" % _start.strftime("%Y-%m-%d %H:%M:%S.%f"))
    # 第1步创建数据库
    bj.main()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 第2步创建股票基础数据表
        executor.submit(hdj.main)
        # # 第3步创建股票指标数据表
        executor.submit(gdj.main)
        # # # # 第4步创建股票策略数据表
        executor.submit(sdj.main)

    # # # # 第5步创建股票回测
    bdj.main()

    logging.info("######## 完成任务, 使用时间: %s 秒 #######" % (time.time() - start))


# main函数入口
if __name__ == '__main__':
    main()