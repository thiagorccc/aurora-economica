import streamlit as st
from datetime import datetime
from PIL import Image

# Importa os posts como funções
from a_acao_que_mais_vai_subir_neste_ano import show_post as post_acao
from satisfacao_e_arrependimento import show_post as post_satisfacao
from afinal_o_que_e_um_bom_investimento import show_post as post_bom_investimento
from humor_calendario_e_seus_investimentos import show_post as post_humor

# Lista de posts
posts = [
    {
        "title": "A Ação que Mais Vai Subir Neste Ano",
        "date": "2024-10-05",
        "image": "https://images.unsplash.com/photo-1611967556157-d5c8830b5161?q=80&w=3070&auto=format&fit=crop",
        "func": post_acao
    },
    {
        "title": "Satisfação e Arrependimento",
        "date": "2024-10-20",
        "image": "https://images.unsplash.com/photo-1745270917449-c2e2c5806586?q=80&w=2940&auto=format&fit=crop",
        "func": post_satisfacao
    },
    {
        "title": "Afinal, O Que É Um Bom Investimento?",
        "date": "2024-10-20",
        "image": "https://images.unsplash.com/photo-1454923634634-bd1614719a7b?q=80&w=1470&auto=format&fit=crop",
        "func": post_bom_investimento
    },
    {
        "title": "Humor, Calendário e seus Investimentos",
        "date": "2024-10-20",
        "image": "https://images.unsplash.com/photo-1555861496-0666c8981751?q=80&w=1470&auto=format&fit=crop",
        "func": post_humor
    },
]

# Exibição principal
def show_blog():

    logo = Image.open("aurora_logo_vertical.png")
    st.image(logo, use_container_width=False, width=800)
    st.title("Aurora Blog")
    # st.markdown("Reflections and tools for finance, economics, and beyond.")
    st.markdown("---")

    if "selected_post" not in st.session_state:
        st.session_state["selected_post"] = None

    if st.session_state["selected_post"] is None:
        for post in posts:
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(post["image"], use_container_width=True)
                with cols[1]:
                    st.subheader(post["title"])
                    st.caption(f"Published on {datetime.strptime(post['date'], '%Y-%m-%d').strftime('%B %d, %Y')}")
                    if st.button(f"📖 Read full post", key=post["title"]):
                        st.session_state["selected_post"] = post["func"]
                        st.rerun()
                st.markdown("---")
    else:
        st.button("🔙 Back to all posts", on_click=lambda: st.session_state.update({"selected_post": None}))
        st.markdown("---")
        st.session_state["selected_post"]()
