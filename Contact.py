import streamlit as st

def show_contact():
    

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("thiago.jpeg", width=200)

    with col2:
       
        st.subheader("Thiago Raymon da Costa")
        st.markdown("""
        PhD candidate in Economics at the State University of Campinas (Unicamp) and Visiting Researcher at Heidelberg University (Alfred Weber Institute for Economics), with a specialization in Finance and Quantitative Methods.

        My professional trajectory includes experience as a Volunteer Professor in Finance at the Department of Administration, Darcy Ribeiro Campus, University of Brasília; Financial Researcher at the Technological Development Support Center (CDT/UnB); Asset Allocation Analyst at GWX Investimentos; Cofounder and Investment Analyst at Andaluz Consultoria de Valores Mobiliários; and Chief Investment Officer (CIO) at Wise Asset Management.
        """)

        st.markdown("Email: [t271175@dac.unicamp.br](mailto:t271175@dac.unicamp.br)")
        st.markdown("LinkedIn: [linkedin.com/in/thiago-raymon-da-costa/](https://www.linkedin.com/in/thiago-raymon-da-costa/)")

        
