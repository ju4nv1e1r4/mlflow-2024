from flask import Flask, request, jsonify, render_template
import pandas as pd
import mlflow

app = Flask(__name__)

logged_model = 'mlruns/133917091883630461/c2cb855ab8be4a8693cfc6975f739b35/artifacts/model'
loaded_model = mlflow.pyfunc.load_model(logged_model)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form if request.form else request.get_json()

        tamanho = float(data.get('tamanho'))
        ano = int(data.get('ano'))
        garagem = int(data.get('garagem'))

        input_data = pd.DataFrame({
            'tamanho': [tamanho],
            'ano': [ano],
            'garagem': [garagem]
        })

        prediction = loaded_model.predict(input_data)
        prediction_value = float(prediction[0])

        return jsonify({
            'preco_previsto': prediction_value
        })
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')