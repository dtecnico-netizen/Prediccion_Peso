
import streamlit as st
import pandas as pd
import numpy as np
import os

# Mostrar logo discreto en la esquina superior izquierda
logo_path = os.path.join(os.path.dirname(__file__), 'logo mejorado.jpg')
st.markdown(f"""
    <div style='position: fixed; top: 1.5rem; left: 1.5rem; z-index: 10;'>
        <img src='file://{logo_path}' width='70' style='opacity:0.7; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'/>
    </div>
    """, unsafe_allow_html=True)


# Cargar coeficientes de los modelos
base_path = os.path.dirname(__file__)
df_dia_vs_cons = pd.read_csv(os.path.join(base_path, 'resultados_dia_vs_cons.csv'))
df_cons_vs_peso = pd.read_csv(os.path.join(base_path, 'resultados_cons_vs_peso.csv'))

# Obtener opciones únicas
razas = df_dia_vs_cons['RAZA'].unique()
sexos = df_dia_vs_cons['SEXO'].unique()

st.title('Predicción Consumo Acumulado y Peso')

# Selección de parámetros
raza = st.selectbox('Seleccione la RAZA', razas, index=list(razas).index('ROSS') if 'ROSS' in razas else 0)
sexo = st.selectbox('Seleccione el SEXO', sexos, index=list(sexos).index('MIXTO') if 'MIXTO' in sexos else 0)
dia = st.number_input('Ingrese el Día', min_value=1, step=1)
cons_acum_real = st.number_input('Ingrese el Cons_Acum real', min_value=0.0, step=1.0)
peso_real = st.number_input('Ingrese el Peso real', min_value=0.0, step=1.0)

# Filtrar coeficientes
row_dia_vs_cons = df_dia_vs_cons[(df_dia_vs_cons['RAZA'] == raza) & (df_dia_vs_cons['SEXO'] == sexo)].iloc[0]
row_cons_vs_peso = df_cons_vs_peso[(df_cons_vs_peso['RAZA'] == raza) & (df_cons_vs_peso['SEXO'] == sexo)].iloc[0]

# Calcular Cons_Acum estimado para el Día
coefs1 = [row_dia_vs_cons[f'coef_{i}'] for i in range(5)]
intercepto1 = row_dia_vs_cons['intercepto']
cons_acum_estimado = intercepto1 + sum([coefs1[i] * dia**i for i in range(5)])

# Calcular Peso estimado para el Cons_Acum ingresado
coefs2 = [row_cons_vs_peso[f'coef_{i}'] for i in range(5)]
intercepto2 = row_cons_vs_peso['intercepto']
peso_estimado = intercepto2 + sum([coefs2[i] * cons_acum_real**i for i in range(5)])

if st.button('Generar Informe'):

    st.subheader('Resultados')
    st.write(f"Cons_Acum estimado para Día {dia}: **{cons_acum_estimado:.2f}**")
    st.write(f"Cons_Acum real ingresado: **{cons_acum_real:.2f}**")
    diff_cons = cons_acum_real - cons_acum_estimado
    pct_cons = (diff_cons / cons_acum_estimado * 100) if cons_acum_estimado != 0 else 0
    st.write(f"Diferencia Cons_Acum (real - estimado): **{diff_cons:.2f}** ({pct_cons:.2f}%)")
    st.write('---')
    st.write(f"Peso estimado para Cons_Acum {cons_acum_real}: **{peso_estimado:.2f}**")
    st.write(f"Peso real ingresado: **{peso_real:.2f}**")
    diff_peso = peso_real - peso_estimado
    pct_peso = (diff_peso / peso_estimado * 100) if peso_estimado != 0 else 0
    st.write(f"Diferencia Peso (real - estimado): **{diff_peso:.2f}** ({pct_peso:.2f}%)")
    st.write('---')

    # Gráfica 1: Cons_Acum estimado vs real para el Día seleccionado
    import matplotlib.pyplot as plt
    fig1, ax1 = plt.subplots()
    dias = np.arange(1, 45)
    cons_acum_pred = intercepto1 + sum([coefs1[i] * dias**i for i in range(5)])
    ax1.plot(dias, cons_acum_pred, label='Cons_Acum estimado', color='red')
    ax1.scatter([dia], [cons_acum_real], color='blue', label='Cons_Acum real (input)', s=80)
    ax1.scatter([dia], [cons_acum_estimado], color='green', label='Cons_Acum estimado (input)', s=80, marker='x')
    ax1.set_xlabel('Día')
    ax1.set_ylabel('Cons_Acum')
    ax1.set_title('Cons_Acum estimado vs real por Día')
    ax1.legend()
    st.pyplot(fig1)

    # Gráfica 2: Peso estimado vs real para el Cons_Acum ingresado
    fig2, ax2 = plt.subplots()
    cons_range = np.linspace(0, max(cons_acum_real, 4500), 100)
    peso_pred = intercepto2 + sum([coefs2[i] * cons_range**i for i in range(5)])
    ax2.plot(cons_range, peso_pred, label='Peso estimado', color='orange')
    ax2.scatter([cons_acum_real], [peso_real], color='blue', label='Peso real (input)', s=80)
    ax2.scatter([cons_acum_real], [peso_estimado], color='green', label='Peso estimado (input)', s=80, marker='x')
    ax2.set_xlabel('Cons_Acum')
    ax2.set_ylabel('Peso')
    ax2.set_title('Peso estimado vs real por Cons_Acum')
    ax2.legend()
    st.pyplot(fig2)



