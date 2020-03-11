from main_order_handler import TodaysOrders

# после обработки alert от SS и загрузки данных в бд приходит вот такая информаця о новом заказе

today_orders = TodaysOrders()
new_order = {"refid": 23, "dishes": [(2, 4, 6, 7), (1, 2, 4, 5)]}

print("Заказы на начало работы", today_orders.current_dishes_proceed)
print("Печи доступные", today_orders.oven_avalable.keys())

today_orders.create_new_order(new_order)

print("Остались печи", today_orders.oven_avalable)

print(today_orders.oven_avalable)
