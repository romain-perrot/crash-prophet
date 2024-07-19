import numpy as np
import pandas as pd

import car_accident_traitement

dic, df = car_accident_traitement.preprocess_data('UK_Accident.csv')

def mapping_function(df, dic, argument_column):
    arrayMapped = []
    for value in dic[argument_column]:
        arrayMapped.append(value)
    array_dic = {index: value for index, value in enumerate(arrayMapped)}
    df[argument_column] = df[argument_column].map(array_dic)
    return df

# Assuming you have a DataFrame 'df' with a column 'road type'
# You can use the following code to select 6,000 random rows for each unique 'road type'

# Define the number of rows to select for each 'road type'
rows_per_group = 300

new_data_set = pd.DataFrame()

df = mapping_function(df, dic, 'Road_Type')

# Group the DataFrame by 'road type' and sample 6,000 rows for each group
for _, group in df.groupby('Road_Type'):
    sampled_group = group.sample(n=rows_per_group, replace=True)  # Change 'replace' as needed
    new_data_set = new_data_set._append(sampled_group)

new_data_set.info()
print(new_data_set['Road_Type'].value_counts())
new_data_set.to_csv('File_for_Satellite_300_Images.csv')