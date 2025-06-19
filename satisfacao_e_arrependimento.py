import streamlit as st

#st.set_page_config(page_title="Satisfação e Arrependimento", page_icon="🧠", layout="wide")

def show_post():

    st.title("Satisfação e Arrependimento")
    st.caption("Publicado em junho de 2025")

    st.markdown("---")

    st.write("""
    No seu biscoito chinês de 2 anos atrás, estava escrito os números 26 35 37 50 52. Desde então, você vai diariamente na lotérica jogar na quina com a esperança de que esses números irão lhe transformar em um sheik árabe da noite para o dia, mas ainda não ganhou nada. Um amigo, já desiludido com o poderio profético dos biscoitos orientais em outrora, sugere a troca da sequência de números na quina. O que você faria?
    """)

    st.write("""
    Racionalmente falando, a probabilidade de você ser premiado é a mesma para ambas as combinações numéricas. Agora imagine que você mudou para a série numérica sugerida pelo seu amigo e, logo no dia seguinte, por ironia do destino, o número do biscoito chinês foi sorteado. Qual seria seu sentimento?
    """)

    st.image("https://images.unsplash.com/photo-1745270917449-c2e2c5806586?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)

    st.write("""
    O arrependimento é a dor relacionada à percepção de que uma decisão, *ex post*, acaba sendo ruim. A defesa mais óbvia para o arrependimento é simplesmente não tomar nenhuma atitude. Dessa forma, é plausível assumir que o indivíduo toma decisões visando minimizar seus arrependimentos e maximizar sua satisfação.
    """)

    st.write("""
    Como exemplo, suponha agora que você tem interesse em fazer a compra de um ativo, mas não tem dinheiro em conta corrente para tal. Contudo, na sua carteira de investimentos, há uma ação X que rendeu 18% e outra Y que sofreu uma queda de 18%. Qual ação você se desfaria para comprar o novo ativo almejado?
    """)

    st.write("""
    Os pesquisadores Hersh Shefrin e Meir Statman, no artigo *The Disposition to Sell Winners Too Early and Ride Losers Too Long: Theory and Evidence*, mostraram que os investidores tendem a vender ativos que tenham aumentado de valor do que vender aqueles que tiveram um retorno negativo, baseando-se no preço de compra — descrevendo assim o **efeito disposição**.
    """)

    st.write("""
    Esta situação acontece porque o receio das pessoas ficarem expostas a possíveis perdas é maior do que a recompensa em relação a possíveis ganhos. Dessa maneira, é preferível garantir a satisfação ao vender um ativo com lucro do que assumir o arrependimento de um investimento com retorno negativo, permitindo que ele fique na sua carteira até que, pelo menos, fique no zero a zero (**efeito trying-to-break-even**). Em outras palavras, a dor do arrependimento é maior do que o prazer da satisfação.
    """)

    st.write("""
    É claro que há a possibilidade de o investidor decidir vender seus ativos vencedores e manter seus ativos perdedores por acreditarem que o retorno esperado do perdedor é maior em comparação ao vencedor de hoje, caracterizando uma atitude totalmente racional.
    """)

    st.write("""
    Por outro lado, se o retorno esperado para a ação perdedora não é maior do que para a ação vencedora; se os fundamentos já não se encaixam; se já não faz mais seu papel na carteira, então essa atitude é irracional e não justificável.
    """)

    st.write("""
    Para entender melhor esse dilema racional x irracional, o cientista Terrance Odean, em sua pesquisa *Are Investors Reluctant to Realize Their Losses?*, examinou 10 mil contas norte-americanas, entre 1987 a 1993. Os resultados mostraram que, em média, os investidores têm 50% a mais de probabilidade de vender uma ação com lucro do que uma ação com prejuízo.
    """)

    st.write("""
    Além disso, foi mostrado que as ações vencedoras vendidas apresentaram um retorno médio anual 3,4% maior em comparação às ações perdedoras mantidas. Dessa forma, desfazer-se das ações com lucro e manter os ativos negativos **não foi um bom negócio**.
    """)

    st.write("""
    É da natureza do ser humano evitar o arrependimento futuro de suas atitudes e buscar a satisfação. Mas, quando esses sentimentos são trazidos para as decisões de investimentos, deve-se tomar o dobro de cuidado. A satisfação do curto prazo pode ser o arrependimento do longo prazo.
    """)

    st.markdown("---")

    st.markdown("<div style='text-align: center;'><strong>Thiago Raymon da Costa – Unicamp</strong></div>", unsafe_allow_html=True)
