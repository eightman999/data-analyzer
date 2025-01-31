import math

from utils.coefficient.hit_point_inclination import dev_year_inclination


def default_hitpoints(manpower,hull_type,armor_value):
    res = 200 * (((hull_type / 1.8) + math.log(armor_value)) / 2)
    res = (res * manpower) / 1000
    return res

def year_to_tech_level(year,manpower,hull_type,armor_value):
    inclination = dev_year_inclination(year)
    hitpoints = default_hitpoints(manpower,hull_type,armor_value)*inclination
    return hitpoints

def default_hitpoint(weight,hull_type,armor_value,Number_of_persons):
    res = 200 * ((weight / 1000 + (hull_type*hull_type) + math.log(armor_value)) / 2)*Number_of_persons
    return res