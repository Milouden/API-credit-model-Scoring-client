## Importation des librarys 
import joblib
import re

from flask import Flask, jsonify
import pandas as pd
import pickle
from lightgbm import LGBMClassifier

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


PATH = 'dataset/'
#      Chargement des données 

#    data = pd.read_csv('dataset/test_dataframe.csv')
data = pd.read_parquet('dataset/test_df.parquet')
print('la taille de Dataframe est = ', data.shape)

#data.drop(columns = {'Unnamed: 0'}  , inplace = True)

print('la taille de la nouvelle Dataframe est = ', data.shape)
#Chargement du modèle
# model = pickle.load(open('model/ModelClassifier.pkl', 'rb'))
model = pickle.load(open('model/ModelClassifier.pkl', 'rb'))



app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello Everyone ,  This is my Web API for credit scoring "





@app.route('/prediction_credit/<id_client>')
def prediction_credit(id_client):

    print('id client = ', id_client)
    
    #Récupération des données du client en question
    
    ID = int(id_client)
    X = data[data['SK_ID_CURR'] == ID]
    
    ## Elimination des features non important et la variable Cible 
    ##   'SK_ID_CURR'    : 
    ##   'INDEX'         :   Index de la dataframe  automatique
    ##   'TARGET'        :  variable cible 
    
    notimportant_features = ['SK_ID_CURR', 'INDEX', 'TARGET']
    selected_features = [col for col in data.columns if col not in notimportant_features]
    
    # Declaration de vecteur X
    X = X[selected_features]
    
    print('La taille du vecteur X  = ', X.shape)
    
    proba = model.predict_proba(X)
    prediction = model.predict(X)
    ## autre = model.
 
    #DEBUG
    print('L''identificateur du client : ', id_client)
  
    dict_final = {
        'prediction' : int(prediction),
        'proba' : float(proba[0][0])
        ##  Ajouter d'autres parametres 
        }
   
    print('Lancer une nouvelle Prédiction : \n', dict_final)
    

     # Say=uvegarde le résultat sous forme de JSON file 
        
    return jsonify(dict_final)


#  lancement de l'application   (  mode local  et non en mode production  ) 














if __name__ == "__main__":
    #import myapp
    #waitress.serve(myapp.wsgifunc, port=8041, url_scheme='https')
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    ## uvicorn.run(app = '127.0.0.1', port = 8000, debug = True)
    ##app.run(host = 'localhost', port = 8088, debug = True)
    ## from waitress import serve
    ##serve(app, host="0.0.0.0", port=8080)
    ##app.run(debug=True)
    ##app.run()