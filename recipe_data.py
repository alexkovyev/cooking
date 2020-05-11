"""Тут расположены псевдоданные рецепта """

# рецепт для оценки времени и определения состава

dough_recipe_time = {
    # move_to_oven
    1: 20,
    # set_position_by_oven
    2: 2,
    # get_vane
    3: 7,
    # get_out_the_oven
    4: 10,
    # move_to_dough_station
    5: 12,
    # controllers_get_dough
    6: 7,
    # control_dough_position
    7: 2,
    # move_to_cut_station
    8: 15,
    # set_position_by_cut_station
    9: 2,
    # get_into_cut_station
    10: 2,
    # free_capture
    11: 1,
}

# dough chain_id: plan_time
dough = {1: 20,
         2: 2,
         3: 7,
         4: 10,
         5: 12,
         6: 7,
         7: 2,
         8: 15,
         9: 2,
         10: 2,
         11: 1,
         }

# sauce chain_id: plan_time (const)
sauce = {1: 20}

# filling filling_id: {dough_id_1:{}
#                      dough_id_2:{}             }
filling = {1: {"chain": {},
              "cooking_prorgamm": {1: 1, 2: 1, 3: 1, 4: 2}
              }
          }

filling_chain = []

# additive chain_id: plan_time
additive = {1: 5}

recipe_data = {
    "dough": dough,
    "sauce": sauce,
    "filling": filling,
    "additive": additive
}