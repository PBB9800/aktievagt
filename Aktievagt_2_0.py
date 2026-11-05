import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Aktievagt 2.2",
    layout="wide"
)

st.title("📈 Aktievagt 2.2")

st.write(
    "Vælg de C25-aktier du vil overvåge."
)

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
    "Tryg": "TRYG.CO",
    "Demant": "DEMANT.CO",
    "GN Store Nord": "GN.CO",
    "NKT": "NKT.CO",
    "Sydbank": "SYDB.CO",
    "Jyske Bank": "JYSK.CO",
    "Netcompany": "NETC.CO",
    "ISS": "ISS.CO",
    "Bavarian Nordic": "BAVA.CO",
    "Royal Unibrew": "RBREW.CO",
    "DFDS": "DFDS.CO"
}

st.subheader("Vælg aktier")

valgte_aktier = []

cols = st.columns(4)

for nr, (navn, ticker) in enumerate(C25.items()):
    with cols[nr % 4]:
        if st.checkbox(navn):
            valgte_aktier.append((navn, ticker))

if st.button("Analyser valgte aktier"):

    rows = []

    for navn, ticker in valgte_aktier:

        try:
            aktie = yf.Ticker(ticker)

            historik = aktie.history(period="1mo")

            if len(historik) == 0:
                continue

            reference = float(
                historik["Close"].iloc[0]
            )

            aktuel = float(
                historik["Close"].iloc[-1]
            )

            udvikling = (
                (aktuel - reference)
                / reference
            ) * 100

            status = "✅ OK"

            if udvikling <= -10:
                status = "🚨 Fald over 10 %"

            elif udvikling <= -5:
                status = "⚠️ Fald over 5 %"

            rows.append(
                [
                    navn,
                    ticker,
                    round(reference, 2),
                    round(aktuel, 2),
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
                "Selskab",
                "Ticker",
                "Reference",
                "Aktuel",
                "Udvikling %",
                "Status"
            ]
        )

        df = df.sort_values(
            "Udvikling %"
        )

        st.subheader("Overvågning")

        st.dataframe(
            df,
            use_container_width=True
        )

        alarmer = df[
            df["Status"] != "✅ OK"
        ]

        st.subheader("Aktive alarmer")

        if len(alarmer):

            for _, række in alarmer.iterrows():

                if række["Udvikling %"] <= -10:
            st.error(
                f"{række['Selskab']} er faldet "
                f"{række['Udvikling %']} %"
            )

        else:

            st.warning(
                f"{række['Selskab']} er faldet "
                f"{række['Udvikling %']} %"
            )

    else:
        st.success(
            "Ingen aktive alarmer"
        )

    valgt_ticker = st.selectbox(
        "Kursgraf",
        df["Ticker"]
    )

    graf = yf.Ticker(
        valgt_ticker
    ).history(period="1y")

    st.subheader("Kursgraf")

    st.line_chart(
        graf["Close"]
    )
