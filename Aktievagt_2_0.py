import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Aktievagt 2.2", layout="wide")

st.title("📈 Aktievagt 2.2")

C25 = {
    "Novo Nordisk": "NOVO-B.CO",
    "DSV": "DSV.CO",
    "Vestas": "VWS.CO",
    "Danske Bank": "DANSKE.CO",
    "Ørsted": "ORSTED.CO",
    "Coloplast": "COLO-B.CO",
    "Pandora": "PNDORA.CO",
    "Genmab": "GMAB.CO",
    "Carlsberg": "CARL-B.CO",
    "Tryg": "TRYG.CO"
}

valgte = st.multiselect(
    "Vælg aktier",
    list(C25.keys()),
    default=["Novo Nordisk", "DSV"]
)

if st.button("Opdater"):

    data = []

    for navn in valgte:

        ticker = C25[navn]

        try:
            aktie = yf.Ticker(ticker)

            hist = aktie.history(period="1mo")

            if len(hist) == 0:
                continue

            reference = float(hist["Close"].iloc[0])
            aktuel = float(hist["Close"].iloc[-1])

            udvikling = (
                (aktuel - reference)
                / reference
            ) * 100

            status = "✅ OK"

            if udvikling <= -10:
                status = "🚨 -10%"

            elif udvikling <= -5:
                status = "⚠️ -5%"

            data.append([
                navn,
                round(reference, 2),
                round(aktuel, 2),
                round(udvikling, 2),
                status
            ])

        except Exception:
            pass

    if len(data) > 0:

        df = pd.DataFrame(
            data,
            columns=[
                "Selskab",
                "Reference",
                "Aktuel",
                "Udvikling %",
                "Status"
            ]
        )

        st.dataframe(df, use_container_width=True)

        st.subheader("Aktive alarmer")

        alarmer = df[df["Status"] != "✅ OK"]

        if len(alarmer) == 0:
            st.success("Ingen aktive alarmer")

        else:
            st.dataframe(
                alarmer,
                use_container_width=True
            )

        valgt = st.selectbox(
            "Vis kursgraf",
            valgte
        )

        graf = yf.Ticker(
            C25[valgt]
        ).history(period="1y")

        st.line_chart(
            graf["Close"]
        )
