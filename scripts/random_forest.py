################################# import ###################################

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedShuffleSplit
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


################################# functions ################################

def stratified(dataframe,column_target):
    y = dataframe[column_target]
    x = dataframe.drop(column_target, axis=1)
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.33)
    for train_index, test_index in sss.split(x, y):
        X_train, X_test = x.iloc[train_index], x.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    return X_train, X_test, y_train, y_test


def random_forest(df):
    #df = df.drop(['Date'],axis='columns')
    target = df['Accident_Severity']
    df = df.drop(['Accident_Severity'], axis='columns')
    x_train , x_test, y_train, y_test = train_test_split(df, target, test_size=0.33)
    model = RandomForestClassifier(n_estimators=58, max_features=None, max_leaf_nodes=None, max_depth=None, random_state=None, n_jobs=-1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print('model created score: {:.3f}%'.format(model.score(x_test, y_test)*100))
    print("Matrice de confusion:")
    print(conf_matrix)
    joblib.dump(model, "random_forest.h5")
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', xticklabels=model.classes_,
                yticklabels=model.classes_)
    plt.title('Matrice de Confusion')
    plt.xlabel('Classe Prédite')
    plt.ylabel('Classe Réelle')
    plt.savefig("heatmap_Random_forest.png")
    plt.show()
    return model

# random_forest(df)

