crawler 文档说明
====
文件夹说明:
1. frame: 主体程序架构，包括配置文件，调度，数据库配置，任务父类。
    1. 启动程序: main.py
    2. 配置文件: config.py/config_default.py/config_override.py
    3. 调度程序: schedule.py
    4. 数据库配置: database.py
    5. 任务父类: taskbase.py

2. library: 具体任务所需的库函数，接口等。
    1. okcoin库: http_md5_util.py/okcoin_spot_api.py
    2. huobi库: huobi_util.py/huobi_api.py/huobi_service.py

3. task: 具体采集任务。
    1. 采集网站:okcoin.cn/okcoin.com/huobi.com
    2. 采集币种: btc_cny/btc_usd/ltc_cny/ltc_usd(huobi.com暂无)
    3. 采集内容: ticker/depth/kline_1min/trades(okcoin)/detail(huobi)
----
个别文件详细:
1. config.py: 把config_default.py和config_override.py的配置内容进行拼接，得到一个dict()的内容，其中任务(task)必须为拼接后的task文件夹相同的模块名。
2. database.py: 设计只能使用mongodb数据库。
----
运行方式：
1. 编写配置文件。包括采集数据网站，内容、数据库信息等。
2. 主程序调用Schedule类，其中调用Config类读取配置文件，使用线程池分发各项采集任务。
3. 调用各项具体的采集任务，任务中包括采集数据，处理数据，存入数据库。返回采集状态(是否继续此任务，间隔时间等)
4. schedule类，根据各项任务返回值进行再次添加新任务。
----
TODO：
1. config中的db设置，若配置文件中没有设置db。则schedule中的db应该为None
2. 修改config中task的表达形式，直接改成’okcoincn_rest_btc_ticker’ 的string字段。简化task任务添加。
3. 重写taskbase类，不够简洁和完善。
4. 添加log监控。
5. 添加程序部署指令。控制程序、守护程序等。