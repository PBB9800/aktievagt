import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Aktievagt 2.3",
    layout="wide"
)

st.title("📈 Aktievagt 2.3")

st.write(
    "Overvåg C25-aktier og få alarm ved store dagsfald."
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
    "A.P. Møller-Mærsk B": "MAERSK-B.CO",
    "A.P. Møller-Mærsk A": "MAERSK-A.CO",
    "Lundbeck": "HLUN-A.CO",
    "Rockwool B": "ROCK-B.CO",
    "Rockwool A": "ROCK-A.CO",
    "DFDS": "DFDS.CO"
}

valgte = st.multiselect(
    "Vælg aktier",
    list(C25.keys()),
    default=[
        "Novo Nordisk",
        "DSV",
        "Danske Bank"
    ]
)

if st.button("Opdater"):

    resultater = []

    for selskab in valgte:

        ticker = C25[selskab]

        try:

            aktie = yf.Ticker(ticker)

            hist = aktie.history(period="5d")

            if len(hist) < 2:
                continue

            gårsdag = float(hist["Close"].iloc[-2])
            idag = float(hist["Close"].iloc[-1])

            ændring = (
                (idag - gårsdag)
                / gårsdag
            ) * 100

            status = "✅ OK"

            if ændring <= -10:
                status = "🚨 Fald > 10 %"

            elif ændring <= -5:
                status = "⚠️ Fald > 5 %"

            resultater.append(
                [
                    selskab,
                    ticker,
                    round(gårsdag, 2),
                    round(idag, 2),
                    round(ændring, 2),
                    status
                ]
            )

        except Exception:
            pass

    if len(resultater) > 0:

        df = pd.DataFrame(
            resultater,
            columns=[
                "Selskab",
                "Ticker",
                "Gårsdag",
                "I dag",
                "Dagsændring %",
                "Status"
            ]
        )

        df = df.sort_values(
            by="Dagsændring %"
        )

        st.subheader("Overvågning")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Aktive alarmer")

        alarmer = df[
            df["Status"] != "✅ OK"
        ]

        if len(alarmer) == 0:

            st.success(
                "Ingen aktive alarmer"
            )

        else:

            st.dataframe(
                alarmer,
                use_container_width=True
            )

        valgt_aktie = st.selectbox(
            "Vis kursgraf",
            valgte
        )

        graf = yf.Ticker(
            C25[valgt_aktie]
        ).history(period="1y")

        st.subheader(
            f"Kursgraf: {valgt_aktie}"
        )

        st.line_chart(
            graf["Close"]
        )
