
import streamlit as st
import pandas as pd
import numpy as np
import os



# Mostrar logo decorativo centrado y semitransparente (compatible con Streamlit Cloud)
st.markdown(
    """
    <div style='display: flex; justify-content: center; margin-bottom: -60px; margin-top: 10px;'>
        <img src='logo_mejorado_2.jpg' width='180' style='opacity:0.15; filter: grayscale(50%);'/>
    </div>
    """,
    unsafe_allow_html=True
)



# Cargar coeficientes de los modelos
base_path = os.path.dirname(__file__)
df_dia_vs_cons = pd.read_csv(os.path.join(base_path, 'resultados_dia_vs_cons.csv'))
df_cons_vs_peso = pd.read_csv(os.path.join(base_path, 'resultados_cons_vs_peso.csv'))

# Obtener opciones únicas
razas = df_dia_vs_cons['RAZA'].unique()
sexos = df_dia_vs_cons['SEXO'].unique()

st.title('ALBATEQ S. A. Predicción Consumo Acumulado y Peso')

# Selección de parámetros
raza = st.selectbox('Seleccione la RAZA', razas, index=list(razas).index('ROSS') if 'ROSS' in razas else 0)
sexo = st.selectbox('Seleccione el SEXO', sexos, index=list(sexos).index('MIXTO') if 'MIXTO' in sexos else 0)
dia = st.number_input('Ingrese el Día', min_value=1, step=1)
cons_acum_real = st.number_input('Ingrese el Consumo Acumulado real en gramos', min_value=0.0, step=1.0)
peso_real = st.number_input('Ingrese el Peso real en gramos', min_value=0.0, step=1.0)

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
    st.write(f"Consumo Acumulado Estimado para Día {dia}: **{cons_acum_estimado:.2f}**")
    st.write(f"Consumo Acumulado Real Ingresado: **{cons_acum_real:.2f}**")
    diff_cons = cons_acum_real - cons_acum_estimado
    pct_cons = (diff_cons / cons_acum_estimado * 100) if cons_acum_estimado != 0 else 0
    st.write(f"Diferencia Consumo Acumulado (real - estimado): **{diff_cons:.2f}** ({pct_cons:.2f}%)")
    st.write('---')
    st.write(f"Peso Estimado para Consumo Acumulado {cons_acum_real}: **{peso_estimado:.2f}**")
    st.write(f"Peso Real ingresado: **{peso_real:.2f}**")
    diff_peso = peso_real - peso_estimado
    pct_peso = (diff_peso / peso_estimado * 100) if peso_estimado != 0 else 0
    st.write(f"Diferencia Peso (real - estimado): **{diff_peso:.2f}** ({pct_peso:.2f}%)")
    st.write('---')

    # Gráfica 1: Cons_Acum estimado vs real para el Día seleccionado
    import matplotlib.pyplot as plt
    fig1, ax1 = plt.subplots()
    dias = np.arange(1, 45)
    cons_acum_pred = intercepto1 + sum([coefs1[i] * dias**i for i in range(5)])
    ax1.plot(dias, cons_acum_pred, label='Consumo Acumulado Estimado', color='red')
    ax1.scatter([dia], [cons_acum_real], color='blue', label='Consumo Acumulado Real (input)', s=80)
    ax1.scatter([dia], [cons_acum_estimado], color='green', label='Consumo Acumulado Estimado (input)', s=80, marker='x')
    ax1.set_xlabel('Día')
    ax1.set_ylabel('Consumo Acumulado')
    ax1.set_title('Consumo Acumulado Estimado vs Real por Día')
    ax1.legend()
    st.pyplot(fig1)

    # Gráfica 2: Peso estimado vs real para el Cons_Acum ingresado
    fig2, ax2 = plt.subplots()
    cons_range = np.linspace(0, max(cons_acum_real, 4500), 100)
    peso_pred = intercepto2 + sum([coefs2[i] * cons_range**i for i in range(5)])
    ax2.plot(cons_range, peso_pred, label='Peso Estimado', color='orange')
    ax2.scatter([cons_acum_real], [peso_real], color='blue', label='Peso Real (input)', s=80)
    ax2.scatter([cons_acum_real], [peso_estimado], color='green', label='Peso estimado (input)', s=80, marker='x')
    ax2.set_xlabel('Consumo Acumulado')
    ax2.set_ylabel('Peso')
    ax2.set_title('Peso Estimado vs Real por Cons Acumulado')
    ax2.legend()
    st.pyplot(fig2)















