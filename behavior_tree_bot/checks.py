

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_enemy_planet_available(state): # returns True or False depending on whether there is any enemy planet available
    return any(state.enemy_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
