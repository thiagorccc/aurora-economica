import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ta import momentum, trend, volatility, volume
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, cohen_kappa_score
import matplotlib.pyplot as plt
import random


def show_predictor():
    st.title("📊 Previsão de Direção de Ativos com Machine Learning (Mensal)")
    st.markdown("Previsão da tendência do ativo para o mês corrente com base em indicadores técnicos e modelos de aprendizado de máquina.")

    ticker = st.selectbox("Selecione a ação ou ETF:", options=["SPY", "ACWI", "QQQ", "EFA", "BOVA11.SA", "IVVB11.SA"])

    st.markdown("### Selecione o método de previsão:")
    col1, col2, col3 = st.columns(3)
    with col1:
        knn_selected = st.button("KNN")
    with col2:
        rf_selected = st.button("RF")
    with col3:
        svm_selected = st.button("SVM")

    model_selected = None
    if knn_selected:
        model_selected = "KNN"
    elif rf_selected:
        model_selected = "RF"
    elif svm_selected:
        model_selected = "SVM"

    if model_selected:
        st.subheader(f"📈 Resultado para {ticker}")
        with st.spinner(f"Analisando {ticker} com {model_selected}..."):
            result, metrics, df_plot, fig_cm, fig_roc = predict_monthly_direction(ticker, model_selected)

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Tendência", result)
            col2.metric("Acurácia Treino", f"{metrics['acc_train']:.2%}")
            col3.metric("Acurácia Teste", f"{metrics['acc_test']:.2%}")
            col4.metric("Kappa", f"{metrics['kappa']:.2f}")
            col5.metric("AUC", f"{metrics['auc']:.2f}" if not np.isnan(metrics["auc"]) else "N/A")

            if 'Close' in df_plot.columns:
                st.markdown("#### Preço Histórico")
                st.line_chart(df_plot['Close'])

            if 'Returns' in df_plot.columns:
                st.markdown("#### Retornos Mensais")
                st.line_chart(df_plot['Returns'])

            st.markdown("#### Matriz de Confusão")
            st.pyplot(fig_cm)

            st.markdown("#### Curva ROC")
            st.pyplot(fig_roc)

def select_best_k(X_train, y_train, k_range=range(1, 21), n_iter=30):
    best_k = 1
    best_kappa = -1
    for k in k_range:
        scores = []
        for _ in range(n_iter):
            idx = np.random.choice(len(X_train), len(X_train), replace=True)
            Xb, yb = X_train.iloc[idx], y_train.iloc[idx]
            model = KNeighborsClassifier(n_neighbors=k)
            model.fit(Xb, yb)
            preds = model.predict(Xb)
            score = cohen_kappa_score(yb, preds)
            scores.append(score)
        mean_kappa = np.mean(scores)
        if mean_kappa > best_kappa:
            best_kappa = mean_kappa
            best_k = k
    return best_k

def predict_monthly_direction(ticker: str, model_name: str):
    today = datetime.today()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    last_day_prev_month = last_day_prev_month.replace(hour=0, minute=0, second=0, microsecond=0)

    data = yf.download(ticker, period="max", end=first_day_this_month)
    if data.empty:
        return "❌ Sem dados", {"acc_train": 0, "acc_test": 0}, pd.DataFrame(), None, None

    close_m = data['Close'].resample('M').last().rename(columns={'Close': ticker}).ffill()
    high_m = data['High'].resample('M').max().rename(columns={'High': ticker}).ffill()
    low_m = data['Low'].resample('M').min().rename(columns={'Low': ticker}).ffill()
    volume_m = data['Volume'].resample('M').sum().rename(columns={'Volume': ticker}).ffill()

    df = pd.DataFrame(index=close_m.index)
    df['RSI'] = momentum.RSIIndicator(close=close_m[ticker]).rsi()
    df['ATR'] = volatility.AverageTrueRange(high=high_m[ticker], low=low_m[ticker], close=close_m[ticker]).average_true_range()
    df['OBV'] = volume.on_balance_volume(close=close_m[ticker], volume=volume_m[ticker])
    df['MACD'] = trend.MACD(close=close_m[ticker]).macd()
    df['SMA10'] = close_m[ticker].rolling(10).mean()
    df['STD10'] = close_m[ticker].pct_change().rolling(10).std()
    df['EWMA_Close_5'] = close_m[ticker].ewm(span=5, adjust=False).mean()
    df['EWMA_Close_10'] = close_m[ticker].ewm(span=10, adjust=False).mean()
    df['EWMA_Close_22'] = close_m[ticker].ewm(span=22, adjust=False).mean()
    df['EWMA_Volume_5'] = volume_m[ticker].ewm(span=5, adjust=False).mean()
    df['EWMA_Volume_10'] = volume_m[ticker].ewm(span=10, adjust=False).mean()
    df['EWMA_Volume_22'] = volume_m[ticker].ewm(span=22, adjust=False).mean()
    df = df.dropna()

    future_returns = np.log(close_m[ticker].shift(-1) / close_m[ticker]).dropna()
    future_signals = np.where(future_returns > 0, 1, -1)
    y = pd.Series(future_signals, index=future_returns.index)

    common_idx = df.index.intersection(y.index)
    df = df.loc[common_idx].dropna()
    y = y.loc[common_idx]


    split_index = int(len(df) * 0.8)
    X_train, X_test = df.iloc[:split_index], df.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

    if model_name == "KNN":
        best_k = select_best_k(X_train, y_train)
        model = KNeighborsClassifier(n_neighbors=best_k)
        model = KNeighborsClassifier(n_neighbors=2)
    elif model_name == "RF":
        model = RandomForestClassifier(n_estimators=10, random_state=0)
    elif model_name == "SVM":
        model = make_pipeline(StandardScaler(), SVC(probability=True, gamma='auto'))
    else:
        return "❌ Modelo inválido", {"acc_train": 0, "acc_test": 0}, pd.DataFrame(), None, None

    model.fit(X_train, y_train)
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    X_latest = df.iloc[[-1]]
    pred_current = model.predict(X_latest)[0]
    trend_arrow = "📈 Alta provável" if pred_current == 1 else "📉 Baixa provável"

    acc_train = (y_pred_train == y_train).mean()
    acc_test = (y_pred_test == y_test).mean()

    cm = confusion_matrix(y_test, y_pred_test)
    fig_cm, ax_cm = plt.subplots()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Baixa", "Alta"])
    disp.plot(ax=ax_cm)
    ax_cm.set_title("Matriz de Confusão (Mensal)")
    ax_cm.grid(False)

    fig_roc, ax_roc = plt.subplots()
    try:
        if hasattr(model, "predict_proba"):
            y_scores = model.predict_proba(X_test)[:, 1]
        else:
            y_scores = model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_scores)
        roc_auc = auc(fpr, tpr)
        ax_roc.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
        ax_roc.plot([0, 1], [0, 1], "k--")
        ax_roc.set_title("Curva ROC (Mensal)")
        ax_roc.set_xlabel("Falso Positivo")
        ax_roc.set_ylabel("Verdadeiro Positivo")
        ax_roc.legend()
    except Exception:
        ax_roc.text(0.5, 0.5, "Curva ROC não disponível", ha='center')

    df_plot = pd.DataFrame({
        'Close': close_m[ticker],
        'Returns': close_m[ticker].pct_change(),
    })

    # Kappa
    kappa = cohen_kappa_score(y_test, y_pred_test)

    # AUC
    try:
        if hasattr(model, "predict_proba"):
            y_scores = model.predict_proba(X_test)[:, 1]
        else:
            y_scores = model.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_scores)
        roc_auc = auc(fpr, tpr)
    except Exception:
        roc_auc = np.nan

    metrics = {"acc_train": acc_train, "acc_test": acc_test, "kappa": kappa,
        "auc": roc_auc}
    return trend_arrow, metrics, df_plot, fig_cm, fig_roc
