class PbmFatalError(Exception):
    def __init__(self):
        self.text = "Возникла критическая ошибка PBM"

class DataBaseError:
    def __init__(self):
        self.text = "Ошибка доступа к БД PBM"