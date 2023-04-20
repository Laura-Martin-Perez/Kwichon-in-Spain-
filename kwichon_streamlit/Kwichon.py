import streamlit as st


st.set_page_config(
    layout = 'wide',
    )

primary_clr ="#023d22"


st.markdown('''
    # Kwichon en España
    ''')

st.image('https://user-images.githubusercontent.com/113755985/229598369-47405110-7455-433a-afe0-997b46a52b91.png')


migraciones = st.checkbox("Migraciones")
if migraciones:
    st.image('Tabla_migraciones_interior.png')
    st.text('Datos extraídos del Instituto Nacional de Estadística (www.INE.es)')