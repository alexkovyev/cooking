import asyncio

import start_PBM as Pbm


def go_to_db_get_data():
    monk_data = True
    return monk_data


def pause_cooking():
    Pbm.pause_cooking()


def main():
    """Какое то описание"""
    equipment_status = go_to_db_get_data()
    if True:
        test_result, equipment_data = Pbm.start_testing(equipment_status)
        if test_result:
            cooking = Pbm.start_cooking(equipment_data)
        else:
            raise ValueError("Оборудование неисправно, нельзя работать")
        return cooking
    else:
        return "DB connection error"


if __name__ == "__main__":
    main()