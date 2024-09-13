from flask import Flask
import pandas as pd
import mlflow


app = Flask(__name__)


@app.route('/')
def home():
    return 'Previsão de preços de casas'


@app.route('/predict/<tamanho>/<ano>/<garagem>')

def predict(tamanho, ano, garagem):
    logged_model = 'runs:/c2cb855ab8be4a8693cfc6975f739b35/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    df = {
        'columns': ['tamanho, ano, garagem'],
        'data': [[tamanho, ano, garagem]]   
        }

    predicted = loaded_model.predict(df)

    data = pd.DataFrame(predicted)
    
    data.to_csv('reports/precos_preditos.csv', index=False)

    return data


app.run(debug=True, port= 5001, host='0.0.0.0')