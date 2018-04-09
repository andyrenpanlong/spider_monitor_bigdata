# spider_monitor_bigdata 顺丰爬虫监控及大数据可视化操作平台

## 主要负责顺丰大数据平台数据展示，及监控等平台于一体的web可视化操作平台

*注意事项：
    1. 首次启动：
        a. 可能出现错误:OperationalError: no such table: django_session
        解决办法：先执行： python manage.py migrate，在执行：python manage.py makemigrations
    2. 启动方式： （0.0.0.0 允许所有网站访问， 9000 表示端口号） 
        python manage.py runserver 0.0.0.0:9000
    3. 


