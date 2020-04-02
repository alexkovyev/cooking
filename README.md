# cooking
Draft for Cooking Module

Текущее решение: 
1. в ssc.py импортируется PMB, после подключения к  БД и получения данных запускается метод Pbm.start_testing(equipment_status)
Это метод контроллеров, запускаемый через PBM 
После успешного тестирования запускается метод Pbm.start_cooking(equipment_data)
Для приостановки готовки (затрагивается только корутина cooking, ss и controllers остаются работать (в текущей версии)) вызывается метод pause_cooking() (меняет значение флага на True) и start_cooking_after_pause (запускает cooking) 

2. файл start_PBM.py start_cooking(equipment_data) создает экземлпяр класса TodayOrders, из equipment_data при Init создаются объекты класса Equipment, при успешном запускаются асинхронно 3 корутины: ss_server, controllers_alert_handler, cooking. 

сам ss_server не написан, предполагается то при разборе post запроса выдается занение today_orders.time_to_cook_all_dishes_left или асинхронно запускается создание нового бюда (пока написано синхронно). 
