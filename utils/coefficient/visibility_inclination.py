def visibility_coefficient(ship_type):
    if ship_type == "IC":
        standard_visibility = 1500
    elif ship_type == "B":
        standard_visibility = 8000
    elif ship_type == "BC":
        standard_visibility = 8500
    elif ship_type == "BB":
        standard_visibility = 9000
    elif ship_type == "AC":
        standard_visibility = 1800
    elif ship_type == "CS":
        standard_visibility = 3500
    elif ship_type == "CL":
        standard_visibility = 6000
    elif ship_type == "CA":
        standard_visibility = 7200
    elif ship_type == "C":
        standard_visibility = 3000
    elif ship_type == "DD":
        standard_visibility = 2750
    elif ship_type == "D":
        standard_visibility = 2500
    elif ship_type == "ACR":
        standard_visibility = 7500
    elif ship_type == "DDE":
        standard_visibility = 2750
    elif ship_type == "DDG":
        standard_visibility = 3200
    elif ship_type == "DDH":
        standard_visibility = 4200
    elif ship_type == "CV":
        standard_visibility = 8000
    else:
        standard_visibility = 8800
    return standard_visibility * 0.01

def fuel_dev_year_inclination(dev_year):
    dev_year = round(dev_year, -1)
    inclinations = {
        1800:0.5,
        1810:0.525,
        1820:0.55,
        1830:0.575,
        1840:0.6,
        1850:0.625,
        1860:0.65,
        1870:0.675,
        1880:0.7,
        1890:0.725,
        1900:0.75,
        1910:0.775,
        1920:0.8,
        1930:0.825,
        1940:0.85,
        1950:0.875,
        1960:0.9,
        1970:0.925,
        1980:0.95,
        1990:0.975,
        2000:1.0,
        2010:1.025,
        2020:1.05,
        2030:1.075,
        2040:1.1,
        2050:1.125,
        2060:1.15,
        2070:1.175,
        2080:1.2,
    }
    res = 1/inclinations[dev_year]
    return res

def extents(extent,dev_year):
    res = 1
    res = extent**2*fuel_dev_year_inclination(dev_year)
    return res