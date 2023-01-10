from flask import Flask, render_template, request
import pandas as pd
from voiture import Voiture
from sklearn.preprocessing import LabelEncoder
import pickle

app = Flask(__name__)
df = pd.read_csv('cleaned_data.csv')

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

@app.route('/')
def index():
    return(render_template("index.html"))

@app.route('/predict', methods = ['POST'])
def prediction():
    v = RequestHandler(request.form)
    price = predict(v.Marque, v.Modele, v.Annee_Modele, v.Type_de_carburant, v.Puissance_fiscale, v.Kilometrage,
            v.etat, v.Boite_de_vitesses, v.Nombre_de_portes, v.Origine,
            v.Premiere_main, v.Jantes_aluminium, v.Airbags,
            v.Climatisation, v.Systeme_de_navigation_GPS, v.Toit_ouvrant, v.Sieges_cuir,
            v.Radar_de_recul, v.Camera_de_recul,
            v.Vitres_electriques, v.ABS, v.ESP, v.Regulateur_de_vitesse, v.Limiteur_de_vitesse,
            v.CD_MP3_Bluetooth, v.Ordinateur_de_bord, v.Verrouillage_centralise_a_distance)

    return(render_template("fileuploaded.html", prix=price, car = v.Marque + " " + v.Modele))


def Load_Model():
    Pkl_Filename = "DecisionTreeRegressor_Model.pkl"
    with open(Pkl_Filename, 'rb') as file:
        Pickled_LR_Model = pickle.load(file)
    print("model Loaded")
    return Pickled_LR_Model



def RequestHandler(values):
    Marque = values.get('Marque')
    Modele = values.get('Modele')
    Annee_Modele = values.get('Annee_Modele')
    Type_de_carburant = values.get('Type_de_carburant')
    Puissance_fiscale = values.get('Puissance_fiscale')
    Kilometrage = values.get('Kilometrage')
    etat = values.get('etat')
    Boite_de_vitesses = values.get('Boite_de_vitesses')
    Nombre_de_portes = values.get('Nombre_de_portes')
    Origine = values.get('Origine')
    Premiere_main = values.get('Premiere_main')
    Jantes_aluminium = True if values.get('Jantes_aluminium') else False
    Airbags = True if values.get('Airbags') else False
    Climatisation = True if values.get('Climatisation') else False
    Systeme_de_navigation_GPS = True if values.get('Systeme_de_navigation_GPS') else False
    Toit_ouvrant = True if values.get('Toit_ouvrant') else False
    Sieges_cuir = True if values.get('Sieges_cuir') else False
    Radar_de_recul = True if values.get('Radar_de_recul') else False
    Camera_de_recul = True if values.get('Camera_de_recul') else False
    Vitres_electriques = True if values.get('Vitres_electriques') else False
    ABS = True if values.get('ABS') else False
    ESP =  True if values.get('ESP') else False
    Regulateur_de_vitesse = True if values.get('Regulateur_de_vitesse') else False
    Limiteur_de_vitesse = True if values.get('Limiteur_de_vitesse') else False
    Ordinateur_de_bord = True if values.get('Ordinateur_de_bord') else False
    CD_MP3_Bluetooth = True if values.get('CD_MP3_Bluetooth') else False
    Verrouillage_centralise_a_distance = True if values.get('Verrouillage_centralise_a_distance') else False

    v = Voiture(Marque, Modele, Annee_Modele, Type_de_carburant, Puissance_fiscale,
                Kilometrage, etat, Boite_de_vitesses, Nombre_de_portes, Origine, Premiere_main,
                Jantes_aluminium, Airbags, Climatisation, Systeme_de_navigation_GPS,
                Toit_ouvrant, Sieges_cuir, Radar_de_recul, Camera_de_recul, Vitres_electriques,
                ABS, ESP, Regulateur_de_vitesse, Limiteur_de_vitesse, Ordinateur_de_bord, CD_MP3_Bluetooth, Verrouillage_centralise_a_distance)
    return v


def predict(Marque, Modele, Annee_Modele, Type_de_carburant, Puissance_fiscale, Kilometrage,
            etat, Boite_de_vitesses, Nombre_de_portes, Origine, Premiere_main, Jantes_aluminium, Airbags, Climatisation,
            Systeme_de_navigation_GPS, Toit_ouvrant, Sieges_cuir, Radar_de_recul, Camera_de_recul, Vitres_electriques,
            ABS, ESP, Regulateur_de_vitesse, Limiteur_de_vitesse, CD_MP3_Bluetooth, Ordinateur_de_bord, Verrouillage_centralise_a_distance):

    Marque = LE.transform([Marque])[0]
    Modele = LE1.transform([Modele])[0]
    Type_de_carburant = LE2.transform([Type_de_carburant])
    Boite_de_vitesses = LE3.transform([Boite_de_vitesses])
    Origine = LE4.transform([Origine])
    Premiere_main = LE7.transform([Premiere_main])
    etat = LE6.transform([etat])
    Kilometrage = Kilometrage.split('-')
    Kilometrage = int(Kilometrage[0].replace(' ', '')) + int(Kilometrage[1].replace(' ', '')) / 2

    car = [Marque, Modele, Annee_Modele, Kilometrage, Type_de_carburant, Puissance_fiscale, Boite_de_vitesses,
           Nombre_de_portes, Origine, Premiere_main, etat, Jantes_aluminium, Airbags, Climatisation, Systeme_de_navigation_GPS, Toit_ouvrant,
           Sieges_cuir, Radar_de_recul, Camera_de_recul, Vitres_electriques, ABS, ESP, Regulateur_de_vitesse, Limiteur_de_vitesse, CD_MP3_Bluetooth,
           Ordinateur_de_bord, Verrouillage_centralise_a_distance]

    DecisionTreeRegressor_model = Load_Model()

    predictions = round(DecisionTreeRegressor_model.predict([car])[0], 2)

    print('\n>>> le prix du véhicule estimé', predictions)
    return predictions


app.run()