import pykakasi
import math

def convert_name(kanji,tag,type):

    kakasi = pykakasi.kakasi()
    hepburn_list = kakasi.convert(kanji)
    hepburn = ''.join([item['hepburn'] for item in hepburn_list])
    result = "USH_"+ tag +"_"+type+"_"+ nakaten_delete(hepburn)
    result = classer(result)
    return result

def nakaten_delete(input):
    result = input.replace("・", "_")
    return result

def classer(input):
    result = input.replace("kyuu", "_class")
    result = result.replace("kyu", "_class")
    result = result.replace("gata", "_class")
    result = result.replace("gou", "go_class")
    result = result.replace("go", "go_class")
    result = result.replace("kata", "_class")
    return result

def max_cruise_speed_converter(max_speed,cruise_speed):
    if max_speed == cruise_speed:
        return max_speed
    else:
        result = (max_speed + cruise_speed) / 2
        return result

def naval_range_converter(ship_type,naval_range,naval_range_min):
    result = 0
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

def hit_and_org_points_converter(weight, hull_type, Length, Width, dev_year, armor_thickness, armor_type, Number_of_persons):
    hit_ratio = (Length + Width) / 20 * weight / 1000
    standard_debuff = -19.85 * (10002 / (weight + 100000))
    armor_value = armor_thickness * (armor_type / 2) / 20 + 0.1
    if armor_value <= 0:
        armor_value = 1 # Set a small positive value to avoid math domain error
    default_hitpoint = 200 * (((hull_type / 1.8) + math.log(armor_value)) / 2)
    if dev_year < 1900:
        hitpoint = default_hitpoint * 0.8
    elif dev_year < 1920:
        hitpoint = default_hitpoint * 0.9
    elif dev_year < 1940:
        hitpoint = default_hitpoint * 1.0
    elif dev_year < 1960:
        hitpoint = default_hitpoint * 1.1
    elif dev_year < 1980:
        hitpoint = default_hitpoint * 1.2
    else:
        hitpoint = default_hitpoint * 1.3
    hitpoint = standard_debuff + hitpoint - hit_ratio + 250 + Number_of_persons/10 + weight/10
    result = math.floor(hitpoint * 100) / 100
    return result

def org_point_converter(weight, hull_type, Length, Width, dev_year, armor_thickness, armor_type, Number_of_persons):
    armor_value = armor_thickness * (armor_type / 2) / 20
    if armor_value <= 0:
        armor_value = 1  # Set a small positive value to avoid math domain error
    default_hitpoint = 200 * ((weight / 1000 + (hull_type*hull_type) + math.log(armor_value)) / 2)
    orgpoint = (default_hitpoint * Number_of_persons) /weight/weight*5000
    result = math.floor(orgpoint * 100)/100
    return result
def ship_cost_generator(weight, dev_year, armor_thickness, armor_type, hull_type,ship_type):
    result = 0
    if ship_type == "IC":
        standard_weight = 10000
    elif ship_type == "B":
        standard_weight = 10000
    elif ship_type == "BC":
        standard_weight = 30000
    elif ship_type == "BB":
        standard_weight = 35000
    elif ship_type == "AC":
        standard_weight = 4000
    elif ship_type == "CS":
        standard_weight = 3000
    elif ship_type == "CL":
        standard_weight = 7250
    elif ship_type == "CA":
        standard_weight = 8800
    elif ship_type == "C":
        standard_weight = 2500
    elif ship_type == "DD":
        standard_weight = 1500
    elif ship_type == "D":
        standard_weight = 800
    elif ship_type == "ACR":
        standard_weight = 9000
    else:
        standard_weight = 8800

    if dev_year < 1900:
        standard_weight = standard_weight * 0.8
    elif dev_year < 1910:
        standard_weight = standard_weight * 0.9
    elif dev_year < 1920:
        standard_weight = standard_weight * 1.0
    elif dev_year < 1930:
        standard_weight = standard_weight * 1.1
    else:
        standard_weight = standard_weight * 1.2
    weapon_weight = weight/0.01
    standard_weight = (weight - standard_weight-weapon_weight) * 0.5 + standard_weight
    standard_cost = standard_weight * 0.02/hull_type
    # standard_year = dev_year-1500
    armor_value = armor_thickness * armor_type
    if armor_value <= 0:
        armor_value = 1 # Set a small positive value to avoid math domain error
    armor_value = math.log(armor_value)
    if dev_year < 1900:
        result = weight*(weight-100) * 0.7 * armor_value * (hull_type*hull_type)
    elif dev_year < 1920:
        result = weight*(weight-100) * 0.75 * armor_value * (hull_type*hull_type)
    elif dev_year < 1940:
        result = weight*(weight-100) * 0.8 * armor_value * (hull_type*hull_type)
    elif dev_year < 1960:
        result = weight*(weight-100) * 0.85 * armor_value * (hull_type*hull_type)
    elif dev_year < 1980:
        result = weight*(weight-100) * 0.9 * armor_value * (hull_type*hull_type)
    else:
        result = weight*(weight-100) * 1.0 * armor_value * (hull_type*hull_type)
    result = result * 0.000005
    result = (result - standard_cost) * 0.3 + standard_cost
    result = result/ 8
    if result <= 0:
        result = result * -1
    result = math.floor(result * 100) / 100
    return result

def surface_visibility_converter(Length,Width,dev_year,fuel_type,ship_type):
    result = 0
    if ship_type == "IC":
        standard_visibility = 10000
    elif ship_type == "B":
        standard_visibility = 12000
    elif ship_type == "BC":
        standard_visibility = 30000
    elif ship_type == "BB":
        standard_visibility = 35000
    elif ship_type == "AC":
        standard_visibility = 4000
    elif ship_type == "CS":
        standard_visibility = 3000
    elif ship_type == "CL":
        standard_visibility = 7250
    elif ship_type == "CA":
        standard_visibility = 8800
    elif ship_type == "C":
        standard_visibility = 2500
    elif ship_type == "DD":
        standard_visibility = 1500
    elif ship_type == "D":
        standard_visibility = 1000
    elif ship_type == "ACR":
        standard_visibility = 9000
    else:
        standard_visibility = 8800
    standard_visibility = standard_visibility * 0.01

    if dev_year < 1900:
        result = (Length + Width)*(Length + Width) * 0.8 * fuel_type
    elif dev_year < 1920:
        result = (Length + Width)*(Length + Width) * 0.825 * fuel_type
    elif dev_year < 1940:
        result = (Length + Width)*(Length + Width) * 0.85 * fuel_type
    elif dev_year < 1960:
        result = (Length + Width)*(Length + Width) * 0.875 * fuel_type
    elif dev_year < 1980:
        result = (Length + Width)*(Length + Width) * 0.9 * fuel_type
    else:
        result = (Length + Width)*(Length + Width) * 1.0 * fuel_type
    result = result * 0.000005 * standard_visibility
    result = math.floor(result * 100) / 100
    return result
