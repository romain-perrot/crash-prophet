################################## import ##################################

from scipy.stats import f_oneway
import car_accident_traitement
from notebooks.traitement.normalisation import normalisation
from scipy import stats



############################## Initialisation ##############################

processed_df = car_accident_traitement.df
df_column = processed_df.columns.tolist()



################################# functions #################################

"""
Brief  : making a correlation matrix with the Accident_Severity attribute
Return : an array with the the correlation between all attributes and Accident_Severity
"""
# def processed_corr_matrix():

#     corr_matrix = processed_df.corr()

#     correlation = corr_matrix['Accident_Severity'].sort_values(ascending=False)
#     print(correlation, "\n")

#     return correlation

# def normalised_corr_matrix():

#     df_column = ['Accident_Severity', 'Day_of_Week', 'Time', 'Road_Type', 'Junction_Control', 'Pedestrian_Crossing-Human_Control', 'Pedestrian_Crossing-Physical_Facilities', 'Light_Conditions', 'Weather_Conditions', 'Road_Surface_Conditions', 'Special_Conditions_at_Site', 'Carriageway_Hazards', 'Year', 'Month']
#     df_column.reverse()

#     temp = processed_corr_matrix()

#     for column_name in df_column:
#         print("Normalisation for", column_name)
#         normalised = normalisation(processed_df, column_name)

#         corr_matrix = normalised.corr()

#         correlation = corr_matrix['Accident_Severity'].sort_values(ascending=False)

#         print(correlation, "\n")

#         for element in df_column:
#             print("Comparing correlation for", element)
#             if element in temp:
#                 if correlation[element] < temp[element]:
#                     print('Better correlation')
#                 elif correlation[element] > temp[element]:
#                     print('Worse correlation')
#                 else:
#                        print('No change...')
#             else:
#                 print(f"'{element}' not found in temp dictionary.")

#         temp = correlation

#         print("\n\n\n")

# normalised_corr_matrix()

"""
Brief  : making a correlation matrix with normalisation values (percentage) DO NOT WORK (cf. normailsation.py)
Return : nothing
"""
# x = df["Weather_Conditions"].value_counts()
# y = df["Weather_Conditions"].count()
# for i in range(len(x)):
#     ans = x[i] / y
#     print(ans)

# for element in df_column:
#     x = df[element].value_counts()
#     y = df[element].count()
#     print(len(x))
#     for i in range(len(x)):
#         ans = x[i] / y
#         print(ans)
#     print(" ")



"""
Brief  : using f_oneway to compare statistical values
Return : not good enough result
"""
# severity_list = df['Accident_Severity'].tolist()

# for attribut in df_column:
#     print("Accident_Severity and " + attribut)
#     attribut = df[attribut].values
#     result = f_oneway(severity_list, attribut)
#     print(result)
#     print(" ")



"""
Brief  : spearman correlation
Return : statistic between all attributes and Accident_Severity
"""
# Accident_Severity = processed_df['Accident_Severity'].tolist()

# for element in df_column:
#     res = stats.spearmanr(Accident_Severity, processed_df[element])
#     print(f"Spearman correlation between 'Accident_Severity' and '{element}': {res.correlation}")
