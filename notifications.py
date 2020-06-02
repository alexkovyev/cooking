class Notifications(object):
    """Этот класс заправляет уведомлениями, отправляемыми из PBM

    self.half_staff_availability_notifications_send = {
    "min_limit":{half_staff_id: time_send},
    "out_of_stock":{half_staff_id: time_send}
    }
    Или если удобнее будет сделать словарь {half_staff_id: notification_type}
    """

    def __init__(self):
        self.half_staff_availability_notifications_send = {}
        self.half_staff_expiration_date_notifications = {}

        self.need_to_be_send = {}

    async def check_is_there_need_to_send(self):
        """Проверяет нужно ли отправлять уведолмение. Можно посмотреть по первчноу ключу тип события
        и потом по ключу найти есть ли пф. Если нет, нужно отправлять

        Или если второй вариант, то ищем п\ф по ключу, сравниваем указаное событие, и если нет
        или не совпадает, то отправляем"""
        pass

    # возможно нужно промежуточный метод для создания уведомления

    async def add_to_send_list(self):
        """метод добавяет в словарь self.need_to_be_send = {}"""
        pass

    async def send_message(self):
        """метод отправляет сообщения из списка """
        pass

    async def list_upddate(self):
        """метод записывает, что уведомление отпарвлено, то есть помещает в списки
                self.half_staff_availability_notifications_send
                self.half_staff_expiration_date_notifications"""
        pass