import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
assert sys.version_info >= (3, 5)

import car_accident_traitement

dic, df = car_accident_traitement.preprocess_data('UK_Accident.csv')

#Mapping function to get back the string inputs from the interval data
def mapping_function(df, dic, argument_column):
    arrayMapped = []
    for value in dic[argument_column]:
        arrayMapped.append(value)
    array_dic = {index: value for index, value in enumerate(arrayMapped)}
    df[argument_column] = df[argument_column].map(array_dic)
    return df

df.info()

#The week days data are not in the dictionary, thus it is done manually
day_mapping = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

# Remapping the integer values into string values for the 3 columns : week days, weather conditions, road surface conditions
df['Day_of_Week'] = df['Day_of_Week'].map(day_mapping)

df = mapping_function(df, dic, 'Weather_Conditions')

df = mapping_function(df, dic, 'Road_Surface_Conditions')

#Create a new df for time and week days
timeData = pd.DataFrame(df[['Time', 'Day_of_Week']])

#Groups the time and week days entities having the same values
data_time = timeData.groupby(["Time", "Day_of_Week"]).size().unstack().fillna(0)

# Create a stacked area plot
ax = data_time.plot(kind="bar", stacked=True, colormap="Paired")

# Customize the plot
plt.title("Repartition of Days for Each Hour")
plt.xlabel("Hour")
plt.ylabel("Count")
plt.legend(title="Day", loc="upper left", bbox_to_anchor=(1, 1))
plt.show()

#Create a new df for Month and Weather conditions
weatherData = pd.DataFrame(df[['Month', 'Weather_Conditions']])

#Groups the month and weather conditions entities having the same values
data_weather = weatherData.groupby(['Month', 'Weather_Conditions']).size().unstack().fillna(0)

# Create a stacked area plot
ax = data_weather.plot(kind="bar", stacked=True, colormap="Paired")

# Customize the plot
plt.title("Repartition of Weather conditions over the Month")
plt.xlabel("Month")
plt.ylabel("Count")
plt.legend(title="Weather_Conditions", loc="upper left", bbox_to_anchor=(1, 1))
plt.show()

#Create new df for Weather conditions and road surface conditions
roadData = pd.DataFrame(df[['Weather_Conditions', 'Road_Surface_Conditions']])

#Groups the weather conditions and road surface conditions entities having the same values
data_road = roadData.groupby(['Weather_Conditions', 'Road_Surface_Conditions']).size().unstack().fillna(0)

# Create a stacked area plot
ax = data_road.plot(kind="bar", stacked=True, colormap="Paired")

# Customize the plot
plt.title("Repartition of road conditions depending on the weather")
plt.xlabel("Weather_Conditions")
plt.ylabel("Count")
plt.legend(title="Road_Conditions", loc="upper left", bbox_to_anchor=(1, 1))
plt.show()
