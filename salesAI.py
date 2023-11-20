# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 21:17:41 2023

@author: IsRa.ChaaBani
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime


# Établir la connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client.datatest
collection = db.sales
collection2 = db.products
collection3 = db.markets
# Extraire les documents de la collection
documents = collection.find()

#definissez une fonction pour le chiffre d'affaire
# trouver un produit grace à son id
def getProductById(id):
    return collection2.find_one({ "_id": ObjectId(id)})

# Calculer le bénéfice total par date
def getProfitByGroup(idMarket):
    profits_par_date = {}
    chiffre_affaire_par_date = {}

    for document in documents:
        if document["from"] == idMarket:
            date_document = document['created_at']
            profit_document = 0
            chiffre_affaire_document = document['total']

            for product in document['cart']:
                
                prod = getProductById(product['_id'])
                profit = (product['price'] - prod['priceA']) * int(product['quantityWanted'])
                profit_document += profit


            profits_par_date[date_document] = profits_par_date.get(date_document, 0) + profit_document
            chiffre_affaire_par_date[date_document] = chiffre_affaire_par_date.get(date_document, 0) + chiffre_affaire_document
            
    return profits_par_date, chiffre_affaire_par_date


#Calculer le chifre d'affaire total par date 

def getTurnOverByGroup(idMarket):
    chiffre_affaire_par_date = {}

    for document in collection.find():
        if document["from"] == idMarket:
            date_document = document['created_at']
            chiffre_affaire_document = document['total']

            # Ajouter le chiffre d'affaires du document à la date correspondante dans le dictionnaire
            chiffre_affaire_par_date[date_document] = chiffre_affaire_par_date.get(date_document, 0) + chiffre_affaire_document

    return chiffre_affaire_par_date



#Définissez une fonction pour regrouper les données par boutique :
def regrouper_par_boutique():
    pipeline = [
        {"$group": {"_id": "$from", "count": {"$sum": 1}}}
    ]
    result = collection.aggregate(pipeline)
    return result


# Convertir les dates en valeurs numériques
def convert_dates_to_numeric(dates):
    numeric_dates = []
    for date_str in dates:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        numeric_date = int(date_obj.timestamp())
        numeric_dates.append(numeric_date)
    return numeric_dates

# Fonction de prédiction du chiffre d'affaires
def predict_turnover_by_date(date, idMarket):
    # Calculer le chiffre d'affaires par date à partir des données existantes
    turnover_data = getTurnOverByGroup(idMarket)
    
    # Extraire X (dates) et Y (chiffre d'affaires) du dictionnaire turnover_data
    dates = list(turnover_data.keys())
    chiffre_affaire = list(turnover_data.values())

    # Convertir les dates en valeurs numériques
    numeric_dates = convert_dates_to_numeric(dates)

    # Créer et ajuster le modèle de régression linéaire
    model = LinearRegression()
    model.fit(np.array(numeric_dates).reshape(-1, 1), np.array(chiffre_affaire))

    # Convertir la date d'entrée au bon format et faire une prédiction
    input_date = datetime.strptime(date, '%d/%m/%Y')
    input_numeric_date = int(input_date.timestamp())
    predicted_turnover = model.predict([[input_numeric_date]])

    return predicted_turnover[0]


#Appelez la fonction regrouper_par_boutique() pour obtenir les résultats et calculer le chiffre d'affaire en meme temps :
resultats = regrouper_par_boutique()

for resultat in resultats:
    print(resultat['_id'])
    print("Le bénéfice est : ",getProfitByGroup(resultat['_id']))
    print("Le chiffre d'affaire est : ", getTurnOverByGroup(resultat['_id']))
    date_prediction = '06/04/2023'
    chiffre_affaire_predit = predict_turnover_by_date(date_prediction, resultat['_id'])
    print("Le chiffre d'affaire prévu pour le {} est : {}".format(date_prediction, chiffre_affaire_predit))
       
 
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello, World!"


# if __name__ == '__main__':
#     app.run()




# # client.close()










