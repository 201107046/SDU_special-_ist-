import io
from base64 import b64encode
import eel
import json
import pandas as pd
import re
from scipy.spatial import distance

eel.init('web') # in order to initialize eel component 
def intersection(cell_string, lst2): #to find simmilar properties between target and rows in dataset
    lst = re.split('[^а-я]', cell_string)
    lst1 = ' '.join(lst).split() 
    lst3 = list(set(lst1).intersection(lst2))
    return lst3 

def calculate_euclidian(vec_1_cuisine, cev_1_extra, vec_1_price, vec_2_cuisine, cev_2_extra, vec_2_price,): # finding euclidian distance
    dst = distance.euclidean([float(vec_1_cuisine),float(cev_1_extra),float(vec_1_price)], [float(vec_2_cuisine),float(cev_2_extra),float(vec_2_price)])
    return dst

def class_price(avg_price): # price segment
    if avg_price < 700:
        return 1
    elif avg_price < 1500:
        return 2
    elif avg_price < 2500:
        return 3
    elif avg_price < 5000:
        return 4
    elif avg_price < 10000:
        return 5
    else:
        return 6

def getDataFromBack(cusine,option,price): # to get back data by given criteria
    locations = pd.read_csv("restoran_data.csv", encoding = "utf-8")
    locations = locations.rename({'Cuisine type': 'Cuisine_type'}, axis=1)
    locations = locations.rename({'Working Hours': 'Working_Hours'}, axis=1)
    locations = locations.rename({'Average Price': 'Average_Price'}, axis=1)
    cuisine_target = [cusine]
    extra_target = [option]
    price_class = price 
    locations['cuisine_simmilarity'] = locations.apply(lambda row: len(intersection(row.Cuisine_type, cuisine_target))/len(cuisine_target), axis=1)
    locations['extra_simmilarity'] = locations.apply(lambda row: len(intersection(row.Extra, extra_target))/len(extra_target), axis=1)
    locations['common_cuisine_types'] = locations.apply(lambda row: len(intersection(row.Cuisine_type, cuisine_target)), axis=1)
    locations['common_extra_types'] = locations.apply(lambda row: len(intersection(row.Extra, extra_target)), axis=1)
    locations['price_class'] = locations.apply(lambda row: class_price(row.Average_Price), axis=1)
    locations['euclidian_distance'] = locations.apply(lambda row: calculate_euclidian(row.common_cuisine_types, row.common_extra_types,
                                                                                 row.price_class,
                                                                                 len(cuisine_target), len(extra_target),
                                                                                 class_price(price_class)), axis=1)
    filtered_table = locations.sort_values(by='euclidian_distance', ascending=True)
    return filtered_table.head(5) # return top five recommendation


@eel.expose
def dummy(dummy_param): # function for check of eel 
    print("I got a parameter: ", dummy_param)
    return "string_value", 1, 1.2, True, [1, 2, 3, 4], {"name": "eel"}

@eel.expose # initialize function in eel, that will be available to call from JS 
def getDataFromPy(param1,param2,param3): #main function on back, with return result as json
    print("I got a parameter: ", param1 + param2 + param3)
    asd=getDataFromBack(param1,param2,int(param3)).to_json(orient='records') # call function getDataFromBack(), and convert result tp JSON
    #print(asd)
    return asd

eel.start('index.html', size=(1000, 600)) # seting of html window 
