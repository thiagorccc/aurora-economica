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


def show_optimizer():

    # --- CONFIG PAGE ---
    #st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

    # --- LOGO ---
    logo = Image.open("aurora_logo_vertical.png")
    st.image(logo, use_container_width=False, width=800)


    # --- TABS ---
    tab1, tab2 = st.tabs(["Optimization", "Compare with Current Portfolio"])

    # === SYMBOLS LIST ===
    symbols = [
        "0P0000RZ2I.F", "AGGH.L", "AMDL", "ARKK", "BIL", "BKLN", "BITX", "BNDX",
        "BPYPM", "BRK-B", "CONL", "CONY", "DOC", "EEM", "EFA", "EGLN.L", "EIMI.L","EQQQ.DE", "EQQQ.L", "ETHA",
        "EWZ", "FAZ", "FRR", "FRT", "FVRR", "FXI", "GDX", "GDXD", "GDXJ", "GLD",
        "GLL", "GOOGL", "GOVT", "IAU", "IBIT", "IE00B7KFL990.IR", "IEAC.L", "IEF", "IEMG", "IEFA", "IBGS.L",
        "IJH", "IJPA.L", "IMEU.L", "ISF.L", "IWDA.AS", "IWMO.L", "IWM", "JAAA",
        "JEPQ", "JNJ", "KMI", "KOLD", "KRE", "LABD", "LQD", "METU", "MSTU",
        "MSTX", "MSTY", "MSTZ", "MVOL.L", "NVDD", "NVD", "NVDL", "NVDQ", "NVDX",
        "O", "PDBC", "PLTD", "PLTU", "PSQ", 
        "QID", "QLD", "QQQ", "QYLD", "ROBN", "RSP", "SBIT", "SCHD", "SCHX",
        "SCHF", "SGOV", "SHV", "SKT", "SLG", "SLV", "SMCX", "SMH", "SMST",
        "SOXL", "SOXS", "SPDN", "SPXU", "SPXS", "SPY", "SPY5.DE", "SRLN", "SQQQ", "SWRD.L",
        "SDS", "TMF", "TLT", "TNA", "TQQQ", "TSLL", "TSLQ", "TSLS", "TSLT",
        "TSLZ", "UNG", "USFR", "USHY", "USO", "UVXY", "VEA", "VOO", "VWO",
        "VWCE.DE", "XBI", "XCHA.DE", "XFFE.MI", "XLE", "XLF", "XLI", "XLRE", "XLP", "XLU"
    ]

    # === TAB 1: OPTIMIZATION ===
    with tab1:
        st.title("Portfolio Optimizer")

        # Benchmarks disponíveis
        benchmarks = {
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
        }

        st.header("Select Assets for Optimization")

        # Nome descritivo + categoria
        symbol_info = {
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

            "IBGS.L": "UK Gilts All Stocks (Fixed Income)",
            "SCHP": "US TIPS ETF (Fixed Income)",
            "TLT": "20+ Year Treasury Bond ETF (Fixed Income)",
            "IEAC.L": "Euro Corporate Bonds (Fixed Income)",
            "AGGH.L": "Global Aggregate Bond (Fixed Income)",
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
            "EXX6.DE": "iShares Euro Government Bond 1-3yr (Fixed Income)",
            "IBCX.DE": "iShares Euro Government Bond 3-5yr (Fixed Income)",
            "IBGX.DE": "iShares Euro Government Bond 7-10yr (Fixed Income)",
            "IBCY.DE": "iShares Euro Government Bond 15-30yr (Fixed Income)",
            "SXR8.DE": "iShares Euro Investment Grade Corp Bond (Fixed Income)",
            "EUNA.DE": "Lyxor Euro Government Bond 10Y DR ETF (Fixed Income)",
            "IBCI.DE": "iShares Euro Government Inflation-Linked Bond ETF (Fixed Income)",
            "AGGE.DE": "iShares Global Aggregate Bond EUR Hedged (Fixed Income)",
            

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
            "BTCE.DE": "21Shares Bitcoin ETP (Crypto)",
            "ABTC.DE": "ETC Group Physical Bitcoin (Crypto)",
            "VBTC.AS": "VanEck Bitcoin ETN (Crypto)",
            "BTCE.AS": "BTCetc Bitcoin Exchange Traded Crypto (Crypto)",

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
            
            "VXX": "S&P 500 VIX Short-Term Futures ETN (Volatility)"            
        }

        available_symbols = sorted(symbol_info.keys(), key=lambda x: symbol_info.get(x, x))

        selected_symbols = st.multiselect(
            "Select the assets to optimize:",
            options=available_symbols,
            default=["VTI", "VT", "VOO", "VEA", "EEM", "BND", "TLT", "GLD", "VNQ"],
            format_func=lambda x: f"{symbol_info.get(x, x)} [{x}]"
        )

        benchmark_choice = st.selectbox("Select Benchmark:", list(benchmarks.keys()), index=0)

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

        returns = np.log(data / data.shift(1)).dropna()
        returns_benchmark_all = np.log(data_benchmark / data_benchmark.shift(1)).dropna()

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
        rf_rate = np.asarray(252 * rf_returns.mean())

        # --- Performance ---
        st.header("Performance Summary")

        returns_portfolio = returns[selected_weights.index] @ selected_weights
        returns_analysis = returns_portfolio[start_analysis:end_analysis]
        returns_benchmark = returns_benchmark_all[benchmark_choice][start_analysis:end_analysis]

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Expected Return", f"{empyrical.annual_return(returns_analysis):.2%}")
        col2.metric("Risk (Std Dev)", f"{empyrical.annual_volatility(returns_analysis):.2%}")
        col3.metric("Sharpe Ratio", f"{empyrical.sharpe_ratio(returns_analysis, risk_free=rf_rate):.2f}")
        col4.metric("Maximum Drawdown", f"{empyrical.max_drawdown(returns_analysis):.2%}")
        col5.metric("VaR (1%)", f"{empyrical.value_at_risk(returns_analysis, cutoff=0.01):.2%}")

        # --- Gráfico Retorno Acumulado ---
        st.header("Cumulative Returns Comparison")

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

        rolling_vol = returns_analysis.rolling(30).std() * np.sqrt(252)

        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol.values,
            mode='lines',
            line=dict(color='red'),
            name='Rolling Volatility'
        ))
        fig_vol.update_layout(
            title="Rolling Volatility - Portfolio (30 Days)",
            xaxis_title="Date",
            yaxis_title="Volatility",
            template="plotly_white"
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        # --- Drawdown ---
        st.header("Portfolio Drawdown")

        cumulative_returns = (1 + returns_analysis).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns / running_max) - 1

        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown.values,
            mode='lines',
            name='Drawdown'
        ))
        fig_dd.update_layout(
            title="Portfolio Drawdown Over Time",
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
            reversescale=True,
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

    # === TAB 2: COMPARISON ===
    with tab2:
        st.subheader("📊 Compare Your Portfolio with an Optimized One")

        if "comparison_ready" not in st.session_state:
            st.session_state["comparison_ready"] = False

        if not st.session_state["comparison_ready"]:
            st.markdown("Select your current holdings below and their respective weights.")

            default_data = pd.DataFrame({
                "Ticker": [
                    "IEAC.L", "IMEU.L", "EIMI.L", "IWDA.AS", "MVOL.L",
                    "IJPA.L", "IWMO.L", "SWRD.L", "VWCE.DE", "0P0000RZ2I.F"
                ],
                "Weight": [0.21, 0.11, 0.11, 0.11, 0.11, 0.06, 0.06, 0.06, 0.06, 0.11]
            })

            user_portfolio = st.data_editor(
                default_data,
                num_rows="dynamic",
                column_config={"Ticker": st.column_config.SelectboxColumn("Ticker", options=symbols)}
            )

            weight_sum = user_portfolio["Weight"].sum() * 100
            st.markdown(f"**Total Allocation: {weight_sum:.2f}%**")

            if abs(weight_sum - 100) > 0.01:
                st.error("Total allocation must sum to 100%. Please adjust the weights.")
                st.stop()

            user_portfolio["Weight"] = user_portfolio["Weight"] / user_portfolio["Weight"].sum()

            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", datetime.today() - relativedelta(years=3))
            with col2:
                end_date = st.date_input("End Date", datetime.today())

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
        portfolio_current = returns @ weights_vector

        mu = expected_returns.mean_historical_return(price_data)
        S = risk_models.sample_cov(price_data)

        cov_matrix = np.asarray(252 * returns.cov())
        annualized_returns = np.asarray(252 * returns.mean())
        rent_alvo = np.arange(0.01, 1.2, 0.005)

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

        st.markdown("### 🔎 Select Optimized Portfolio for Backtesting")
        choice = st.radio("Select Portfolio:", ["Same Risk (↑ Return)", "Same Return (↓ Risk)"], key="portfolio_choice")

        if choice == "Same Risk (↑ Return)":
            selected_weights = same_risk_opt["Weights"]
            label_opt = "Same Risk Optimized"
        else:
            selected_weights = same_return_opt["Weights"]
            label_opt = "Same Return Optimized"

        returns_opt = returns @ selected_weights

        st.markdown("### 📊 Performance Metrics Comparison")
        col1, col2 = st.columns(2)
        col1.metric("Annual Return (Current)", f"{empyrical.annual_return(portfolio_current):.2%}")
        col2.metric(f"Annual Return ({label_opt})", f"{empyrical.annual_return(returns_opt):.2%}")

        col3, col4 = st.columns(2)
        col3.metric("Volatility (Current)", f"{empyrical.annual_volatility(portfolio_current):.2%}")
        col4.metric(f"Volatility ({label_opt})", f"{empyrical.annual_volatility(returns_opt):.2%}")

        col5, col6 = st.columns(2)
        col5.metric("Sharpe Ratio (Current)", f"{empyrical.sharpe_ratio(portfolio_current):.2f}")
        col6.metric(f"Sharpe Ratio ({label_opt})", f"{empyrical.sharpe_ratio(returns_opt):.2f}")

        col7, col8 = st.columns(2)
        col7.metric("Max Drawdown (Current)", f"{empyrical.max_drawdown(portfolio_current):.2%}")
        col8.metric(f"Max Drawdown ({label_opt})", f"{empyrical.max_drawdown(returns_opt):.2%}")

        col9, col10 = st.columns(2)
        col9.metric("VaR 1% (Current)", f"{empyrical.value_at_risk(portfolio_current, cutoff=0.01):.2%}")
        col10.metric(f"VaR 1% ({label_opt})", f"{empyrical.value_at_risk(returns_opt, cutoff=0.01):.2%}")

        st.markdown("### 📈 Cumulative Returns")
        cum_opt = (1 + returns_opt).cumprod()
        cum_cur = (1 + portfolio_current).cumprod()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cum_cur.index, y=cum_cur, mode='lines', name='Current'))
        fig.add_trace(go.Scatter(x=cum_opt.index, y=cum_opt, mode='lines', name=label_opt))
        fig.update_layout(title="Cumulative Returns Comparison", xaxis_title="Date", yaxis_title="Portfolio Value")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📉 Rolling Volatility (30 Days)")
        rolling_vol_cur = portfolio_current.rolling(30).std() * np.sqrt(252)
        rolling_vol_opt = returns_opt.rolling(30).std() * np.sqrt(252)
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=rolling_vol_cur.index, y=rolling_vol_cur, name='Current', line=dict(color='gray')))
        fig_vol.add_trace(go.Scatter(x=rolling_vol_opt.index, y=rolling_vol_opt, name=label_opt, line=dict(color='red')))
        fig_vol.update_layout(title="Rolling Volatility Comparison", xaxis_title="Date", yaxis_title="Volatility")
        st.plotly_chart(fig_vol, use_container_width=True)

        st.markdown("### 📉 Portfolio Drawdown")
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
