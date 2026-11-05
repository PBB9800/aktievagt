import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Aktievagt", layout="wide")

st.title("📈 Aktievagt")

st.write("Overvåg aktier og få besked ved fald på 5 % eller 10 %.")

ticker = st.text_input("Aktieticker", "NOVO-B.CO")

reference = st.number_input(
    "Referencekurs",
    min_value=0.0,
    value=500.0,
    step=1.0
)

if st.button("Tjek aktie"):
    try:
        aktie = yf.Ticker(ticker)
        kurs = float(
            aktie.history(period="1d")["Close"].iloc[-1]
        )

        ændring = ((kurs - reference) / reference) * 100

        st.metric(
            "Aktuel kurs",
            f"{kurs:.2f}"
        )

        st.metric(
            "Udvikling",
            f"{ændring:.2f}%"
        )

        if ændring <= -10:
            st.error(
                f"🚨 Alarm: {ticker} er faldet mere end 10 %"
            )

        elif ændring <= -5:
            st.warning(
                f"⚠️ Alarm: {ticker} er faldet mere end 5 %"
            )

        else:
            st.success(
                "Ingen alarm"
            )

        historik = aktie.history(period="1y")

        st.subheader("Kursudvikling")
        st.line_chart(historik["Close"])

    except Exception as e:
        st.error(f"Fejl: {e}")
