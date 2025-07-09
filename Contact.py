import streamlit as st


def show_contact():
 
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("thiago.png", width=200)

    with col2:
       
        st.header("Thiago Raymon da Costa")
        st.markdown("""
        **PhD Candidate in Economics** at the **State University of Campinas (Unicamp)** and **Visiting Researcher** at **Heidelberg University** (Alfred Weber Institute for Economics), with a specialization in **Finance and Quantitative Methods**.

        My professional background includes experience as **Chief Investment Officer (CIO)** at **Wise Asset Management**, **Co-Founder and Investment Analyst** at **Andaluz Consultoria de Valores Mobiliários**, **Asset Allocation Analyst** at **GWX Investimentos**, **Financial Researcher** at the **Technological Development Support Center (CDT/UnB)**, and **Volunteer Lecturer in Finance** at the **University of Brasília (UnB)**
        """)

        st.markdown("Email: [t271175@dac.unicamp.br](mailto:t271175@dac.unicamp.br)")
        st.markdown("LinkedIn: [linkedin.com/in/thiago-raymon-da-costa/](https://www.linkedin.com/in/thiago-raymon-da-costa/)")
        st.markdown("Google Scholar: [scholar.google.com/citations?user=tNDcTlUAAAAJ](https://scholar.google.com/citations?user=tNDcTlUAAAAJ&hl=pt-BR)")

        with open("curriculum.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(
            label="📄 Click here to download my CV (PDF)",
            data=PDFbyte,
            file_name="curriculum.pdf",
            mime="application/pdf")
            

        
        # st.markdown("---")
        # st.subheader("💼 Professional Experience")

        # st.markdown("""
        # - **Co-Founder & Investment Analyst**, Andaluz Financial Advisory (2020–2025)  
        # Defined strategies for individual portfolio management and company valuation.  
        # **AUM:** USD 25.5 million

        # - **Chief Investment Officer (CIO)**, Wise Asset Management (2021–2023)  
        # Responsible for managing investment funds in equities, fixed income, and commodities, and overseeing the risk management division.  
        # **AUM:** USD 51 million

        # - **Asset Allocation Analyst**, GWX Investimentos (2018–2020)  
        # Responsible for strategy definition for private portfolios and equity valuation.  
        # **AUM:** USD 85 million

        # - **Financial Consultant**, Technological Development Support Center – UnB (2013–2014)  
        # Delivered financial planning and startup valuation, supported business plan development, and assisted investor meetings.
        #     """)

        # st.markdown("---")
        # st.subheader("📚 Publications")

        # st.markdown("""
        # - *Portfolio Optimization with Asset Pre-Selection Using Machine Learning: Evidence for Emerging Market Indices*, **International Journal of Business and Emerging Markets** (In press)

        # - *The Profitability of Moving Average Trading Rules in BRICS and Emerging Stock Markets*, **North American Journal of Economics and Finance**, 2016

        # - *Trading System Based on the Use of Technical Analysis: A Computational Experiment*, **Journal of Behavioral and Experimental Finance**, 2015

        # - *Trading System Baseado no MACD: Uma Experimentação Computacional*, **RACEF – FUNDACE**, 2013

        # - *Modelagem e Simulação de um Mercado Acionário Artificial com Agentes Heterogêneos*, **EnANPAD**, 2016
        #     """)

        # st.markdown("---")
        # st.subheader("🎓 Teaching & Volunteer Experience")

        # st.markdown("""
        # - **Tutor in the Financial Market Group**, Unicamp (2024–Present)  
        # Course: *Financial Theory*

        # - **Volunteer Lecturer**, IDP (2022–2023)  
        # Course: *Data Science*

        # - **Volunteer Lecturer**, University of Brasília – UnB (2015–2017)  
        # Course: *Financial Theory*
        #     """)

        # st.markdown("---")
        # st.subheader("🛠️ Skills & Certifications")

        # st.markdown("""
        # - **Languages**:  
        # Native: Portuguese  
        # Fluent: English, Spanish  
        # Basic: German

        # - **Certifications**:  
        # CGA – Brazilian Portfolio Management License  
        # CNPI – Brazilian Investment Analyst Certification  
        # CGE – Structured Fund Manager Certification

        # - **Technical Skills**:  
        # Python, R, LaTeX, VBA, Microsoft Office
        #     """)

        


        
