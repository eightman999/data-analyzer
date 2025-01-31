# 装甲化率
def armor_inclination(armor_thickness,armor_type):
    armor_value = armor_thickness * (armor_type / 2) / 20 + 0.1
    if armor_value <= 0:
        armor_value = 1
    return armor_value

#年代係数
def dev_year_inclination(dev_year):
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
    return inclinations[dev_year]

def standard_inclination(weight):
    return -19.85 * (10002 / (weight + 100000))