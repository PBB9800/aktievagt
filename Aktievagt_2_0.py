import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Aktievagt 2.1",
    layout="wide"
)

st.title("📈 Aktievagt 2.1")

st.write(
    "Overvåg flere aktier samtidig og få advarsel ved fald på 5 % og 10 %."
)

watchlist = st.text_area(
    "Aktier (én ticker pr. linje)",
    value="""NOVO-B.CO
DSV.CO
ORSTED.CO
DANSKE.CO
VWS.CO"""
)

reference = st.number_input(
    "Referencekurs (%)",
    min_value=0,
    max_value=100,
    value=100
)

if st.button("Opdater watchlist"):

    tickers = [
        t.strip()
        for t in watchlist.split("\n")
        if t.strip()
    ]

    rows = []

    for ticker in tickers:

        try:
            aktie = yf.Ticker(ticker)

            historik = aktie.history(period="1mo")

            if len(historik) == 0:
                continue

            aktuel_kurs = float(
                historik["Close"].iloc[-1]
            )

            reference_kurs = float(
                historik["Close"].iloc[0]
            )

            udvikling = (
                (aktuel_kurs - reference_kurs)
                / reference_kurs
            ) * 100

            status = "✅ OK"

            if udvikling <= -10:
                status = "🚨 Fald > 10 %"

            elif udvikling <= -5:
                status = "⚠️ Fald > 5 %"

            rows.append(
                [
                    ticker,
                    round(reference_kurs, 2),
                    round(aktuel_kurs, 2),
                    round(udvikling, 2),
                    status
                ]
            )

        except Exception:
            pass

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Ticker",
                "Reference",
                "Aktuel",
                "Udvikling %",
                "Status"
            ]
        )

        st.subheader("Watchlist")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Alarmer")

        alarmer = df[
            df["Status"] != "✅ OK"
        ]

        if len(alarmer) > 0:

            for _, row in alarmer.iterrows():

                if row["Udvikling %"] <= -10:

                    st.error(
                        f"{row['Ticker']} er faldet "
                        f"{row['Udvikling %']} %"
                    )

                else:

                    st.warning(
                        f"{row['Ticker']} er faldet "
                        f"{row['Udvikling %']} %"
                    )

        else:
            st.success(
                "Ingen aktive alarmer"
            )

        st.subheader("Kursgraf")

        valgt = st.selectbox(
            "Vælg aktie",
            df["Ticker"]
        )

        graf = yf.Ticker(valgt).history(
            period="1y"
        )

        st.line_chart(
            graf["Close"]
        )
