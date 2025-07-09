import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from Optimizer import show_optimizer
from Blog import show_blog
from Contact import show_contact


# Configurações da página
st.set_page_config(
    page_title='Aurora Economica',
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Oculta menu lateral padrão do Streamlit
hide_default_sidebar = """
<style>
section[data-testid="stSidebarNav"] {
    display: none;
}
</style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

# Fundo bonito com imagem de fundo
page_bg_image = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url('https://images.unsplash.com/photo-1519120944692-1a8d8cfc107f?q=80&w=1336&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
background-size: cover;
}
[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}
[data-testid="stSidebar"] {
background-image: url('https://images.unsplash.com/photo-1750056661722-8381f9012079?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
background-size: cover;
}
</style>
"""

st.markdown(page_bg_image, unsafe_allow_html=True)

# Sidebar com menu principal
with st.sidebar:
    selected = option_menu(
        menu_title= None,
        options=["Home", "Portfolio Optimizer", "Contact"],
        icons=["house", "bar-chart", "envelope"],
        menu_icon="sunrise",
        default_index=0,
    )

# Página: HOME
if selected == "Home":
    logo = Image.open("aurora_logo_horizontal.png")
    st.image(logo, use_container_width=True)
   

# Página: Portfolio Optimizer
elif selected == "Portfolio Optimizer":
    show_optimizer()

# Página: Blog (com submenu horizontal)
# elif selected == "Machine Learning Predictor":
#     show_predictor()

# elif selected == "Blog":
#     show_blog()



# Página: Contato
elif selected == "Contact":
    show_contact()






