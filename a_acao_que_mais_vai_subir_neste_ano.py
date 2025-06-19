import streamlit as st

#st.set_page_config(page_title="A ação que mais vai subir neste ano", page_icon="📈", layout="wide")

def show_post():

    st.title("A ação que mais vai subir neste ano")
    st.caption("Publicado em junho de 2025")

    st.markdown("---")

    st.write("""
    Imagino que esse título tenha conquistado sua atenção. Não se culpe, a procura de ganhos rápidos e certos é o objetivo de qualquer indivíduo. Uma parte dos profissionais e gurus do mercado financeiro exploram essa ânsia e se autoproclamam “profetas da bolsa de valores”. 

    Não é difícil navegarmos na internet e depararmos com frases semelhantes ao do título desse texto, como exemplo: “saiba quais são os ativos que mais vão subir esse ano clicando aqui”, “minha carteira rendeu 340% nesse ano, saiba como”, “arraste para cima e conheça a nova Magalu”. São promessas de ganhos extraordinários em razão da alta capacidade de previsão de retornos.

    Afinal de contas, o quão bom o profissional em Finanças é em prever o futuro?
    """)

    st.write("""
    O pesquisador James Montier, na obra *Seven Sins of Fund Management: A Behavioural Critique*, analisou os dados da pesquisa sazonal do Federal Reserve Bank of Philadelphia, cujo o objetivo é medir o poder de previsão dos especialistas em Finanças e Economia em relação à inflação, curva de juros e o S&P 500 (índice da bolsa americana) entre 1993 e 2005.

    Os resultados evidenciam a baixa capacidade dos analistas em prever o futuro. Especificamente em relação à previsão dos juros futuros, a cada prognóstico de alta, os juros caiam em 55% das vezes. Em outras palavras, o ato de lançar uma moeda para o alto traria uma previsão mais fidedigna do que a de um profissional.
    """)

    st.write("""
    A seguir, está o gráfico que relaciona o palpite dos analistas (*forecast*) com o valor do juros futuro (10 years bond yield), representados pela linha pontilhada e pela linha contínua, respectivamente.
    """)

    st.image("Figuras/Figura_Acao_que_Mais_Vai_Subir_Neste_Ano.png", caption="Fonte: Seven Sins of Fund Management: A Behavioural Critique – James Montier", use_container_width=True)

    st.write("""
    O gráfico mostra que a linha que representa os palpites está sempre atrasada em relação à linha dos davdos reais. Essa mesma situação também foi encontrada por Montier nas previsões sobre a inflação e o S&P 500.

    Isso mostra claramente que os analistas são muito bons em nos dizer o que acabou de acontecer, mas de pouca utilidade para nos informar o que vai acontecer no futuro.
    """)

    st.write("""
    Então o que será que motiva um analista de mercado a continuar baseando suas decisões de investimento em futurologia? O sempre presente excesso de confiança, também conhecido como ego.

    O pesquisador Philip Tetlock estudou as previsões que experts em política mundial davam para possíveis eventos políticos. Os resultados mostraram que os especialistas que relataram ter 80% ou mais de confiança em suas previsões estavam realmente corretos em apenas 45% das vezes.

    Mais uma vez, o ato de lançar uma moeda para cima se torna tão eficiente quanto um profissional da área para prever o futuro.
    """)

    st.write("""
    Logo, podemos concordar com Tetlock e Montier na afirmação de que a expertise não traz poder de previsibilidade, mas sim melhora a capacidade de criar explicações para previsões que sejam tão convincentes, tanto para o cliente quanto para o próprio profissional.

    A solução, portanto, seria não focarmos nossos esforços em tentativas de previsões inúteis. Existem muitas estratégias que podem ser implementadas sem o uso de futurologia, sendo parte dos autores desses métodos ganhadores de Prêmio Nobel. Como exemplo, temos a otimização de portfólio de Harry Markowitz, entre diversas outras.
    """)

    st.write("""
    O resultado desse mito da previsibilidade no nosso mundo do mercado financeiro é uma série de “oportunidades de mercado” que não podemos perder de forma alguma.

    Enfim, quem não quer ser a próxima Betina?
    """)


    st.markdown("---")

    st.markdown("<div style='text-align: center;'><strong>Thiago Raymon da Costa – Unicamp</strong></div>", unsafe_allow_html=True)
