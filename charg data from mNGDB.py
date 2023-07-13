# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId


# Établir la connexion à MongoDB
client = MongoClient('localhost', 27017)
db = client.datatest
collection = db.sales
collection2 = db.products
collection3 = db.markets
# Extraire les documents de la collection
documents = collection.find()

# =============================================================================
# # Traiter les documents extraits
# for document in documents:
#     # Effectuer les opérations souhaitées sur chaque document
#     print(document)  # Par exemple, imprimer le document
# =============================================================================

# Fermer la connexion à la base de données
# client.close()

#definissez une fonction pour le chiffre d'affaire
# trouver un produit grace à son id
def getProductById(id):
    return collection2.find_one({ "_id": ObjectId(id)})

#print(getProductById("6330ce1f4135f8089f9d2c25"))

# second fonction pour calculer le bénéfice avec for
def getProfitByGroup(idMarket):
    tt = 0
    for document in documents:
        # Effectuer les opérations souhaitées sur chaque document
        if document["from"] == idMarket:
            #print(document['cart']) 

            for product in document['cart']:
                
                prod = getProductById(product['_id'])
                profit = (product['price'] - prod['priceA']) * int(product['quantityWanted'])
                tt += profit
            
    return tt



def getTurnOverByGroup(idMarket):
    somme = 0

    for document in collection.find():
        # Effectuer les opérations souhaitées sur chaque document
        if document["from"] == idMarket:
            somme += document['total']
            
    return somme



#Définissez une fonction pour regrouper les données par boutique :
def regrouper_par_boutique():
    pipeline = [
        {"$group": {"_id": "$from", "count": {"$sum": 1}}}
    ]
    result = collection.aggregate(pipeline)
    return result



#Appelez la fonction regrouper_par_boutique() pour obtenir les résultats et calculer le chiffre d'affaire en meme temps :
resultats = regrouper_par_boutique()

for resultat in resultats:
    print(resultat['_id'])
    print("Le bénéfice est : ",getProfitByGroup(resultat['_id']))
    print("Le chiffre d'affaire est : ", getTurnOverByGroup(resultat['_id']))
    

# for next
# regroupement des etapes 4 & 5 par date

#nous utilisons l'opérateur $group dans le pipeline d'agrégation de MongoDB pour regrouper les données par l'attribut "from". L'opérateur $sum est utilisé pour compter le nombre d'occurrences pour chaque boutique. Le résultat est renvoyé par la fonction aggregate().
# fermer la connexion
# client.close()



#Définissez une fonction pour calculer le bénéfice et le chiffre d'affaires de chaque groupe :
# =============================================================================
# def calculer_benefice_chiffre_affaire_par_groupe():
#     pipeline = [
#         {"$group": {
#             "_id": "$groupe",
#             "chiffre_affaire": {"$sum": "$total"},
#             "benefice": {"$sum": {"$subtract": ["$total", "$cout_production"]}}
#         }}
#     ]
#     result = collection.aggregate(pipeline)
#     return result
# =============================================================================





            
# affichage du resultat 
print(getProfitByGroup("6330cd1d4135f8089f9d2c1b"))
#Appelez la fonction calculer_benefice_chiffre_affaire_par_groupe() pour obtenir les résultats :

# =============================================================================
# resultats = calculer_benefice_chiffre_affaire_par_groupe()
# for resultat in resultats:
#     print(resultat)
# 
# =============================================================================

def getProfitByGroup():
    tt = 0
    for document in documents:
        # Effectuer les opérations souhaitées sur chaque document
        print(document['cart']) 
        
        for product in document['cart']:
            
            prod = getProductById(product['_id'])
            profit = (product['price'] - prod['priceA']) * int(product['quantityWanted'])
            tt += profit
            
    return tt
client.close()


#importer les bibliotheque 
import numpy as np
from sklearn.linear_model import LinearRegression
#Définissez une fonction de prédiction :
def effectuer_prediction(X, Y, date_a_predire):
    # Convertir les données de date en nombres de jours depuis une référence
    X = np.array(X).reshape(-1, 1)
    jours_de_reference = X[0]  # Utilisez la première date comme référence
    X = (X - jours_de_reference) / np.timedelta64(1, 'D')

    # Créer un modèle de régression linéaire
    modele = LinearRegression()
    modele.fit(X, Y)

    # Convertir la date à prédire en nombre de jours depuis la référence
    date_a_predire = (date_a_predire - jours_de_reference) / np.timedelta64(1, 'D')

    # Effectuer la prédiction
    prediction = modele.predict([[date_a_predire]])
    return prediction
    
    
    
    