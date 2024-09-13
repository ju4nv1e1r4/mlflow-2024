import streamlit as st
import pandas as pd
import mlflow

st.markdown('##[Previsão de Preços de Casas]')

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


tamanho = st.number_input('Qual o tamanho da casa?')
ano = st.number_input('Qual o ano da casa?')
garagem = st.number_input('Quantas garagens tem a casa?') 

if st.button('Prever'):
    st.markdown(':blue[**O preço da casa é:**]', predict(tamanho, ano, garagem))    