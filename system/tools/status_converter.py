def max_cruise_speed_converter(max_speed,cruise_speed):
    if max_speed == cruise_speed:
        return max_speed
    else:
        result = (max_speed + cruise_speed) / 2
        return result

def naval_range_converter(ship_type,naval_range,naval_range_min):
    if ship_type == "submarine":
        result = (naval_range+naval_range_min) * 0.25
    else:
        result = naval_range * 0.5
    return result

def fuel_consumption_maker(fuel_amount,fuel_type):
    fuel_consumption_ratio = 0
    fuel_consumption = 0
    fuel_amount_k = fuel_amount / 1000
    if fuel_type == "coal_steam_reciprocating":
        fuel_consumption_ratio = 1.8
    elif fuel_type == "coal_steam_turbine":
        fuel_consumption_ratio = 1.6
    elif fuel_type == "oil_steam_reciprocating":
        fuel_consumption_ratio = 1.5
    elif fuel_type == "oil_steam_turbine":
        fuel_consumption_ratio = 1.3
    elif fuel_type == "diesel":
        fuel_consumption_ratio = 0.8
    elif fuel_type == "nuclear":
        fuel_consumption_ratio = 0.1
    fuel_consumption = fuel_amount_k * fuel_consumption_ratio
    return fuel_consumption

def armor_thickness_converter(max_armor_thickness,min_armor_thickness,armor_type):
    result = 0
    Converted_armor_type = 0
    if max_armor_thickness == 0:
        return result
    if min_armor_thickness == 0:
        min_armor_thickness = 1
    avg_armor_thickness = (max_armor_thickness * 1.2 + min_armor_thickness * 0.8) / 2
    if armor_type == "cupper_nickel":
        result = avg_armor_thickness * 0.2
        Converted_armor_type = 0.2
    elif armor_type == "wooden":
        result = avg_armor_thickness * 0.1
        Converted_armor_type = 0.1
    elif armor_type == "HV_armor_steel":
        result = avg_armor_thickness * 0.6
        Converted_armor_type = 0.6
    elif armor_type == "KC_armor_steel":
        result = avg_armor_thickness * 0.8
        Converted_armor_type = 0.8
    elif armor_type == "VC_armor_steel":
        result = avg_armor_thickness * 1.0
        Converted_armor_type = 1.0
    elif armor_type == "VH_armor_steel":
        result = avg_armor_thickness * 1.05
        Converted_armor_type = 1.05
    elif armor_type == "CNC_armor_steel":
        result = avg_armor_thickness * 1.1
        Converted_armor_type = 1.1
    elif armor_type == "NC_armor_steel":
        result = avg_armor_thickness * 1.15
        Converted_armor_type = 1.15
    elif armor_type == "DU_armor":
        result = avg_armor_thickness * 2
        Converted_armor_type = 2
    return result,Converted_armor_type
