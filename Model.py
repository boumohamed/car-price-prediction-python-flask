import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('../avito_car_dataset_ALL.csv', encoding='latin-1')
#print(df.columns)

#df.to_html('avito_car_dataset_ALL.html')
# élimination des marque rare que nous n'avons pas assez d'informations sur

df.drop(df[ (df['Marque'] == "Suzuki") | (df['Marque'] == "mini") | (df['Marque'] == "Alfa Romeo")
            | (df['Marque'] == "Chevrolet") | (df['Marque'] == "Jeep") ].index, inplace=True)


df['Boite de vitesses'].replace(to_replace='--',value='Manuelle',inplace=True)
df['Origine'].replace(to_replace='',value='WW au Maroc',inplace=True)
df['Nombre de portes'].replace(to_replace='',value='5',inplace=True)
df['État'].replace(to_replace='',value='Bon',inplace=True)
df['Première main'].replace(to_replace='',value='Non',inplace=True)

# convertir les booléens en 0 et 1
df.replace(to_replace=True,value=1,inplace=True)
df.replace(to_replace=False,value=0,inplace=True)

df.drop(columns=["Unnamed: 0","Lien","Secteur","Ville"],inplace=True) #suppression


df = df.dropna()


# converssion en entiers

df['Année-Modèle'] = df['Année-Modèle'].astype(int)
df['Nombre de portes'] = df['Nombre de portes'].astype(int)
df['Puissance fiscale'] = df['Puissance fiscale'].astype(int)

# la moyenne de kilometrage

splited = df['Kilométrage'].str.split("-", n=1, expand=True)
splited[0] = splited[0].str.replace(' ', '').astype(int)
splited[1] = splited[1].str.replace(' ', '').astype(int)
df['Kilométrage'] = (splited[1] + splited[0])/2



# ----------------------------------- Model  ---------------------------------------------------#


LE = LabelEncoder()
LE.fit(df["Marque"])
df["Marque"] = LE.transform(df["Marque"])

LE1 = LabelEncoder()
LE1.fit(df["Modèle"])
df["Modèle"] = LE1.transform(df["Modèle"])

LE2 = LabelEncoder()
LE2.fit(df["Type de carburant"])
df["Type de carburant"] = LE2.transform(df["Type de carburant"])

LE3 = LabelEncoder()
LE3.fit(df['Boite de vitesses'])
df['Boite de vitesses'] = LE3.transform(df['Boite de vitesses'])

LE4 = LabelEncoder()
LE4.fit(df['Origine'])
df['Origine'] = LE4.transform(df['Origine'])

LE6 = LabelEncoder()
LE6.fit(df['État'])
df['État'] = LE6.transform(df['État'])

LE7 = LabelEncoder()
LE7.fit(df['Première main'])
df['Première main'] = LE7.transform(df['Première main'])

# show the data
#print(df.head(20))

#deviser le dataset en une base de donnees test et d'entrainement

X = df.drop(columns="Prix")
y = df["Prix"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# =============== Decision Tree Regressor ============
DecisionTreeRegressor_model=DecisionTreeRegressor()
# fit model
DecisionTreeRegressor_model.fit(X_train,y_train)


# Dump the trained decision tree classifier with Pickle
decision_tree_pkl_filename = 'DecisionTreeRegressor_Model.pkl'
decision_tree_model_pkl = open(decision_tree_pkl_filename, 'wb')
pickle.dump(DecisionTreeRegressor_model, decision_tree_model_pkl)
# Close the pickle instances
decision_tree_model_pkl.close()
# Expected value Y using X test
y_predDTR = DecisionTreeRegressor_model.predict(X_test)



print("====================================================================")
# ----------------/// prediction function ///---------------------
def predict(Marque, Modele, Annee_Modele, Type_de_carburant, Puissance_fiscale, Kilometrage='30 000 - 34 999', etat='Très bon', Boite_de_vitesses='Manuelle',\
    Nombre_de_portes=5, Origine='WW au Maroc', Premiere_main='Non', Jantes_aluminium=False, Airbags=False, Climatisation=False, Systeme_de_navigation_GPS=False,\
    Toit_ouvrant=False, Sieges_cuir=False, Radar_de_recul=False, Camera_de_recul=False, Vitres_electriques=False, ABS=False, ESP=False, Regulateur_de_vitesse=False,\
    Limiteur_de_vitesse=False, CD_MP3_Bluetooth=False, Ordinateur_de_bord=False, Verrouillage_centralise_a_distance=False):
    print('\n\n', Marque, Modele)
    Marque = LE.transform([Marque])[0]
    Modele = LE1.transform([Modele])[0]
    Type_de_carburant = LE2.transform([Type_de_carburant])
    Boite_de_vitesses = LE3.transform([Boite_de_vitesses])
    Origine = LE4.transform([Origine])
    Premiere_main = LE7.transform([Premiere_main])
    etat = LE6.transform([etat])
    Kilometrage = Kilometrage.split('-')
    Kilometrage = int(Kilometrage[0].replace(' ', '')) + int(Kilometrage[1].replace(' ', '')) / 2

    car = [Marque,Modele, Annee_Modele, Kilometrage, Type_de_carburant, Puissance_fiscale, Boite_de_vitesses, Nombre_de_portes, Origine, \
           Premiere_main, etat, Jantes_aluminium, Airbags, Climatisation, Systeme_de_navigation_GPS, Toit_ouvrant, Sieges_cuir, Radar_de_recul, \
           Camera_de_recul, Vitres_electriques, ABS, ESP, Regulateur_de_vitesse, Limiteur_de_vitesse, CD_MP3_Bluetooth, Ordinateur_de_bord, Verrouillage_centralise_a_distance]

    prediction = round(DecisionTreeRegressor_model.predict([car])[0], 2)
    print('\n>>> le prix du véhicule estimé', prediction)


#https://www.avito.ma/fr/casablanca/voitures_d'occasion/Clio_4_2015_2%C3%A8me_main_51835420.htm


predict(Marque='Renault', Modele='Clio', Annee_Modele=2015, Type_de_carburant='Diesel', Puissance_fiscale=7, Kilometrage='140 000 - 149 999',\
        etat='Excellent', Boite_de_vitesses='Manuelle', Nombre_de_portes=5, Origine='WW au Maroc', Premiere_main='Non', Jantes_aluminium=False,\
        Airbags=True, Climatisation=True, Systeme_de_navigation_GPS=True, Toit_ouvrant=False, Sieges_cuir=False, Radar_de_recul=False,\
        Camera_de_recul=False, Vitres_electriques=True, ABS=False, ESP=False, Regulateur_de_vitesse=True, Limiteur_de_vitesse=True,\
        CD_MP3_Bluetooth=False, Ordinateur_de_bord=False, Verrouillage_centralise_a_distance=True)

