import streamlit as st
import pandas as pd
import mlflow

st.markdown('##[Previsão de Preços de Casas]')

def predict(tamanho, ano, garagem):
    logged_model = 'runs:/c2cb855ab8be4a8693cfc6975f739b35/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    data = {
        'tamanho': [tamanho],
        'ano': [ano],
        'garagem': [garagem]
    }

    df = pd.DataFrame(data)
    predicted = loaded_model.predict(df)

    return (predicted[0])

# print(predict(150, 2003, 2))

tamanho = float(st.number_input('Qual o tamanho da casa?'))
ano = int(st.number_input('Qual o ano da casa?'))
garagem = int(st.number_input('Quantas garagens tem a casa?') )

if st.button('Prever'):
    pred = predict(tamanho, ano, garagem)
    st.markdown(':blue[**O preço da casa é:**]', pred)
