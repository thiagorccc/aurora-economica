import streamlit as st

#st.set_page_config(page_title="Afinal, O Que É Um Bom Investimento?", page_icon="💰", layout="wide")

def show_post():

    st.title("Afinal, O Que É Um Bom Investimento?")
    st.caption("Publicado em junho de 2025")

    st.markdown("---")

    st.write("""
    Sinergia é a ação associada de dois ou mais órgãos. Construir uma equipe e procurar pessoas que tenham papeis e características distintas e que trabalhem harmoniosamente em prol de um mesmo objetivo é o segredo do sucesso de muitas empresas. 

    Acredite, a busca da sinergia também é o segredo do sucesso dos seus investimentos.
    """)

    st.write("""
    Afinal, o que é um bom investimento? Há setenta anos, o economista Harry Markowitz, vencedor do Prêmio Nobel, respondeu essa pergunta provando que o investidor deveria possuir investimentos que, combinados entre si, formassem uma carteira que oferecesse o maior retorno possível para o nível de risco que a pessoa deseja assumir — o famoso prêmio pelo risco. 

    Dessa maneira, o mais desejável seria pensar em sinergia, ou seja, ativos que tenham funções diferentes, mas que trabalhem com o único intuito de te deixar mais rico.
    """)

    st.write("""
    Para tanto, para identificarmos se uma ação, fundo ou título é um bom investimento, devemos ter em mente três características. Os primeiros desses parâmetros são a expectativa de retorno do ativo, juntamente com o grau de incerteza (risco) de que essa esperança de ganho futuro não se concretize. Para curiosos e entusiastas das Finanças, esse risco é calculado por uma medida chamada **desvio padrão**.
    """)

    st.image("https://images.unsplash.com/photo-1454923634634-bd1614719a7b?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", use_container_width=True)

    st.write("""
    A terceira característica importante nada mais é do que a maior arma para diminuir o risco do seu portfólio: a **correlação**. A maneira como cada investimento numa mesma carteira interage com os demais é medida pela correlação. 

    Assim como para construir uma equipe de sucesso, temos que propiciar sinergia aos investimentos. Devemos procurar ativos que tenham funções distintas, mas que se completem e trabalhem harmoniosamente. Em “financês”, entenda “funções distintas” como **baixa correlação**. Exemplos de pares com baixa correlação são: Ibovespa X Dólar, Empresas de Petróleo X Empresas de Aviação, entre outros.
    """)

    st.write("""
    Diminuir as oscilações da carteira significa levar em consideração a interação entre dois diferentes ativos. Infelizmente, os investidores costumam tratar cada investimento como uma conta mental diferente e tendem a ignorar a comunicação que existe entre as várias contas.
    """)

    st.write("""
    A obra *The Psychology of Investing* de John Nofsinger mostra uma pesquisa que pedia para 88 participantes — sendo eles alunos de graduação e pós-graduação em investimentos, além de participantes de clube de investimentos — classificarem determinados ativos de acordo com o nível de risco que cada um contribuiria à carteira.

    Entre esses papéis estavam commodities, títulos públicos e privados, imóveis, ações de mercados emergentes, ações da Europa e do Sudeste Asiático.
    """)

    st.write("""
    O resultado da pesquisa mostra que os títulos públicos e privados foram classificados em um primeiro grupo de investimentos que menos ofereciam risco. Em um segundo grupo de risco, estavam os imóveis e as commodities. Um último grupo foi formado pelas ações de mercados emergentes e ações da Europa e Sudeste Asiático.
    """)

    st.write("""
    Após essa classificação feita pelos participantes, o mesmo estudo mostrou que a inclusão de **commodities e bens imóveis diminuía o risco** das carteiras, assim como a inclusão das **ações de mercados emergentes**, que, analisadas isoladamente, são aquelas de maior risco.
    """)

    st.write("""
    Encarar a seleção de ativos como contas mentais, conforme a pesquisa mostrou, é semelhante a escolher seus investimentos como se estivesse em um bufê: *“Quero um pouco disso... Isso me parece bom... Me disseram que este é bom”*. 

    Em momentos de crise, esses erros podem custar caro. A busca pela **baixa correlação** pode trazer ao seu portfólio papéis que protejam seus rendimentos. 

    Para um bom investimento, **busque sinergia**.
    """)

    st.markdown("---")

    st.markdown("<div style='text-align: center;'><strong>Thiago Raymon da Costa – Unicamp</strong></div>", unsafe_allow_html=True)
