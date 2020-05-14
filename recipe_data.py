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