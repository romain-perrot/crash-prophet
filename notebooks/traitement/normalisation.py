################################# functions #################################

"""
Attributs to normalise:

['Accident_Severity', ???
'Day_of_Week',
'Time',
'Road_Type',
'Junction_Control',
'Pedestrian_Crossing-Human_Control',
'Pedestrian_Crossing-Physical_Facilities',
'Light_Conditions',
'Weather_Conditions',
'Road_Surface_Conditions',
'Special_Conditions_at_Site',
'Carriageway_Hazards',
'Year', ???
'Month']
"""

def normalisation(df, column_name):
    counts = df[column_name].value_counts()
    total = df[column_name].count()
    replacement_dict = (counts / total) * 100
    df[column_name] = df[column_name].map(replacement_dict)
    return df

# normalised_df = normalisation(df, df_column)
