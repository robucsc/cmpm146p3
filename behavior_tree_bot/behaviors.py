import sys
import math

sys.path.insert(0, '../')
from planet_wars import issue_order

def distance_between(pointA, pointB):
    return math.sqrt(pow(pointA[0] - pointB[0], 2) + pow(pointA[1] - pointB[1], 2))

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def attack_closest_planets(state):
    if len(state.my_planets()) == 0:
        return False

    weakest_planet = min(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    weak_ships = weakest_planet.num_ships

    closest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    planet_dist = distance_between([weakest_planet.x, weakest_planet.y],[closest_planet.x, closest_planet.y])
    # planet_dist = temp_dist < planet_dist and planet.num_ships > (weak_ships + 3)

    for planet in state.my_planets():
        # temp_dist = distance_between([weakest_planet.x, weakest_planet.y], [planet.x,planet.y])
        temp_dist = state.distance(planet.ID, weakest_planet.ID)
        if temp_dist < planet_dist and planet.num_ships > (weak_ships + 3):
            closest_planet = planet
            planet_dist = temp_dist
    # if closest_planet:
    return issue_order(state, closest_planet.ID, weakest_planet.ID, weak_ships + 3)

def spread_and_attack_planets(state):  # performs as many spread and attacks as possible using all my planets as long as required ships is met
    my_planets = iter(
        sorted(state.my_planets(), key=lambda planet: planet.num_ships))  # sort my planets based on num of ships

    possible_planets = [planet for planet in state.not_my_planets()
                        if not any(fleet.destination_planet == planet.ID for fleet in
                                   state.my_fleets())]  # make a list of planets that I can spread into or attack
    possible_planets.sort(key=lambda
        planet: planet.num_ships)  # sort the possible planets for my planets to spread or attack in ascending order

    target_planets = iter(possible_planets)  # to start iteration of target planets from possible planets

    try:
        my_planet = next(my_planets)  # initiator of to get the items of my_planets
        target_planet = next(target_planets)  # initiator of to get the items of target_planets
        while True:
            required_ships = target_planet.num_ships + 1  # calculate the required ships to make the target_planet (assuming its neutral) into my-planet

            if target_planet in state.enemy_planets():
                required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID,
                                                target_planet.ID) * target_planet.growth_rate + 1  # calculate the required ships to make the target_planet (assuming its enemy) into my-planet

            # check to whether attack or move to my next planet
            if my_planet.num_ships > required_ships:  # check if my current planet has enough ships
                issue_order(state, my_planet.ID, target_planet.ID,
                                   required_ships)  # issue order if can make the target planet my planet
                my_planet = next(my_planets)  # get next item of my_planet list
                target_planet = next(target_planets)  # get next item of target_planet list
            else:
                my_planet = next(my_planets)  # get next item of my_planet list

    except StopIteration:  # ran out of my_planets or target_planets
        return False
