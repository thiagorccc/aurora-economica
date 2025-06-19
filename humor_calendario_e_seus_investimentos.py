import streamlit as st

#st.set_page_config(page_title="Humor, Calendário e seus Investimentos", page_icon="📆", layout="wide")

def show_post():

    st.title("Humor, Calendário e seus Investimentos")
    st.caption("Publicado em junho de 2025")

    st.markdown("---")

    st.write("""
    O que é anomalia? Em bom português, é o estado ou qualidade do que é irregular. Já em economês, é o que difere da racionalidade ou, mais precisamente, da noção de eficiência de mercado.

    De forma bem resumida, para o cientista Eugene Fama, um mercado eficiente é aquele que reflete todas as informações disponíveis de maneira racional nos preços. Um consenso é que tentamos, mas não somos sempre racionais. Por exemplo, até que ponto seu humor afeta suas decisões?
    """)

    st.write("""
    Um dia bonito com o céu azul, sem trânsito, depois de uma noite bem dormida muda a sua expectativa sobre a rentabilidade da bolsa de valores no final do ano? 

    A ciência mostra que isso é muito mais normal do que pensamos. David Hirshleifer e Tyler Shumway, na pesquisa *Good Day Sunshine: Stock Returns and the Weather*, examinaram o índice de preços de 26 mercados acionários durante 15 anos e os compararam com o clima dos seus respectivos países. 

    Os resultados mostraram uma forte relação entre o brilho do sol e os retornos das ações. Mais precisamente, os dias ensolarados tiveram um retorno anual de impressionantes **24% a mais** que os dias nublados.
    """)

    st.image("https://images.unsplash.com/photo-1555861496-0666c8981751?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)

    st.write("""
    É inegável que o sol é um fator fundamental para o nosso humor. Psicólogos mostram que a baixa quantidade de luz no dia, como acontece no inverno de países mais distantes da linha do Equador, pode resultar até mesmo em depressão — síndrome conhecida como **transtorno afetivo sazonal**.
    """)

    st.write("""
    Os cientistas Mark Kamstra, Lisa Kramer e Maurice Levi observaram como os retornos das ações de nove mercados (Estados Unidos, Suécia, Grã-Bretanha, Canadá, Nova Zelândia, Japão, Austrália e África do Sul) se comportam em períodos de dias mais curtos. 

    Os retornos são significativamente menores entre o outono e o dia 21 de dezembro, data que marca a noite mais longa do Hemisfério Norte.
    """)

    st.write("""
    Pode jogar uma pedra aquele que não gosta de uma sexta-feira. Afinal de contas, ainda tem dois dias para chegar a segunda-feira, que, convenhamos, não é o dia mais popular da semana. E, sim, isso também afeta os retornos das ações.
    """)

    st.write("""
    Uma série de estudos mostra o **efeito do calendário** na precificação do mercado acionário, revelando retornos superiores ou inferiores em determinadas épocas do ano ou da semana. Entre essas anomalias estão:

    - **Efeito Final de Semana**: retornos de segunda-feira significativamente menores do que os de sexta-feira.  
    - **Efeito Rally do Papai Noel**: retornos positivos entre os 5 últimos dias do ano e os 2 primeiros do ano seguinte.  
    - **Sell in May and Go Away**: quedas nos preços dos ativos no mês de maio.  
    """)

    st.write("""
    É fato que o humor afeta nossas decisões. Somos mais críticos e pessimistas ao estarmos de mal humor, e mais otimistas e permissivos com riscos quando estamos animados. As **anomalias de mercado** são reflexos desse emocional coletivo dos investidores.
    """)

    st.write("""
    É claro que não podemos esperar que todas as segundas-feiras sejam desastrosas e que em todos os dias de sol a bolsa suba. 

    Mas haverá dias em que o mercado irá, sim, "provar" essas anomalias. E saber disso é parte importante da consciência de um bom investidor.
    """)

    st.markdown("---")

    st.markdown("<div style='text-align: center;'><strong>Thiago Raymon da Costa – Unicamp</strong></div>", unsafe_allow_html=True)
