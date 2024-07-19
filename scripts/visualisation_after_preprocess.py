import sys

import pandas as pd

assert sys.version_info >= (3, 5)
# Python ≥3.5 is required

import car_accident_traitement

dic, df = car_accident_traitement.preprocess_data('UK_Accident.csv')

df.info()

# To plot figures
import matplotlib.pyplot as plt

df.hist(bins=50, figsize=(20,15))
plt.show()
#According to the plots, the features related to car accident and to keep are: the time, the accident severity, the day

#Display the string values associated to the numeric categories
for i in dic.keys():
  print(i)
  print(dic[i])