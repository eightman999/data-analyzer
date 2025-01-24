
def ship_type_coefficient(ship_type):
    if ship_type == "IC":
        standard_weight = 8500
        STD_PC = 0.6
    elif ship_type == "B":
        standard_weight = 9000
        STD_PC = 0.6
    elif ship_type == "BC":
        standard_weight = 9800
        STD_PC = 0.85
    elif ship_type == "BB":
        standard_weight = 10000
        STD_PC = 0.7
    elif ship_type == "AC":
        standard_weight = 4000
        STD_PC = 1
    elif ship_type == "CS":
        standard_weight = 3000
        STD_PC = 1
    elif ship_type == "CL":
        standard_weight = 7250
        STD_PC = 2.5
    elif ship_type == "CA":
        standard_weight = 8800
        STD_PC = 0.85
    elif ship_type == "C":
        standard_weight = 2500
        STD_PC = 1.85
    elif ship_type == "DDE":
        standard_weight = 2000
        STD_PC = 18.5
    elif ship_type == "DDG":
        standard_weight = 3200
        STD_PC = 1.2
    elif ship_type == "DDH":
        standard_weight = 4200
        STD_PC = 1.5
    elif ship_type == "CV":
        standard_weight = 10000
        STD_PC = 0.75
    elif ship_type == "DD":
        standard_weight = 2000
        STD_PC = 0.75
    elif ship_type == "D":
        standard_weight = 1200
        STD_PC = 0.85
    elif ship_type == "ACR":
        standard_weight = 9000
        STD_PC = 0.9
    else:
        standard_weight = 8800
        STD_PC = 0.85
    return standard_weight,STD_PC