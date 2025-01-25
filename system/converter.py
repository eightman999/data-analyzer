from datetime import datetime
import math

from tools.calc import significant_figures
from tools.line_tools import L2, L3, L1, LE, L4

from system.coefficient.cost_inclination import ship_type_coefficient
from system.coefficient.hit_point_inclination import armor_inclination, standard_inclination
from system.coefficient.visibility_inclination import visibility_coefficient, extents
from system.tools.HP_tools import year_to_tech_level, default_hitpoint

global locked
global unlockable
default_modules = []

def hit_and_org_points_converter(weight, hull_type, Length, Width, dev_year, armor_thickness, armor_type, Number_of_persons):
    hit_ratio = (Length + Width) / 20 * weight / 1000
    armor_value = armor_inclination(armor_thickness, armor_type)
    result = standard_inclination(weight) + year_to_tech_level(dev_year, Number_of_persons, hull_type, armor_value) - hit_ratio + 250 + Number_of_persons/10 + weight/10
    result = significant_figures(result, 2)
    return result

def org_point_converter(weight, hull_type, Length, Width, dev_year, armor_thickness, armor_type, Number_of_persons):
    armor_value = armor_inclination(armor_thickness, armor_type)
    result = default_hitpoint(weight, hull_type, armor_value, Number_of_persons)
    result = result
    result = significant_figures(result, 2)
    return result

def ship_cost_generator(weight, dev_year):
    result = weight * (dev_year-1800)/500
    result = significant_figures(result, 2)
    return result

def surface_visibility_converter(Length,Width,dev_year,fuel_type,ship_type):

    standard_visibility = visibility_coefficient(ship_type)
    result = extents(Length*Width,dev_year) * fuel_type
    result = result * 0.00000005 * standard_visibility
    result = significant_figures(result, 2)
    return result

def slot_maker(SLTOTYPE, SLOTNAME):
    result = ""
    if SLOTNAME == "":
        SLOTNAME = "UNDEFINED"
    global locked
    global unlockable
    if SLTOTYPE.isdecimal():
        result = result + L2  +  SLOTNAME + " = {" + LE
        result = result + L3 + "required = no" + LE
        result = result + L3 + "allowed_module_categories = {" + LE
        result = result + L3 + L1 + "SM_HNG_" + SLTOTYPE  +  LE
        result = result + L3 + "}" + LE
        result = result + L2 + "}" + LE
        default_modules.append(SLOTNAME + " = SM_HNG_" + SLTOTYPE)
    elif SLTOTYPE == "=":
        unlockable += 1
        result = result + L2 + "unlockable_slot_" + str(unlockable) + " = {" + LE
        result = result + L3 + "required = yes" + LE
        result = result + L3 + "allowed_module_categories = {" + LE
        result = result + L3 + L1 + "Releasable_locking_modules" + LE
        result = result + L3 + "}" + LE
        result = result + L2 + "}" + LE
        default_modules.append(L3 + "unlockable_slot_" + str(unlockable) + " = Releasable_locking_module" + LE)
    elif SLTOTYPE == "-":
        locked += 1
        result = result + L2 + "locked_slot_" + str(locked) + " = {" + LE
        result = result + L3 + "required = yes" + LE
        result = result + L3 + "allowed_module_categories = {" + LE
        result = result + L3 + L1 + "Non_releasable_locking_modules" + LE
        result = result + L3 + "}" + LE
        result = result + L2 + "}" + LE
        default_modules.append(L3 + "locked_slot_" + str(locked) + " = Non_releasable_locking_module" + LE)
    else:
        result = result + L2  +  SLOTNAME + " = {" + LE
        result = result + L3 + "required = no" + LE
        result = result + L3 + "allowed_module_categories = {" + LE
        result = result + L4 + SLTOTYPE  +  LE
        result = result + L3 + "}" + LE
        result = result + L2 + "}" + LE
        default_modules.append(L3  +  SLOTNAME + " = empty" + LE)

    return result

def add_archetype(archetype):
    result = ""
    return result

def To_Code(ID,YEAR,archetype,TYPE,PA,SA,PSA,SSA,PLA,SLA,ALLW_TYPE,HP,ORG,COST,VISIVLE,manpower):
    global locked
    global unlockable
    locked = 0
    unlockable = 0
    default_modules.clear()
    # HULL FIXED TEXT
    result = L1  +  ID + " = {" + LE
    result = result + L1 + "year = " + YEAR  +  LE
    result = result + L1 + "archetype = ship_hull_" + archetype  +  LE
    result = result + L1 + "module_slots = {" + LE
    # TYPE
    result = result + L2 + "ship_type_slot = {" + LE
    result = result + L3 + "required = yes" + LE
    result = result + L3 + "allowed_module_categories = {" + LE
    result = result + L4+ALLW_TYPE+"" + LE
    result = result + L3 + "}" + LE
    result = result + L2 + "}" + LE
    # SLOT DEFINITION
    # PRIMARY ARMAMENT
    result = result + slot_maker(PA,"primary_armament_slot")
    # SECONDARY ARMAMENT
    result = result + slot_maker(SA,"secondary_armament_slot")
    # PRIMARY SUB ARMAMENT
    result = result + slot_maker(PSA,"primary_sub_armament_slot")
    # SECONDARY SUB ARMAMENT
    result = result + slot_maker(SSA,"secondary_sub_armament_slot")
    # PRIMARY LIGHT ARMAMENT
    result = result + slot_maker(PLA,"primary_light_armament_slot")
    # SECONDARY LIGHT ARMAMENT
    result = result + slot_maker(SLA,"secondary_light_armament_slot")

    result = result + L1 + "}" + LE
    # DEFAULT MODULES
    result = result + L2 + "default_modules = {" + LE
    result = result + L3 + "ship_type_slot = SRM_" + TYPE  +  LE
    for module in default_modules:
        result = result +L4+ module  +  LE
    result = result + L2 + "}" + LE
    result = result + L2 + "max_organisation = " + str(ORG)  +  LE
    result = result + L2 + "max_strength = " + str(HP)  +  LE
    result = result + L2 + "build_cost_ic = " + str(COST)  +  LE
    result = result + L2 + "surface_visibility = " + str(VISIVLE)  +  LE
    result = result + L2 + "resources = {" + LE
    result = result + L3 + "steel = "+str(significant_figures(math.log2(COST), 0))+"" + LE
    result = result + L2 + "}" + LE
    result = result + L2 + "manpower = " + manpower  +  LE
    result = result + L1 + "}" + LE



    return result