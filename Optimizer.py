import streamlit as st
from PIL import Image
import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import plotly.graph_objects as go
from pypfopt import risk_models, expected_returns, EfficientFrontier
import empyrical 
import calendar
from scipy.optimize import minimize
import time
import plotly.figure_factory as ff


def show_optimizer():

    try:

        # --- CONFIG PAGE ---
        #st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

        # --- LOGO ---
        logo = Image.open("aurora_logo_vertical.png")
        st.image(logo, use_container_width=False, width=800)


        # --- TABS ---
        tab1, tab2 = st.tabs(["Optimization", "Compare with Current Portfolio"])

        # === SYMBOLS LIST ===
        # Benchmarks disponíveis
        benchmarks = {
                "Ibovespa (Brazil)": "^BVSP",
                "S&P 500 (SPY)": "SPY",
                "S&P 500 Index (^GSPC)": "^GSPC",
                "Dow Jones (^DJI)": "^DJI",
                "Nasdaq 100 (^NDX)": "^NDX",
                "Russell 2000 (^RUT)": "^RUT",
                "EURO STOXX 50": "^STOXX50E",
                "STOXX Europe 600": "^STOXX",
                "DAX (Germany)": "^GDAXI",
                "CAC 40 (France)": "^FCHI",
                "FTSE MIB (Italy)": "FTSEMIB.MI",
                "IBEX 35 (Spain)": "^IBEX",
                "FTSE 100 (UK)": "^FTSE",
                "Euro Corporate Bonds (ETF - IEAC.L)": "IEAC.L",
                "U.S. Treasury Bill ETF (Cash Equivalent)": "BIL" ,
                
            }  
        
        benchmarks_anbima = {
                "CDI index": "CDI",
                "IMA-B index": "IMA-B"
            }  
        
        #benchmarks_total = benchmarks | benchmarks_anbima

        symbol_real = {
            # Grandes blue‑chips (Ibovespa e top 10)
            "VALE3.SA": "Vale ON",
            "PETR4.SA": "Petrobras PN",
            "ITUB4.SA": "Itaú Unibanco PN",
            "B3SA3.SA": "B3 ON",
            "BBAS3.SA": "Banco do Brasil ON",
            "BBDC3.SA": "Bradesco ON",
            "ABEV3.SA": "Ambev ON",
            "WEGE3.SA": "WEG ON",
            "PETR3.SA": "Petrobras ON",
            "MGLU3.SA": "Magazine Luiza ON",
            # Outros destaques top ~100 do IBrX‑100
            "SUZB3.SA": "Suzano ON",
            "GGBR4.SA": "Gerdau PN",
            "CSNA3.SA": "CSN ON",
            "BRAP4.SA": "Bradespar PN",
            "BRKM5.SA": "Braskem PNA",
            "BBDC4.SA": "Bradesco PN",
            "BBSE3.SA": "BB Seguridade ON",
            "BPAC11.SA": "BTG Pactual Units",
            "ITSA4.SA": "Itaúsa PN",
            "RADL3.SA": "Raia Drogasil ON",
            "LREN3.SA": "Lojas Renner ON",
            "RENT3.SA": "Localiza ON",
            "GOLL4.SA": "Gol PN",
            "CYRE3.SA": "Cyrela ON",
            "COGN3.SA": "Cogna ON",
            "TIMS3.SA": "Tim ON",
            "RDOR3.SA": "Rede D’Or ON",
            "CPFE3.SA": "CPFL Energia ON",
            "RAIL3.SA": "Rumo ON",
            "MRVE3.SA": "MRV ON",
            "JBSS3.SA": "JBS ON",
            "QUAL3.SA": "Qualicorp ON",
            "KLBN11.SA": "Klabin Units",
            "ENGI11.SA": "Energisa Units",
            "ELET3.SA": "Eletrobras ON",
            "ELET6.SA": "Eletrobras PNB",
            "ENBR3.SA": "EDP Brasil ON",
            "EGIE3.SA": "Engie Brasil ON",
            "SLCE3.SA": "SLC Agrícola ON",
            "TAEE11.SA": "Taesa Units",
            "AZUL4.SA": "Azul PN",
            "BEEF3.SA": "Minerva ON",
            "NTCO3.SA": "Natura ON",
            "VIVT3.SA": "Telefônica Brasil ON",
            "BRFS3.SA": "BRF ON",
            "MULT3.SA": "Multiplan ON",
            "MOGU3.SA": "Movida ON",
            "PRIO3.SA": "PetroRio ON",
            "CPLE6.SA": "Copel PNB",
            "CGAS5.SA": "Comgás PNA",
            "HYPE3.SA": "Hypera ON",
            "CSAN3.SA": "Cosan ON",
            "SMTO3.SA": "Simpar ON",
            "ENAT3.SA": "Enauta ON",
            "LWSA3.SA": "Lojas Quero-Quero ON",
            "BPAN4.SA": "Banrisul PN",
            "ALPA4.SA": "Alpargatas PN",
            "BRML3.SA": "BR Malls ON",
            "CAML3.SA": "Camil ON",
            "EMBR3.SA": "Embraer ON",
            "CVCB3.SA": "CVC ON",
            "VVAR3.SA": "Via ON",
            "LAME4.SA": "Lame4 PN",
            "EZTC3.SA": "EZTEC ON",
            "LOGG3.SA": "Log Commercial Properties ON",
            "EQTL3.SA": "Equatorial ON",
            "FLRY3.SA": "Fleury ON",
            "IRBR3.SA": "IRB Brasil ON",
            "SMTO3.SA": "São Martinho ON",
            "SBSP3.SA": "Sabesp ON",
            "TOTS3.SA": "Totvs ON",
            "UGPA3.SA": "Ultrapar ON",
            "USIM5.SA": "Usiminas PNA",
            "VIVT4.SA": "Telefônica Brasil PN",
            "PCAR4.SA": "Pão de Açúcar ON",
            "ARZZ3.SA": "Arezzo ON",
            "ASAI3.SA": "Assaí Atacadista ON",
            "CRFB3.SA": "Carrefour Brasil ON",
            "MRFG3.SA": "Marfrig ON",
            "MOVI3.SA": "Movida ON",
            "PETZ3.SA": "Petz ON",
            "POSI3.SA": "Positivo Tecnologia ON",
            "RECV3.SA": "PetroRecôncavo ON",
            "RRRP3.SA": "3R Petroleum ON",
            "SOMA3.SA": "Grupo Soma ON",
            "SYNE3.SA": "Syn Prop & Tech ON",
            "TRPL4.SA": "Transmissão Paulista PN",
            "UNIP6.SA": "Unipar PNB",
            "CASH3.SA": "Méliuz ON",
            "AERI3.SA": "Aeris ON",    "AMER3.SA": "Americanas ON",
            "ALSO3.SA": "Aliansce Sonae ON",
            "B3SA3.SA": "B3 ON",  
            "BMGB4.SA": "Banco BMG PN",
            "CEAB3.SA": "C&A ON",
            "DXCO3.SA": "Dexco ON",
            "IGTI11.SA": "Iguatemi Units",
            "JHSF3.SA": "JHSF ON",
            "LIGT3.SA": "Light ON",
            "LOGN3.SA": "Log-In Logística ON",
            "MEAL3.SA": "IMC - International Meal Company ON",
            "NGRD3.SA": "Neogrid ON",
            "PNVL3.SA": "Panvel ON",
            "SAPR11.SA": "Sanepar Units",
            "SLED4.SA": "Saraiva Livreiros PN",
            "AURE3.SA": "Auren Energia ON",
            "CXSE3.SA": "Caixa Seguridade Participações ON",
            "HBSA3.SA": "Hidrovias do Brasil ON",
            "ISAE4.SA": "ISA Energia Brasil PN",
            "SIMH3.SA": "Simpar ON",
            "TUPY3.SA": "Tupy ON",
            "OIBR3.SA": "Oi ON",

                # Índices de Ações Brasil
            "BOVA11.SA": "iShares Ibovespa ETF (Equities)",
            "BRAX11.SA": "iShares IBrX-100 ETF (Equities)",
            "SMAL11.SA": "iShares Small Cap ETF (Equities)",
            "ISUS11.SA": "iShares S&P 500 USD Hedge (Equities)",
            "IVVB11.SA": "iShares S&P 500 ETF (Equities)",

            # Setoriais
            "FIND11.SA": "iShares Financials ETF (Equities)",
            "MATB11.SA": "iShares Basic Materials ETF (Equities)",
            "IMOB11.SA": "iShares Real Estate ETF (Equities)",

            # ESG / Temáticos
            "ESGB11.SA": "iShares ESG Brasil ETF (Equities)",
            "GOVE11.SA": "Trend Governance ESG ETF (Equities)",

            # Fundos internacionais
            "XINA11.SA": "Trend China ETF (Equities)",
            "EURP11.SA": "Trend Europe ETF (Equities)",
            "JAPN11.SA": "Trend Japan ETF (Equities)",
            "ASIA11.SA": "Trend Asia ETF (Equities)",
            "ETHE11.SA": "Hashdex Ethereum ETF (Crypto)",
            "HASH11.SA": "Hashdex Nasdaq Crypto Index ETF (Crypto)",
            "BITH11.SA": "Bitcoin Futures ETF – Hashdex (Crypto)",

            # Renda fixa e proteção
            "FIXA11.SA": "Trend Renda Fixa Imediata ETF (Fixed Income)",
            "IMAB11.SA": "iShares Índice de Títulos Públicos (Fixed Income)",
            "IRFM11.SA": "iShares Índice de Renda Fixa de Mercado (Fixed Income)",
            "TIPB11.SA": "Trend Inflação Longa ETF (Fixed Income)",
            "GOLD11.SA": "Trend Ouro (Commodities)",

            # Imobiliário (IFIX)
            "XFIX11.SA": "Trend IFIX ETF (REITs)"}
                
        symbol_dolar = {
                "VOO": "Vanguard S&P 500 ETF (Equities)",
                "QQQ": "Invesco QQQ Trust (Equities)",
                "IVV": "S&P 500 Core ETF (Equities)",
                "DHS": "US High Dividend ETF (Equities)",
                "AOK": "Conservative Allocation ETF (Multi-Asset)",
                "QQQM": "NASDAQ 100 ETF (Equities)",
                "EEMA": "EM Asia ETF (Equities)",
                "VEA": "Developed Markets ETF (Equities)",
                "VIG": "Dividend Appreciation ETF (Equities)",
                "VYM": "High Dividend Yield ETF (Equities)",
                "SPY": "S&P 500 (Equities)",
                "VTI": "Vanguard Total Stock Market ETF (Equities)",
                "VT": "Vanguard Total World Stock ETF (Equities)",
                "VO": "Vanguard Mid-Cap ETF (Equities)",
                "VB": "Vanguard Small-Cap ETF (Equities)",
                "IWM": "iShares Russell 2000 ETF (Equities)",
                "DIA": "SPDR Dow Jones Industrial Average ETF (Equities)",
                "SPLG": "SPDR Portfolio S&P 500 ETF (Equities)",
                "EFA": "MSCI EAFE Developed Markets ETF (Equities)",
                "EWZ": "iShares MSCI Brazil ETF (Equities)",
                "FXI": "iShares China Large-Cap ETF (Equities)",
                "EWJ": "iShares MSCI Japan ETF (Equities)",
                "INDA": "iShares MSCI India ETF (Equities)",
                "EWW": "iShares MSCI Mexico ETF (Equities)",
                "AFK": "VanEck Africa Index ETF (Equities)",
                "FM": "iShares Frontier and Select EM ETF (Equities)",
                "FRN": "Invesco Frontier Markets ETF (Equities)",
                "ILF": "iShares Latin America 40 ETF (Equities)",
                "ECH": "iShares MSCI Chile ETF (Equities)",
                "EPU": "iShares MSCI Peru ETF (Equities)",
                "GXG": "Global X MSCI Colombia ETF (Equities)",
                "VNM": "VanEck Vietnam ETF (Equities)",
                "THD": "iShares MSCI Thailand ETF (Equities)",
                "EPHE": "iShares MSCI Philippines ETF (Equities)",
                "EIDO": "iShares MSCI Indonesia ETF (Equities)",
                "GULF": "WisdomTree Middle East Dividend ETF (Equities)",
                "MES": "Market Vectors Gulf States ETF (Equities)",
                "VTV": "Vanguard Value ETF (Equities)",
                "VUG": "Vanguard Growth ETF (Equities)",
                "VOE": "Vanguard Mid-Cap Value ETF (Equities)",
                "VBR": "Vanguard Small-Cap Value ETF (Equities)",
                "IVW": "iShares S&P 500 Growth ETF (Equities)",
                "IVE": "iShares S&P 500 Value ETF (Equities)",
                "IJH": "iShares Core S&P Mid-Cap ETF (Equities)",
                "IJR": "iShares Core S&P Small-Cap ETF (Equities)",
                "IUSG": "iShares Core S&P U.S. Growth ETF (Equities)",
                "IUSV": "iShares Core S&P U.S. Value ETF (Equities)",
                "ACWI": "iShares MSCI ACWI ETF (Equities)",
                "MTUM": "iShares MSCI USA Momentum Factor ETF (Equities)",
                "USMV": "iShares MSCI USA Min Vol Factor ETF (Equities)",
                "QUAL": "iShares MSCI USA Quality Factor ETF (Equities)",
                "VLUE": "iShares MSCI USA Value Factor ETF (Equities)",
                "EEM": "iShares MSCI Emerging Markets ETF (Equities)",
                "SCHP": "US TIPS ETF (Fixed Income)",
                "TLT": "20+ Year Treasury Bond ETF (Fixed Income)",
                "BNDX": "Int'l Bond ETF (Fixed Income)",
                "IEF": "7-10Y Treasury Bond (Fixed Income)",
                "GOVT": "US Government Bond (Fixed Income)",
                "LQD": "Investment Grade Corporate Bond (Fixed Income)",
                "USHY": "US High Yield Bond (Fixed Income)",
                "USFR": "Floating Rate Treasury (Fixed Income)",
                "SHY": "1-3 Year Treasury Bond ETF (Fixed Income)",
                "BND": "Total Bond Market ETF (Fixed Income)",
                "TIP": "TIPS Bond ETF (Fixed Income)",
                "HYG": "High Yield Corporate Bond ETF (Fixed Income)",
                "MUB": "National Muni Bond ETF (Fixed Income)",
                "EMB": "Emerging Markets USD Bond ETF (Fixed Income)",
                "VCIT": "Intermediate-Term Corporate Bond ETF (Fixed Income)",
                "VCSH": "Short-Term Corporate Bond ETF (Fixed Income)",
                "TFI": "SPDR Nuveen Municipal Bond ETF (Fixed Income)",
                "HYD": "High-Yield Muni Bond ETF (Fixed Income)",
                "SPSB": "Short-Term Investment Grade Bond ETF (Fixed Income)",
                "BSV": "Short-Term Bond ETF (Fixed Income)",
                "IGOV": "International Treasury Bond ETF (Fixed Income)",
                "BWX": "International Govt Bond ETF ex-US (Fixed Income)",
                "SGOV": "1-3 Month US Treasury ETF (Fixed Income)",
                "GLD": "Gold ETF (Commodities)",
                "GDX": "Gold Miners ETF (Commodities)",
                "IAU": "iShares Gold Trust (Commodities)",
                "SLV": "Silver Trust (Commodities)",
                "USO": "US Oil Fund (Commodities)",
                "PDBC": "Diversified Commodities (Commodities)",
                "DBC": "Commodities Index Tracking ETF (Commodities)",
                "CPER": "US Copper Index Fund (Commodities)",
                "DBA": "Agriculture Fund ETF (Commodities)",
                "TQQQ": "UltraPro QQQ (Leveraged/Inverse)",
                "SQQQ": "UltraPro Short QQQ (Leveraged/Inverse)",
                "SPXS": "UltraShort S&P500 (Leveraged/Inverse)",
                "UVXY": "VIX Short-Term Futures (Leveraged/Inverse)",
                "UPRO": "UltraPro S&P 500 (Leveraged/Inverse)",
                "SDOW": "UltraPro Short Dow30 (Leveraged/Inverse)",
                "TZA": "Small Cap Bear 3x Shares (Leveraged/Inverse)",
                "FNGU": "FANG+ 3X Leveraged ETN (Leveraged/Inverse)",
                "DOC": "Physicians Realty (REITs)",
                "FRT": "Federal Realty (REITs)",
                "SLG": "SL Green Realty (REITs)",
                "O": "Realty Income (REITs)",
                "VNQ": "Vanguard Real Estate ETF (REITs)",
                "SCHH": "Schwab U.S. REIT ETF (REITs)",
                "IYR": "iShares U.S. Real Estate ETF (REITs)",
                "SOXX": "Semiconductor ETF (Thematic)",
                "SMH": "VanEck Semiconductor ETF (Thematic)",
                "XLK": "Technology Sector ETF (Thematic)",
                "XLV": "Healthcare Sector ETF (Thematic)",
                "XLY": "Consumer Discretionary ETF (Thematic)",
                "XHB": "Homebuilders ETF (Thematic)",
                "XAR": "Aerospace & Defense ETF (Thematic)",
                "REZ": "Residential & Healthcare REIT ETF (Thematic)",
                "ARKK": "ARK Innovation ETF (Thematic)",
                "QYLD": "Nasdaq-100 Covered Call (Thematic)",
                "SCHD": "US Dividend Equity (Thematic)",
                "XLF": "Financials Sector (Thematic)",
                "XLI": "Industrials Sector (Thematic)",
                "XLE": "Energy Sector (Thematic)",
                "XLU": "Utilities Sector (Thematic)",
                "XLP": "Consumer Staples (Thematic)",
                "XBI": "S&P Biotech ETF (Thematic)",
                "BITO": "ProShares Bitcoin Strategy ETF (Crypto)",
                "GBTC": "Grayscale Bitcoin Trust (Crypto)",
                "ETHE": "Grayscale Ethereum Trust (Crypto)",
                "IBIT": "iShares Bitcoin Trust (Crypto)",
                "FBTC": "Fidelity Wise Origin Bitcoin Fund (Crypto)",
                "ARKB": "ARK 21Shares Bitcoin ETF (Crypto)",
                "FXE": "Invesco CurrencyShares Euro Trust (Currency)",
                "FXY": "Invesco CurrencyShares Japanese Yen Trust (Currency)",
                "FXF": "Invesco CurrencyShares Swiss Franc Trust (Currency)",
                "FXB": "Invesco CurrencyShares British Pound Trust (Currency)",
                "FXC": "Invesco CurrencyShares Canadian Dollar Trust (Currency)",
                "FXA": "Invesco CurrencyShares Australian Dollar Trust (Currency)",
                "CYB": "WisdomTree Chinese Yuan Strategy Fund (Currency)",
                "UUP": "US Dollar Index Bullish ETF (Currency)",
                "UDN": "US Dollar Index Bearish ETF (Currency)",
                "DBV": "Invesco DB G10 Currency Harvest Fund (Currency)",
                "VXX": "S&P 500 VIX Short-Term Futures ETN (Volatility)",
                "AAPL": "Apple Inc.",
                "MSFT": "Microsoft Corp.",
                "NVDA": "Nvidia Corp.",
                "GOOGL": "Alphabet Inc. (Class A)",
                "AMZN": "Amazon.com Inc.",
                "JPM": "JPMorgan Chase & Co.",
                "PG": "Procter & Gamble Co.",
                "UNH": "UnitedHealth Group Inc.",
                "V": "Visa Inc.",
                "MA": "Mastercard Inc.",
                "HD": "Home Depot, Inc.",
                "DIS": "Walt Disney Co.",
                "INTC": "Intel Corp.",
                "CSCO": "Cisco Systems, Inc.",
                "XOM": "Exxon Mobil Corp.",
                "CVX": "Chevron Corp.",
                "KO": "Coca‑Cola Co.",
                "PEP": "PepsiCo, Inc.",
                "VZ": "Verizon Communications",
                # Mega‑caps adicionais
                "TSM": "Taiwan Semiconductor (ADR)",
                "ADBE": "Adobe Inc.",
                "ABBV": "AbbVie Inc.",
                "COST": "Costco Wholesale Corp.",
                "BAC": "Bank of America Corp.",
                "CRM": "Salesforce Inc.",
                "MCD": "McDonald's Corp.",
                "ORCL": "Oracle Corp.",
                "TXN": "Texas Instruments Inc.",
                "QCOM": "Qualcomm Inc.",
                "BA": "Boeing Co.",
                "GS": "Goldman Sachs Group Inc.",
                "GE": "General Electric Co.",
                "NKE": "Nike Inc.",
                "SBUX": "Starbucks Corp.",
                "AMD": "Advanced Micro Devices Inc.",
                "INTU": "Intuit Inc.",
                "ISRG": "Intuitive Surgical Inc.",
                "NOW": "ServiceNow Inc.",
                "AMAT": "Applied Materials Inc.",
                "BKNG": "Booking Holdings Inc.",
                "MDLZ": "Mondelez International Inc.",
                "ADI": "Analog Devices Inc.",
                "VRTX": "Vertex Pharmaceuticals Inc.",
                "REGN": "Regeneron Pharmaceuticals Inc.",
                "FDX": "FedEx Corp.",
                "MRNA": "Moderna Inc.",
                "LRCX": "Lam Research Corp.",
                "MO": "Altria Group Inc.",
                "DE": "Deere & Co.",
                "T": "AT&T Inc.",
                "F": "Ford Motor Co.",
                "GM": "General Motors Co.",
                "WBA": "Walgreens Boots Alliance Inc.",
                "MET": "MetLife Inc.",
                "PNC": "PNC Financial Services Group Inc.",
                "USB": "U.S. Bancorp",
                "SO": "Southern Co.",
                "D": "Dominion Energy Inc.",
                "AEP": "American Electric Power Co.",
                "EOG": "EOG Resources Inc.",
                "PSX": "Phillips 66",
                "MPC": "Marathon Petroleum Corp.",
                "PLD": "Prologis Inc.",
                "SPGI": "S&P Global Inc.",
                "ICE": "Intercontinental Exchange Inc.",
                "TGT": "Target Corp.",
                "LOW": "Lowe's Companies Inc.",
                "BK": "Bank of New York Mellon Corp.",
                "CTAS": "Cintas Corp.",
                "AIG": "American International Group Inc.",
                "C": "Citigroup Inc.",
                "ALL": "Allstate Corp.",
                "MS": "Morgan Stanley",
                "SCHW": "Charles Schwab Corp.",
                "EBAY": "eBay Inc.",
                "ZM": "Zoom Video Communications Inc.",
                "PYPL": "PayPal Holdings Inc.",
                "ROKU": "Roku Inc.",
                "SNOW": "Snowflake Inc.",
                "ABNB": "Airbnb Inc.",
                "LYFT": "Lyft Inc.",
                "UBER": "Uber Technologies Inc.",
                "RBLX": "Roblox Corp.",
                "BIDU": "Baidu Inc. (ADR)",
                "JD": "JD.com Inc. (ADR)",
                "PDD": "PDD Holdings Inc. (ADR)",
                "BABA": "Alibaba Group Holding Ltd. (ADR)",
                "ADP": "Automatic Data Processing Inc.",
                "MNST": "Monster Beverage Corp.",
                "AFL": "Aflac Inc.",
                "CME": "CME Group Inc.",
                "EL": "Estée Lauder Companies Inc.",
                "HCA": "HCA Healthcare Inc.",
                "BIIB": "Biogen Inc.",
                "AZO": "AutoZone Inc.",
                "ORLY": "O'Reilly Automotive Inc.",
                "TT": "Trane Technologies plc",
                "FTNT": "Fortinet Inc.",
                "CDNS": "Cadence Design Systems Inc.",
                "ANET": "Arista Networks Inc.",
                "ENPH": "Enphase Energy Inc.",
                "FSLR": "First Solar Inc.",
                "TTD": "The Trade Desk Inc.",
                "ZS": "Zscaler Inc.",
                "CRWD": "CrowdStrike Holdings Inc.",
                "DDOG": "Datadog Inc.",
                "OKTA": "Okta Inc.",
                "MDB": "MongoDB Inc.",
                "TEAM": "Atlassian Corp.",
                "DOCU": "DocuSign Inc.",
                "ROST": "Ross Stores Inc.",
                "DLTR": "Dollar Tree Inc.",
                "DG": "Dollar General Corp.",
                "WBD": "Warner Bros. Discovery Inc.",
                "PARA": "Paramount Global",
                "FOXA": "Fox Corp. Class A",
                "LCID": "Lucid Group Inc.",
                "RIVN": "Rivian Automotive Inc.",
                "NKLA": "Nikola Corp.",
                "XOM": "Exxon Mobil Corp.",
                "CVX": "Chevron Corp.",
                "COP": "ConocoPhillips",
                "HAL": "Halliburton Co.",
                "SLB": "Schlumberger NV",
                "MRO": "Marathon Oil Corp.",
                "APA": "APA Corp.",
                "OXY": "Occidental Petroleum Corp.",
                "ADM": "Archer-Daniels-Midland Co.",
                "KHC": "Kraft Heinz Co.",
                "KR": "Kroger Co.",
                "PEP": "PepsiCo Inc.",
                "KO": "Coca-Cola Co.",
                "CL": "Colgate-Palmolive Co.",
                "PG": "Procter & Gamble Co.",
                "MDT": "Medtronic plc",
                "SYK": "Stryker Corp.",
                "BSX": "Boston Scientific Corp.",
                "BDX": "Becton Dickinson & Co.",
                "ZBH": "Zimmer Biomet Holdings Inc."
                }
        
            
        symbol_euro = {
                "IWDA.AS": "iShares MSCI World (Equities)",
                "EIMI.L": "iShares Emerging Markets IMI (Equities)",
                "IMEU.L": "iShares MSCI Europe (Equities)",
                "MVOL.L": "MSCI Europe Min Volatility (Equities)",
                "EQQQ.DE": "NASDAQ 100 UCITS (Equities)",
                "EQQQ.L": "NASDAQ 100 UCITS GBP (Equities)",
                "IWMO.L": "MSCI World Minimum Volatility (Equities)",
                "SPY5.DE": "SPDR S&P 500 UCITS (Equities)",
                "XCHA.DE": "MSCI China A (Equities)",
                "XFFE.MI": "FTSE MIB (Equities)",
                "IBGS.L": "UK Gilts All Stocks (Fixed Income)",
                "IEAC.L": "Euro Corporate Bonds (Fixed Income)",
                "AGGH.L": "Global Aggregate Bond (Fixed Income)",
                "EXX6.DE": "iShares Euro Government Bond 1-3yr (Fixed Income)",
                "IBCX.DE": "iShares Euro Government Bond 3-5yr (Fixed Income)",
                "IBGX.DE": "iShares Euro Government Bond 7-10yr (Fixed Income)",
                "IBCY.DE": "iShares Euro Government Bond 15-30yr (Fixed Income)",
                "SXR8.DE": "iShares Euro Investment Grade Corp Bond (Fixed Income)",
                "EUNA.DE": "Lyxor Euro Government Bond 10Y DR ETF (Fixed Income)",
                "IBCI.DE": "iShares Euro Government Inflation-Linked Bond ETF (Fixed Income)",
                "AGGE.DE": "iShares Global Aggregate Bond EUR Hedged (Fixed Income)",
                "BTCE.DE": "21Shares Bitcoin ETP (Crypto)",
                "ABTC.DE": "ETC Group Physical Bitcoin (Crypto)",
                "VBTC.AS": "VanEck Bitcoin ETN (Crypto)",
                "BTCE.AS": "BTCetc Bitcoin Exchange Traded Crypto (Crypto)",
                "XDWD.DE": "Xtrackers MSCI World UCITS ETF 1C (Equities)",
                "XDWD.L": "Xtrackers MSCI World UCITS ETF 1C (Equities, LSE)",
                "XMME.DE": "Xtrackers MSCI Emerging Markets UCITS ETF 1C (Equities)",
                "XMME.L": "Xtrackers MSCI Emerging Markets UCITS ETF 1C (Equities, LSE)",
                "XDWT.DE": "Xtrackers MSCI World Information Technology UCITS ETF (Thematic)",
                "XDEQ.DE": "Xtrackers MSCI World Quality UCITS ETF",
                "XZEM.DE": "Xtrackers MSCI Emerging Markets ESG UCITS ETF",
                "XWLD.L": "Xtrackers MSCI Europe UCITS ETF 1C",
                "NEAR": "iShares Short Duration Bond Active ETF (Fixed Income)",
                "IGSB": "iShares 1–5 Year Investment Grade Corporate Bond ETF (Fixed Income)",
                "RSP": "Invesco S&P 500 Equal Weight ETF (Equities)",
                "XAR": "SPDR S&P Aerospace & Defense ETF (Equities)",
                
                # Europa fatores & estilo
                "DBX0FK.DE": "Xtrackers MSCI Europe Value UCITS ETF",
                "DBXA.DE": "Xtrackers MSCI Europe UCITS ETF 1C",
                "DBEU.DE": "Xtrackers MSCI Europe Hedged Equity ETF",

                # Setoriais europeus
                "DBXD.DE": "Xtrackers DAX UCITS ETF 1C",
                "FEZ.L": "SPDR EURO STOXX 50 UCITS ETF",
                "ISF.L": "iShares Core FTSE 100 UCITS ETF",
                "EQS1.DE": "iShares Core DAX UCITS ETF",

                # Temáticos / fatores defensivos
                "DFND.L": "iShares STOXX Europe 600 ETF",
                "DBXS.DE": "Xtrackers Short DAX x2 Daily Swap ETF",
                "DBX0B6.DE": "Xtrackers S&P 500 2x Inverse UCITS ETF",
                "DBX0V7.DE": "Xtrackers MSCI Europe ESG ETF",

                # Imobiliário europeu
                "EPRA.L": "iShares EPRA NAREIT Europe UCITS ETF",
                "WCHG.DE": "iShares European Property Yield UCITS ETF",

                # Defensivos/dividendos
                "IEUR.DE": "iShares Core MSCI Europe Dividend UCITS",
                "BNK.DE": "Amundi STOXX Europe 600 Banks UCITS ETF",
                "ENUE.DE": "iShares MSCI Europe Financials Screened UCITS ETF",

                # Commodity / ouro ETC
                "SGLN.L": "iShares Physical Gold ETC",
                "PHAG.DE": "WisdomTree Physical Gold ETC EUR",

                # Criptomoedas
                "DFNG.L": "VanEck Europe Defence UCITS ETF",  
                "WDEF.L": "WisdomTree Europe Defence UCITS ETF",  

                # Multi-fundo / Balanced
                "VWRL.L": "Vanguard FTSE All-World UCITS ETF",
                "VUAG.L": "Vanguard S&P 500 UCITS ETF USD Acc",
                "CSP1.L": "iShares Core S&P 500 UCITS ETF USD Acc",
                }
                
        symbol_info = symbol_real | symbol_dolar | symbol_euro


        # === TAB 1: OPTIMIZATION ===
        with tab1:
            st.title("Portfolio Optimizer")

            st.header("Select Assets for Optimization")

            available_symbols = sorted(symbol_info.keys(), key=lambda x: symbol_info.get(x, x))

            selected_symbols = st.multiselect(
                "Select the assets to optimize:",
                options=available_symbols,
                default=["PETR4.SA", "TAEE11.SA", "WEGE3.SA", "BND", "TLT", "GLD"],
                format_func=lambda x: f"{symbol_info.get(x, x)} [{x}]"
            )

            #default=["VTI", "VT", "VOO", "VEA", "EEM", "BND", "TLT", "GLD", "VNQ"]

            benchmark_choice = st.selectbox("Select Benchmark:", list(benchmarks.keys()), index=0)
            currency_choice = st.selectbox("Select Currency", ["Real", "Dollar", "Euro"], index=0)


            if len(selected_symbols) < 2:
                st.warning("Please select at least two assets.")
                st.stop()

            # --- Download de dados ---
            st.header("Downloading Data...")

            today = pd.to_datetime('today').normalize()

            def safe_download(symbol, start, end, max_retries=10, wait=2):
                for attempt in range(max_retries):
                    try:
                        df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
                        if 'Close' in df and not df['Close'].dropna().empty:
                            return df['Close']
                    except Exception:
                        pass
                    time.sleep(wait)
                return pd.Series(dtype=float)

            data = pd.DataFrame()
            valid_symbols = []
            for symbol in selected_symbols:
                close_data = safe_download(symbol, start="2000-01-01", end=today)
                if not close_data.empty:
                    data[symbol] = close_data
                    valid_symbols.append(symbol)
                else:
                    st.warning(f"⚠️ Failed to download data for: {symbol}")

            if len(valid_symbols) < 2:
                st.error("Too few valid assets to optimize. Please adjust your selection.")
                st.stop()

            data_benchmark = pd.DataFrame()
            for name, ticker in benchmarks.items():
                data_benchmark[name] = safe_download(ticker, start="2000-01-01", end=today)

            # #Baixando o CDI
            # var_ok = 0 
            # while var_ok != 1:
            #     try:
            #         url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json'
            #         cdi = pd.read_json(url)
            #         cdi['data'] = pd.to_datetime(cdi['data'], dayfirst=True)
            #         cdi.rename({'data': 'Date','valor':'CDI'}, axis='columns', inplace= True)
            #         cdi.set_index('Date', inplace = True)
            #         cdi['CDI']=cdi['CDI']/100
            #         var_ok = 1 
            #     except:
            #         0

            # #Baixando o IMA-B
            # var_ok = 0
            # while var_ok != 1:
            #     try:
            #         url2 = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.12466/dados?formato=json'
            #         imab = pd.read_json(url2)
            #         imab['data'] = pd.to_datetime(imab['data'], dayfirst=True)
            #         imab.rename({'data': 'Date','valor':'Ima-B'}, axis='columns', inplace= True)
            #         imab.set_index('Date', inplace = True)
            #         var_ok = 1
            #     except:
            #         0

            # data_benchmark['IMA-B'] = imab['Ima-B']

            returns = np.log(data / data.shift(1)).dropna()

            returns_benchmark_all = np.log(data_benchmark / data_benchmark.shift(1)).dropna()
            # returns_benchmark_all['CDI'] = cdi['CDI']
            
            dollar_brl = safe_download("USDBRL=X", start="2000-01-01", end=today)
            euro_brl = safe_download("EURBRL=X", start="2000-01-01", end=today)
            usd_eur = safe_download("USDEUR=X", start="2000-01-01", end=today) 

        # --- Ajustar retorno para moeda escolhida ---
            if currency_choice == "Real":
                for symbol in returns.columns:
                    if symbol in symbol_dolar:
                        aligned = np.log(dollar_brl / dollar_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDBRL=X"]) - 1
                    elif symbol in symbol_euro:
                        aligned = np.log(euro_brl / euro_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["EURBRL=X"]) - 1

            elif currency_choice == "Dollar":
                for symbol in returns.columns:
                    if symbol in symbol_real:
                        aligned = -np.log(dollar_brl / dollar_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDBRL=X"]) - 1
                    elif symbol in symbol_euro:
                        aligned = np.log(usd_eur / usd_eur.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDEUR=X"]) - 1

            elif currency_choice == "Euro":
                for symbol in returns.columns:
                    if symbol in symbol_real:
                        aligned = -np.log(euro_brl / euro_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["EURBRL=X"]) - 1
                    elif symbol in symbol_dolar:
                        aligned = -np.log(usd_eur / usd_eur.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDEUR=X"]) - 1

            cov_matrix = np.asarray(252 * returns.cov())
            annualized_returns = np.asarray(252 * returns.mean())

            first_available_date = returns.index.min()
            last_available_date = returns.index.max()

            st.success(f"Data downloaded successfully! Available from {first_available_date.date()} to {last_available_date.date()}.")

            # --- Otimização (Fronteira Eficiente) ---
            st.header("Efficient Frontier")

            bounds = [(0.0, 1.0) for _ in range(len(selected_symbols))]
            initial_guess = [1 / len(selected_symbols)] * len(selected_symbols)
            rent_alvo = np.arange(0.01, 1.5, 0.005)

            def portfolio_variance(w):
                return np.dot(w.T, np.dot(cov_matrix, w))

            def portfolio_return(w):
                return np.dot(w, annualized_returns)

            def minimize_portfolio_variance(min_return):
                cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                        {'type': 'ineq', 'fun': lambda w: portfolio_return(w) - min_return})
                return minimize(portfolio_variance, initial_guess,
                                method='SLSQP',
                                bounds=bounds,
                                constraints=cons)

            frontier = pd.Series()
            weights_frontier = pd.DataFrame()

            for r_target in rent_alvo:
                result = minimize_portfolio_variance(r_target)
                if result.success:
                    w_opt = result.x
                    sigma = np.sqrt(portfolio_variance(w_opt))
                    ret = portfolio_return(w_opt)
                    frontier.at[sigma] = ret
                    for idx, sym in enumerate(selected_symbols):
                        weights_frontier.at[round(sigma, 4), sym] = w_opt[idx]

            frontier_df = pd.DataFrame({
                'Risk (Std Dev)': frontier.index,
                'Expected Return': frontier.values
            })
            frontier_df['Sharpe'] = frontier_df['Expected Return'] / frontier_df['Risk (Std Dev)']

            min_vol_idx = frontier_df['Risk (Std Dev)'].idxmin()
            max_ret_idx = frontier_df['Expected Return'].idxmax()
            max_sharpe_idx = frontier_df['Sharpe'].idxmax()

            # --- Plot Fronteira ---
            st.subheader("Efficient Frontier")

            fig_frontier = go.Figure()
            fig_frontier.add_trace(go.Scatter(
                x=frontier_df['Risk (Std Dev)'],
                y=frontier_df['Expected Return'],
                mode='lines+markers',
                name='Efficient Frontier'
            ))

            highlight_points = {
                "Minimum Volatility": (min_vol_idx, 'blue', 'diamond'),
                "Maximum Return": (max_ret_idx, 'green', 'square'),
                "Maximum Sharpe": (max_sharpe_idx, 'red', 'star')
            }

            for label, (idx, color, symbol) in highlight_points.items():
                fig_frontier.add_trace(go.Scatter(
                    x=[frontier_df.loc[idx, 'Risk (Std Dev)']],
                    y=[frontier_df.loc[idx, 'Expected Return']],
                    mode='markers+text',
                    name=label,
                    text=[label],
                    textposition='bottom center',
                    marker=dict(size=12, symbol=symbol, color=color)
                ))

            fig_frontier.update_layout(
                title="Efficient Frontier with Key Portfolios Highlighted",
                xaxis_title="Portfolio Risk (Std Dev)",
                yaxis_title="Portfolio Expected Return",
                template="plotly_white"
            )

            st.plotly_chart(fig_frontier, use_container_width=True)

            # --- Escolha da carteira para análise ---
            st.header("Select Portfolio for Analysis")

            portfolio_choice = st.selectbox(
                "Choose which portfolio to analyze:",
                ("Minimum Volatility", "Maximum Return", "Maximum Sharpe"),
                index=2
            )

            if portfolio_choice == "Minimum Volatility":
                idx_selected = min_vol_idx
            elif portfolio_choice == "Maximum Return":
                idx_selected = max_ret_idx
            elif portfolio_choice == "Maximum Sharpe":
                idx_selected = max_sharpe_idx

            selected_sigma = frontier_df.loc[idx_selected, 'Risk (Std Dev)']
            selected_weights = weights_frontier.loc[round(selected_sigma, 4)]
            selected_weights = selected_weights[selected_weights > 0]

            # --- Tabela da Composição da Carteira ---
            st.subheader("Portfolio Composition")

            composition_df = pd.DataFrame(selected_weights)
            composition_df.columns = ['Weight']
            st.dataframe(composition_df.style.format({"Weight": "{:.2%}"}))

            # --- Seleção de período ---
            st.header("Select Analysis Period")

            start_analysis = st.date_input(
                "Start Date", 
                min_value=first_available_date.date(), 
                max_value=last_available_date.date(), 
                value=first_available_date.date()
            )

            end_analysis = st.date_input(
                "End Date", 
                min_value=first_available_date.date(), 
                max_value=last_available_date.date(), 
                value=last_available_date.date()
            )

            if start_analysis >= end_analysis:
                st.warning("Start Date must be before End Date.")
                st.stop()

            rf_data = safe_download("BIL", start="2000-01-01", end=today)
            rf_returns = np.log(rf_data / rf_data.shift(1)).dropna()
            rf_analysis = rf_returns[start_analysis:end_analysis]
            #rf_rate = empyrical.annual_return(rf_analysis)
            #rf_rate = np.asarray(252 * rf_returns.mean())
            rf_rate = rf_returns[start_analysis:end_analysis].mean()


            # --- Performance ---       
            st.header("Performance Summary")

            returns_portfolio = returns[selected_weights.index] @ selected_weights
            returns_analysis = returns_portfolio[start_analysis:end_analysis].dropna()

            rf_analysis = rf_returns[start_analysis:end_analysis]
            rf_analysis = rf_analysis.reindex(returns_analysis.index).dropna()
            #rf_analysis = rf_analysis.loc[returns_analysis.index].dropna()

            returns_benchmark = returns_benchmark_all[benchmark_choice][start_analysis:end_analysis]

            # Sharpe Ratio manual
            mean_return = float(returns_analysis.mean())
            std_dev = float(returns_analysis.std())
            rf_mean = float(rf_analysis.mean())
            sharpe_ratio = ((mean_return - rf_mean) / std_dev) * np.sqrt(252)


            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Expected Return", f"{empyrical.annual_return(returns_analysis):.2%}")
            col2.metric("Risk (Std Dev)", f"{empyrical.annual_volatility(returns_analysis):.2%}")
            col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            col4.metric("Maximum Drawdown", f"{empyrical.max_drawdown(returns_analysis):.2%}")
            col5.metric("VaR (1%)", f"{empyrical.value_at_risk(returns_analysis, cutoff=0.01):.2%}")
            
            # --- Gráfico Retorno Acumulado ---
            st.header("Cumulative Returns Comparison")

            # Garantir que os índices estejam alinhados para os gráficos
            common_index = returns_analysis.index.intersection(returns_benchmark.index)

            # Reindexar as séries
            returns_analysis = returns_analysis.loc[common_index]
            returns_benchmark = returns_benchmark.loc[common_index]

            cumulative_portfolio = (1 + returns_analysis).cumprod()
            cumulative_benchmark = (1 + returns_benchmark).cumprod()

            fig_cum = go.Figure()
            fig_cum.add_trace(go.Scatter(x=cumulative_portfolio.index, y=cumulative_portfolio.values, mode='lines', name='Portfolio'))
            fig_cum.add_trace(go.Scatter(x=cumulative_benchmark.index, y=cumulative_benchmark.values, mode='lines', name=benchmark_choice))
            fig_cum.update_layout(
                title="Cumulative Returns: Portfolio vs Benchmark",
                xaxis_title="Date",
                yaxis_title="Cumulative Value",
                template="plotly_white"
            )
            st.plotly_chart(fig_cum, use_container_width=True)

            # --- Rolling Volatility ---
            st.header("Rolling Volatility (30 Days)")

            rolling_vol_portfolio = returns_analysis.rolling(30).std() * np.sqrt(252)
            rolling_vol_benchmark = returns_benchmark.rolling(30).std() * np.sqrt(252)

            fig_vol = go.Figure()
            fig_vol.add_trace(go.Scatter(
                x=rolling_vol_portfolio.index,
                y=rolling_vol_portfolio.values,
                mode='lines',
                name='Portfolio',
                line=dict(color='blue')
            ))
            fig_vol.add_trace(go.Scatter(
                x=rolling_vol_benchmark.index,
                y=rolling_vol_benchmark.values,
                mode='lines',
                name=benchmark_choice,
                line=dict(color='red')
            ))
            fig_vol.update_layout(
                title="Rolling Volatility (30 Days)",
                xaxis_title="Date",
                yaxis_title="Volatility (Annualized)",
                template="plotly_white"
            )
            st.plotly_chart(fig_vol, use_container_width=True)


            # --- Drawdown ---
            st.header("Portfolio Drawdown")

            # Carteira
            cumulative_returns_portfolio = (1 + returns_analysis).cumprod()
            running_max_portfolio = cumulative_returns_portfolio.cummax()
            drawdown_portfolio = (cumulative_returns_portfolio / running_max_portfolio) - 1

            # Benchmark
            cumulative_returns_benchmark = (1 + returns_benchmark).cumprod()
            running_max_benchmark = cumulative_returns_benchmark.cummax()
            drawdown_benchmark = (cumulative_returns_benchmark / running_max_benchmark) - 1

            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(
                x=drawdown_portfolio.index,
                y=drawdown_portfolio.values,
                mode='lines',
                name='Portfolio',
                line=dict(color='blue')
            ))
            fig_dd.add_trace(go.Scatter(
                x=drawdown_benchmark.index,
                y=drawdown_benchmark.values,
                mode='lines',
                name=benchmark_choice,
                line=dict(color='red')
            ))
            fig_dd.update_layout(
                title="Portfolio vs Benchmark Drawdown",
                xaxis_title="Date",
                yaxis_title="Drawdown",
                template="plotly_white"
            )
            st.plotly_chart(fig_dd, use_container_width=True)


            # --- Monthly Returns Heatmap ---
            st.header("Monthly Returns Heatmap")

            monthly_returns = returns_analysis.resample('M').apply(lambda x: np.exp(x.sum()) - 1)
            monthly_returns_df = monthly_returns.to_frame(name='Return')
            monthly_returns_df.index = monthly_returns_df.index.to_period('M')

            monthly_returns_df['Year'] = monthly_returns_df.index.year
            monthly_returns_df['Month'] = monthly_returns_df.index.month

            pivot_table = monthly_returns_df.pivot_table(index='Year', columns='Month', values='Return')
            pivot_table = pivot_table.reindex(columns=range(1,13))  # Garantir 12 meses

            months_labels = [calendar.month_abbr[m] for m in range(1,13)]
            years_labels = pivot_table.index.astype(str).tolist()

            fig = go.Figure(data=go.Heatmap(
                z=pivot_table.values * 100,  # Converter para %
                x=months_labels,
                y=years_labels,
                colorscale='RdYlGn',
                colorbar=dict(title="Return (%)"),
                zmin=-20,
                zmax=20,
                hovertemplate='%{y} %{x}<br>Return: %{z:.2f}%<extra></extra>'
            ))

            fig.update_layout(
                title="Monthly Returns Heatmap",
                xaxis_title="Month",
                yaxis_title="Year",
                template="plotly_white",
                height=600,
                width=1000
            )

            st.plotly_chart(fig, use_container_width=True)

            # --- Correlation Matrix ---
            correlation_matrix = returns.corr()
            # Criar texto de anotação com duas casas decimais
            annot_text = correlation_matrix.round(2).astype(str).values.tolist()

            # Título para seção
            st.markdown("### Correlation Matrix")

            # Gráfico de calor interativo
            fig_corr = ff.create_annotated_heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns.tolist(),
                y=correlation_matrix.index.tolist(),
                annotation_text=annot_text,
                colorscale='RdBu',
                showscale=True,
                reversescale=True,
                zmin=-1,
                zmax=1
            )
            st.plotly_chart(fig_corr, use_container_width=True)


        # === TAB 2: COMPARISON ===
        with tab2:
            st.subheader("Compare Your Portfolio with an Optimized One")

            if "comparison_ready" not in st.session_state:
                st.session_state["comparison_ready"] = False

            if not st.session_state["comparison_ready"]:
                st.markdown("Select your current holdings below and their respective weights.")

                # Gerar lista de opções amigáveis com descrição + ticker
                ticker_options = [f"{desc} [{symbol}]" for symbol, desc in symbol_info.items()]
                ticker_lookup = {f"{desc} [{symbol}]": symbol for symbol, desc in symbol_info.items()}  # reverse map

                # Dados padrão com tickers válidos
                default_symbols = ["VTI", "VT", "VOO", "VEA", "EEM", "BND", "TLT", "GLD", "VNQ"]
                default_weights = [0.11, 0.10, 0.10, 0.10, 0.10, 0.15, 0.09, 0.10, 0.15]

                # Criar a tabela com tickers formatados
                default_data_display = pd.DataFrame({
                    "Ticker": [f"{symbol_info.get(sym, sym)} [{sym}]" for sym in default_symbols],
                    "Weight": [w * 100 for w in default_weights]  # porcentagem
                })

                user_portfolio_display = st.data_editor(
                    default_data_display,
                    num_rows="dynamic",
                    column_config={
                        "Ticker": st.column_config.SelectboxColumn(
                            "Ticker",
                            options=ticker_options
                        ),
                        "Weight": st.column_config.NumberColumn(
                            "Weight (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f"
                        )
                    }
                )

                # Converter de volta para formato interno: símbolo real e peso como fração
                user_portfolio = user_portfolio_display.copy()
                user_portfolio["Ticker"] = user_portfolio["Ticker"].map(ticker_lookup)
                user_portfolio["Weight"] = user_portfolio["Weight"] / 100

                # Verificar soma dos pesos
                weight_sum = user_portfolio["Weight"].sum() * 100
                st.markdown(f"**Total Allocation: {weight_sum:.2f}%**")

                if abs(weight_sum - 100) > 0.01:
                    st.error("Total allocation must sum to 100%. Please adjust the weights.")
                    st.stop()

                user_portfolio["Weight"] = user_portfolio["Weight"] / user_portfolio["Weight"].sum()

                tickers = user_portfolio["Ticker"].unique().tolist()

                currency_choice = st.selectbox("Select Currency", ["Real", "Dollar", "Euro"], index=0, key="currency_tab2")


                def safe_download(symbol, start, end, max_retries=10, wait=2):
                    for attempt in range(max_retries):
                        try:
                            df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
                            if 'Close' in df and not df['Close'].dropna().empty:
                                return df['Close']
                        except Exception:
                            pass
                        time.sleep(wait)
                    return pd.Series(dtype=float)

                today = pd.Timestamp.today().date()

                price_data = pd.DataFrame()
                valid_symbols = []
                for symbol in tickers:
                    close_data = safe_download(symbol, start="2000-01-01", end=today)
                    if not close_data.empty:
                        price_data[symbol] = close_data
                        valid_symbols.append(symbol)
                    else:
                        st.warning(f"⚠️ Failed to download data for: {symbol}")

                if len(valid_symbols) < 2:
                    st.error("Too few valid assets to run the analysis. Please adjust your selection.")
                    st.stop()

                # Identificar intervalo real disponível com base nos dados baixados
                first_available_date = price_data.index.min()
                last_available_date = price_data.index.max()

                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Start Date",
                        value=first_available_date.date(),
                        min_value=first_available_date.date(),
                        max_value=last_available_date.date()
                    )
                with col2:
                    end_date = st.date_input(
                        "End Date",
                        value=last_available_date.date(),
                        min_value=first_available_date.date(),
                        max_value=last_available_date.date()
                    )

                if st.button("Run Comparison"):
                    st.session_state["user_portfolio"] = user_portfolio
                    st.session_state["start_date"] = start_date
                    st.session_state["end_date"] = end_date
                    st.session_state["comparison_ready"] = True
                    st.rerun()

            if not st.session_state["comparison_ready"]:
                st.stop()

            user_portfolio = st.session_state["user_portfolio"]
            start_date = st.session_state["start_date"]
            end_date = st.session_state["end_date"]

            tickers = user_portfolio["Ticker"].tolist()
            weights_current = user_portfolio.set_index("Ticker")["Weight"].to_dict()

            raw_data = yf.download(tickers, start=start_date, end=end_date, group_by="ticker")
            if isinstance(raw_data.columns, pd.MultiIndex):
                price_data = raw_data.xs('Close', axis=1, level=1)[tickers].dropna()
            else:
                price_data = raw_data[tickers].dropna()

            weights_vector = np.array([weights_current[t] for t in price_data.columns])
            returns = price_data.pct_change().dropna()

            # Ajuste cambial com base na escolha do usuário
            if currency_choice == "Real":
                for symbol in returns.columns:
                    if symbol in symbol_dolar:
                        dollar_brl = safe_download("USDBRL=X", start="2000-01-01", end=today)
                        aligned = np.log(dollar_brl / dollar_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDBRL=X"]) - 1
                    elif symbol in symbol_euro:                          
                        euro_brl = safe_download("EURBRL=X", start="2000-01-01", end=today)
                        aligned = np.log(euro_brl / euro_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["EURBRL=X"]) - 1

            elif currency_choice == "Dollar":
                for symbol in returns.columns:
                    if symbol in symbol_real:
                        dollar_brl = safe_download("USDBRL=X", start="2000-01-01", end=today)
                        aligned = -np.log(dollar_brl / dollar_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDBRL=X"]) - 1
                    elif symbol in symbol_euro:
                        usd_eur = safe_download("USDEUR=X", start="2000-01-01", end=today) 
                        aligned = np.log(usd_eur / usd_eur.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDEUR=X"]) - 1

            elif currency_choice == "Euro":
                for symbol in returns.columns:
                    if symbol in symbol_real:
                        euro_brl = safe_download("EURBRL=X", start="2000-01-01", end=today)
                        aligned = -np.log(euro_brl / euro_brl.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["EURBRL=X"]) - 1
                    elif symbol in symbol_dolar:
                        usd_eur = safe_download("USDEUR=X", start="2000-01-01", end=today) 
                        aligned = -np.log(usd_eur / usd_eur.shift(1)).dropna()
                        aligned = aligned.reindex(returns.index).dropna()
                        returns = returns.loc[aligned.index]
                        returns[symbol] = (1 + returns[symbol]) * (1 + aligned["USDEUR=X"]) - 1

            # Agora com returns ajustado:
            portfolio_current = returns @ weights_vector

            mu = expected_returns.mean_historical_return(price_data)
            S = risk_models.sample_cov(price_data)

            cov_matrix = np.asarray(252 * returns.cov())
            annualized_returns = np.asarray(252 * returns.mean())
            rent_alvo = np.arange(0.01, 1.2, 0.0025)

            def port_ret(w): return w @ annualized_returns
            def port_vol(w): return np.sqrt(w @ cov_matrix @ w)
            def minimize_var(target):
                cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                        {'type': 'eq', 'fun': lambda w: port_ret(w) - target})
                return minimize(port_vol, x0=[1/len(tickers)]*len(tickers), bounds=[(0,1)]*len(tickers), constraints=cons)

            def minimize_risk_for_target_return(r):
                res = minimize_var(r)
                if res.success:
                    return port_vol(res.x), r, res.x

            frontier_points = [minimize_risk_for_target_return(r) for r in rent_alvo]
            frontier_points = [pt for pt in frontier_points if pt is not None]

            frontier_df = pd.DataFrame(frontier_points, columns=["Risk", "Return", "Weights"])
            frontier_df["Sharpe"] = frontier_df["Return"] / frontier_df["Risk"]

            target_return = port_ret(weights_vector)
            target_risk = port_vol(weights_vector)

            same_risk_opt = frontier_df.iloc[(frontier_df["Risk"] - target_risk).abs().argmin()]
            same_return_opt = frontier_df.iloc[(frontier_df["Return"] - target_return).abs().argmin()]

            st.markdown("### Efficient Frontier & Portfolio Comparison")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=frontier_df["Risk"], y=frontier_df["Return"], mode='lines', name="Efficient Frontier"))
            fig.add_trace(go.Scatter(x=[target_risk], y=[target_return], mode='markers+text', marker=dict(color="red", size=12), name="Your Portfolio", text=["Current"], textposition="top center"))
            fig.add_trace(go.Scatter(x=[same_risk_opt["Risk"]], y=[same_risk_opt["Return"]], mode='markers+text', marker=dict(color="green", size=12), name="Same Risk", text=["↑ Return"], textposition="bottom center"))
            fig.add_trace(go.Scatter(x=[same_return_opt["Risk"]], y=[same_return_opt["Return"]], mode='markers+text', marker=dict(color="blue", size=12), name="Same Return", text=["↓ Risk"], textposition="bottom center"))
            fig.update_layout(title="Efficient Frontier & Portfolio Comparison", xaxis_title="Risk (Std Dev)", yaxis_title="Expected Return")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Recommended Portfolios")
            rec_weights_df = pd.DataFrame({
                "Same Risk": same_risk_opt["Weights"],
                "Same Return": same_return_opt["Weights"]
            }, index=tickers)
            st.dataframe(rec_weights_df.style.format("{:.2%}"))

            st.markdown("### Select Optimized Portfolio for Backtesting")
            choice = st.radio("Select Portfolio:", ["Same Risk (↑ Return)", "Same Return (↓ Risk)"], key="portfolio_choice")

            if choice == "Same Risk (↑ Return)":
                selected_weights = same_risk_opt["Weights"]
                label_opt = "Same Risk Optimized"
            else:
                selected_weights = same_return_opt["Weights"]
                label_opt = "Same Return Optimized"

            returns_opt = returns @ selected_weights

            st.markdown("### Performance Metrics Comparison")
            col1, col2 = st.columns(2)
            col1.metric("Annual Return (Current)", f"{empyrical.annual_return(portfolio_current):.2%}")
            col2.metric(f"Annual Return ({label_opt})", f"{empyrical.annual_return(returns_opt):.2%}")

            col3, col4 = st.columns(2)
            col3.metric("Volatility (Current)", f"{empyrical.annual_volatility(portfolio_current):.2%}")
            col4.metric(f"Volatility ({label_opt})", f"{empyrical.annual_volatility(returns_opt):.2%}")

            # Calcular Sharpe Ratio manualmente         
            rf_data = safe_download("BIL", start="2000-01-01", end=today)
            rf_returns = np.log(rf_data / rf_data.shift(1)).dropna()
            rf_analysis = rf_returns[start_date:end_date]
            rf_analysis = rf_analysis.reindex(returns_analysis.index).dropna()
            #rf_analysis = rf_analysis.loc[returns_analysis.index].dropna()        
            rf_mean = rf_analysis.mean()

            sharpe_current = ((portfolio_current.mean().item() - rf_mean.item()) / portfolio_current.std().item()) * np.sqrt(252)
            sharpe_opt = ((returns_opt.mean().item() - rf_mean.item()) / returns_opt.std().item()) * np.sqrt(252)

            col5, col6 = st.columns(2)
            col5.metric("Sharpe Ratio (Current)", f"{sharpe_current:.2f}")
            col6.metric(f"Sharpe Ratio ({label_opt})", f"{sharpe_opt:.2f}")

            col7, col8 = st.columns(2)
            col7.metric("Max Drawdown (Current)", f"{empyrical.max_drawdown(portfolio_current):.2%}")
            col8.metric(f"Max Drawdown ({label_opt})", f"{empyrical.max_drawdown(returns_opt):.2%}")

            col9, col10 = st.columns(2)
            col9.metric("VaR 1% (Current)", f"{empyrical.value_at_risk(portfolio_current, cutoff=0.01):.2%}")
            col10.metric(f"VaR 1% ({label_opt})", f"{empyrical.value_at_risk(returns_opt, cutoff=0.01):.2%}")

            st.markdown("### Cumulative Returns")
            cum_opt = (1 + returns_opt).cumprod()
            cum_cur = (1 + portfolio_current).cumprod()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=cum_cur.index, y=cum_cur, mode='lines', name='Current'))
            fig.add_trace(go.Scatter(x=cum_opt.index, y=cum_opt, mode='lines', name=label_opt))
            fig.update_layout(title="Cumulative Returns Comparison", xaxis_title="Date", yaxis_title="Portfolio Value")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Rolling Volatility (30 Days)")
            rolling_vol_cur = portfolio_current.rolling(30).std() * np.sqrt(252)
            rolling_vol_opt = returns_opt.rolling(30).std() * np.sqrt(252)
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Scatter(x=rolling_vol_cur.index, y=rolling_vol_cur, name='Current', line=dict(color='gray')))
            fig_vol.add_trace(go.Scatter(x=rolling_vol_opt.index, y=rolling_vol_opt, name=label_opt, line=dict(color='red')))
            fig_vol.update_layout(title="Rolling Volatility Comparison", xaxis_title="Date", yaxis_title="Volatility")
            st.plotly_chart(fig_vol, use_container_width=True)

            st.markdown("### Portfolio Drawdown")
            def get_drawdown(series):
                cumulative = (1 + series).cumprod()
                running_max = cumulative.cummax()
                return (cumulative / running_max) - 1

            drawdown_cur = get_drawdown(portfolio_current)
            drawdown_opt = get_drawdown(returns_opt)

            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(x=drawdown_cur.index, y=drawdown_cur, name='Current'))
            fig_dd.add_trace(go.Scatter(x=drawdown_opt.index, y=drawdown_opt, name=label_opt))
            fig_dd.update_layout(title="Portfolio Drawdown Comparison", xaxis_title="Date", yaxis_title="Drawdown")
            st.plotly_chart(fig_dd, use_container_width=True)

        
            st.markdown("### Correlation Matrix")
            correlation_matrix = returns.corr()
            annot_text = correlation_matrix.round(2).astype(str).values.tolist()

            fig_corr = ff.create_annotated_heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns.tolist(),
                y=correlation_matrix.index.tolist(),
                annotation_text=annot_text,
                colorscale='RdBu',
                showscale=True,
                reversescale=True,
                zmin=-1,
                zmax=1
            )
            st.plotly_chart(fig_corr, use_container_width=True)

    except Exception as e:

         st.error("An unexpected error occurred during the optimization process.")
        #st.text(f"Technical details: {e}")
        
   
