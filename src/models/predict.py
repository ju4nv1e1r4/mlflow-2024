import mlflow
logged_model = 'runs:/c2cb855ab8be4a8693cfc6975f739b35/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
import pandas as pd

data = pd.read_csv('data/processed/casas_X.csv')
predicted = loaded_model.predict(data)

data['predicted'] = predicted
data.to_csv('reports/precos.csv', index=False)
