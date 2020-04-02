from PBM_main import TodaysOrders
from settings import QT_DISH_PER_ORDER


# создаем экземпляр класса TodaysOrders для работы на день в момент включения
today_orders = TodaysOrders()

# после обработки alert от SS и загрузки данных в бд приходит вот такая информаця о новом заказе
new_order = {"refid": 23, "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}

print("Заказы на начало работы", today_orders.current_dishes_proceed)
print("Печи доступные", today_orders.oven_available.keys())

today_orders.create_new_order(new_order, QT_DISH_PER_ORDER)

print("Остались печи", today_orders.oven_available)

print("Так выглядит заказ", today_orders.current_orders_proceed)

print("Это список блюд в TO", today_orders.current_dishes_proceed.keys())






