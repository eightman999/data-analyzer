import pykakasi


def nakaten_delete(input):
    result = input.replace("・", "_")
    return result

def convert_name(kanji,tag,type):

    kakasi = pykakasi.kakasi()
    hepburn_list = kakasi.convert(kanji)
    hepburn = ''.join([item['hepburn'] for item in hepburn_list])
    result = "USH_"+ tag +"_"+type+"_"+ nakaten_delete(hepburn)
    result = classer(result)
    return result

def classer(input):
    result = input.replace("kyuu", "_class")
    result = result.replace("kyu", "_class")
    result = result.replace("gata", "_class")
    result = result.replace("gou", "go_class")
    result = result.replace("go", "go_class")
    result = result.replace("kata", "_class")
    return result