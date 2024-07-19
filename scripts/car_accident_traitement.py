################################# import ###################################

import pandas as pd
import pickle
import opendatasets as od



################################# functions ################################

"""
Brief  : retrieving the csv dataframe
var    : name : name of the dataframe we want to extract
return : return the dataframe as a pandas one
"""
# od.download(
#     'https://www.kaggle.com/datasets/devansodariya/road-accident-united-kingdom-uk-dataset')

def get_data():
    csv_path = "UK_Accident.csv"
    df = pd.read_csv(csv_path)
    return df



"""
Brief  : removing column that we won't use because irrelevant to our key question
var    : df : pandas dataframe we want to sort
return : return the pandas sorted dataframe
"""
def sorting_dataset(df):
    df = df.drop('Accident_Index', axis=1)
    df = df.drop('Police_Force', axis=1)
    df = df.drop('Local_Authority_(District)', axis=1)
    df = df.drop('Local_Authority_(Highway)', axis=1)
    df = df.drop('2nd_Road_Number', axis=1)
    df = df.drop('Did_Police_Officer_Attend_Scene_of_Accident', axis=1)
    df = df.drop('LSOA_of_Accident_Location', axis=1)
    return df



"""
Brief  : changing qualitative attributs to numerical one
var    : column_name : name of the column we want to change
         dataframe : pandas dataframe on which we are working
return : dataframe : pandas dataframe actualised
         values_and_keys : dictionnary with the column name as key and a list in attribut containing the map of the numerical values
"""
def qualititative_to_numerical(column_name, dataframe):
    values = list(set(dataframe[column_name].values))
    values_remplaced = [i for i in range(len(values))]
    dataframe[column_name].replace(values,values_remplaced, inplace=True)
    values_and_keys = {}
    for i in range(len(values)):
        values_and_keys[values[i]] = i
    return dataframe, values_and_keys



"""
Brief  : retrieving all the column which have qualitative values
var    : dataframe : pandas dataframe on which we want to work
return : return a list of all the column we need to change
"""
def get_object_column(dataframe):
    list_to_remplace = dataframe.select_dtypes(include = 'object').columns.tolist()
    if "Date" in list_to_remplace:
        list_to_remplace.remove("Date")
        keeping_month(dataframe)
    if "Time" in list_to_remplace:
        list_to_remplace.remove("Time")
        keeping_hour(dataframe)
    return list_to_remplace



"""
Brief  : sorting the date column to only keeping the month
var    : dataframe : pandas dataframe on which we want to work
"""
def keeping_month(dataframe):
    dataframe['Month'] = dataframe['Date'].str.split('/').str[1]



"""
Brief  : sorting the hour column to removes the minutes
var    : dataframe : pandas dataframe on which we want to work
"""
def keeping_hour(dataframe):
    dataframe['Time'] = dataframe['Time'].str.split(':').str[0]



"""
Brief  : changing NaN into number
var    : dataframe : pandas dataframe on which we want to work
return : return a dictionnary with the column name as key and a list in attribut containing the map of the numerical values
"""
def create_map_and_remove_nan(dataframe):
    list_qualitative = get_object_column(dataframe)
    # print(list_qualitative)
    record_dic = {}
    for element in list_qualitative :
        clean_df, dic_value = qualititative_to_numerical(element, dataframe)
        record_dic[element] = dic_value
        # print(element, " done")
    # print("dic created")
    return record_dic



"""
Brief  : suppress the NaN remaining
var    : dataframe : pandas dataframe on which we want to work
return : return the Dataframe without any NaN
"""
def suppress_NaN(dataframe):
    dataframe = dataframe.dropna(axis=0)
    return dataframe



"""
Brief  : convert an object column in int
var    : dataframe : pandas dataframe on which we want to work
         column_name : name of the column we want to translate
"""
def convert_to_int(dataframe, column_name):
    dataframe[column_name] = dataframe[column_name].astype(int)



"""
Brief  : realising all the preprocessing operation we need to do on a dataframe
var    : name : name of the csv dataframe
return : map_dic : dictionnary with the column name as key and a list in attribut containing the map of the numerical values
         new_df : pandas dataset sorted and with only numerical values
"""
def preprocess_data():
    df = get_data()
    new_df = sorting_dataset(df)
    map_dic = create_map_and_remove_nan(new_df)
    new_df = suppress_NaN(new_df)
    convert_to_int(new_df, 'Time')
    convert_to_int(new_df, 'Month')
    new_df = new_df.drop('Date', axis=1)
    return map_dic, new_df



#### usage de pickle pour enreegistrer le dataframe et pas se retaper le truc qui prends du temps (gain de 50% de temps) --> a implementer

def save_datas(df, name):
    with open(name, "wb") as fichier:
        pickle.dump(df,fichier)

def open_datas(name):
    real_name = name+".pickle"
    try :
        with open(real_name, "rb") as fichier:
            df = pickle.load(fichier)
    except :
        df = get_data(name)
    return df

################################# test ###################################
# list_qualitative = ["Road_Type", "Junction_Control", "Pedestrian_Crossing-Human_Control", "Pedestrian_Crossing-Physical_Facilities", "Light_Conditions", 'Weather_Conditions', "Road_Surface_Conditions", "Special_Conditions_at_Site", "Carriageway_Hazards"]



dic, df = preprocess_data()



print(dic.keys())
print(df)
print(df['Month'])

print(df.isnull().sum().sum())
print()

