################################# import ###################################

import car_accident_traitement as car
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
import pandas as pd
import random_forest as rf
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

################################# functions ################################

"""
Brief  : geting a training and test dataset with the function train_test_split
var    : dataframe : pandas dataframe on which we want to work
         column_target : name of the dataframe's column we want as target
return : return the X test and train and tue Y test and train
"""
def training_and_verif(dataframe, column_target):
    y = dataframe[column_target]
    print("total :", y.value_counts())
    x = dataframe
    x.drop(column_target, axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    return X_train, X_test, y_train, y_test


"""
Brief  : creation and training of a bayesien model
var    : dataframe : pandas dataframe on which we want to work
         target : name of the dataframe's column we want as target
return : return the trained bayesien model and both of the test dataset
"""
# def model_Bayes(dataframe,target):
#     # X_train, X_test, y_train, y_test = training_and_verif(dataframe, target)
#     X_train, X_test, y_train, y_test = stratified(dataframe, target)
#     print("unique : ", y_train.value_counts())
#     model_bayes = GaussianNB(var_smoothing=1e-9)
#     model_bayes.fit(X_train, y_train)
#     return model_bayes , X_test, y_test


def model_Bayes(dataframe, target, use_all_data=False):
    if use_all_data:
        # Utiliser l'ensemble complet de données
        X_train, X_test, y_train, y_test = train_test_split(
            dataframe.drop(target, axis=1), dataframe[target], test_size=0.33, random_state=42
        )
    else:
        # Utiliser uniquement les données de la classe 1
        class_1_data = dataframe[dataframe[target] == 1]
        X_train, X_test, y_train, y_test = train_test_split(
            class_1_data.drop(target, axis=1), class_1_data[target], test_size=0.33, random_state=42
        )

    print("Unique labels in training set:", y_train.value_counts())

    model_bayes = GaussianNB(var_smoothing=1e-9)
    model_bayes.fit(X_train, y_train)
    joblib.dump(model_bayes, "bayes.h5")
    

    return model_bayes, X_test, y_test


def debogage(df, target):
    # y = df[target]
    # x = df.drop(target, axis=1) 
    df_test = df 
    groupes = df.groupby(target)
    class1 = groupes.get_group(1)
    class2 = groupes.get_group(2)
    class3 = groupes.get_group(3)
    quarter_class3 = class3.sample(frac=0.165, random_state=42)
    print("type", type(class1), type(df_test))
    new = pd.concat([class1, class1], ignore_index=True)
    new = pd.concat([new, class1], ignore_index=True)
    new = pd.concat([new, class2], ignore_index=True)
    new = pd.concat([new, quarter_class3], ignore_index=True)
    #new_gr = new.groupby(target)
    #print("nb : ", new_gr.value_counts())
    #resultat = new_gr.apply(lambda x: x.sample(n=38880))
    # print("idk : ",resultat)
    return class1


def dataAugm(df, target):
    # y = df[target]
    # x = df.drop(target, axis=1)  
    groupes = df.groupby(target)
    class1 = groupes.get_group(1)
    if not class1.empty:
        # Définir le nombre de valeurs supplémentaires à générer (réduit)
        valeurs_supplementaires =19440

        # Générer des valeurs de bruit aléatoire pour chaque colonne sauf 'target'
        bruit = np.random.normal(0, 0.1, size=(valeurs_supplementaires, class1.shape[1]-1))

        # Dupliquer le groupe et ajouter le bruit
        class1_augmente = pd.DataFrame(np.tile(class1.iloc[:, :-1].values, (valeurs_supplementaires, 1)) + bruit,
                                       columns=class1.columns[:-1])

        # Ajouter la colonne 'target' sans aucune modification
        class1_augmente['target'] = 1

        # Concaténer le groupe augmenté avec le reste des groupes
        resultat = pd.concat([class1_augmente] + [groupe for cle, groupe in groupes if cle != 1], ignore_index=True)

    resultat = groupes.apply(lambda x: x.sample(n=38880))
    # print("idk : ",resultat)
    return resultat

"""
Brief  : geting a training and test dataset with the class stratified
var    : dataframe : pandas dataframe on which we want to work
         column_target : name of the dataframe's column we want as target
return : return the X test and train and tue Y test and train
"""
def stratified(dataframe,column_target):
    y = dataframe[column_target]
    x = dataframe.drop(column_target, axis=1)  
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.33)
    for train_index, test_index in sss.split(x, y):
        X_train, X_test = x.iloc[train_index], x.iloc[test_index]  
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    return X_train, X_test, y_train, y_test



def only_good_column(df):
    ans = df.drop('Location_Easting_OSGR', axis=1)
    ans = ans.drop('Unnamed: 0', axis=1)
    ans = ans.drop('Longitude', axis=1)
    ans = ans.drop('Latitude', axis=1)
    ans = ans.drop('Location_Northing_OSGR', axis=1)
    ans = ans.drop('Number_of_Vehicles', axis=1)
    ans = ans.drop('Number_of_Casualties', axis=1)
    ans = ans.drop('1st_Road_Class', axis=1)
    ans = ans.drop('1st_Road_Number', axis=1)
    ans = ans.drop('Junction_Control', axis=1)
    ans = ans.drop('2nd_Road_Class', axis=1)
    ans = ans.drop('Pedestrian_Crossing-Physical_Facilities', axis=1)
    ans = ans.drop('Pedestrian_Crossing-Human_Control', axis=1)
    ans = ans.drop('Special_Conditions_at_Site', axis=1)
    ans = ans.drop('Carriageway_Hazards', axis=1)
    return ans







################################# test ###################################



dic, df = car.preprocess_data()
df = only_good_column(df)
# df = df.drop('Date', axis=1)

class1 = debogage(df,"Accident_Severity")
# test = dataAugm(df,"Accident_Severity")
# print(df)


# Entraînement sur uniquement la classe 1
model_class_1, X_test_class_1, y_test_class_1 = model_Bayes(class1, 'Accident_Severity', use_all_data=False)

# Entraînement sur l'ensemble complet de données
model_all_data, X_test_all_data, y_test_all_data = model_Bayes(df, 'Accident_Severity', use_all_data=True)


y_pred = model_all_data.predict(X_test_all_data)

conf_matrix = confusion_matrix(y_test_all_data, y_pred)
print("Matrice de confusion:")
print(conf_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=model_all_data.classes_,
            yticklabels=model_all_data.classes_)
plt.title('Matrice de Confusion')
plt.xlabel('Classe Prédite')
plt.ylabel('Classe Réelle')
plt.savefig("heatmap_bayes.png")
plt.show()

print(f"Précision: {model_all_data.score(X_test_all_data, y_test_all_data)}")

scores = cross_val_score(model_all_data, X_test_all_data, y_test_all_data, cv=5)
print("Précision moyenne après validation croisée :", np.mean(scores))


print(df.columns)

# rf.random_forest(df)

