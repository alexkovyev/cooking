import start_PBM as Pbm
from utils import start_testing, parse_recipes


def pause_cooking():
    """Для остановки системы необходимо запустить эту функцию SSC"""
    Pbm.pause_cooking()


def main():
    """это наброски ssc"""
    # какая то нужна информация контроллерам, если не нужно, удаляем

    test_result, equipment_data = start_testing()
    recipes = parse_recipes()
    if test_result and recipes:
        cooking = Pbm.start(equipment_data, recipes)
    else:
        raise ValueError("Оборудование неисправно, нельзя работать")


if __name__ == "__main__":
    main()
