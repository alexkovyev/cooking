import start_PBM as Pbm
from utils import start_testing


def pause_cooking():
    """Для остановки системы необходимо запустить эту функцию SSC"""
    Pbm.pause_cooking()


def main():
    """это наброски ssc"""
    # какая то нужна информация контроллерам, если не нужно, удаляем

    test_result, equipment_data = start_testing()
    if test_result:
        cooking = Pbm.start(equipment_data)
    else:
        raise ValueError("Оборудование неисправно, нельзя работать")


if __name__ == "__main__":
    main()
