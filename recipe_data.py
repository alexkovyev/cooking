"""Тут расположены псевдоданные рецепта """

# dough chain_id: plan_time
dough = {1: 10,
         2: 5,
         3: 10,
         4: 10,
         5: 12,
         6: 7,
         7: 2,
         }

# sauce chain_id: plan_time (const)
sauce = {1: 20}

# filling -> {filling_id: {filling}
#                         dough_id_2:{filling}
#                         }

#heating_program \ cooking_program -> {dough_id :(heating_program_id : duration)}
filling = {1: {"chain": {},
               "cooking_program": {1: (1, 180), 2: (2, 180), 3: (1, 180), 4: (1, 180)},
               "heating_program": {1: (1, 20), 2: (2, 20), 3: (1, 25), 4: (1, 37)},
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