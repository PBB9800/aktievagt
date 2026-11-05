import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Aktievagt 2.3",
    layout="wide"
)

st.title("📈 Aktievagt 2.3")

st.write(
    "Scanner C25 og fremhæver dagens største kursfald."
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

rows = []

with st.spinner("Henter kurser..."):

    for selskab, ticker in C25.items():

        try:

            hist = yf.Ticker(
                ticker
            ).history(period="5d")

            if len(hist) < 2:
                continue

            gårsdag = float(
                hist["Close"].iloc[-2]
            )

            idag = float(
                hist["Close"].iloc[-1]
            )

            ændring = (
                (idag - gårsdag)
                / gårsdag
            ) * 100

            rows.append([
                selskab,
                ticker,
                round(gårsdag, 2),
                round(idag, 2),
                round(ændring, 2)
            ])

        except Exception:
            pass

if len(rows) > 0:

    df = pd.DataFrame(
        rows,
        columns=[
            "Selskab",
            "Ticker",
            "Gårsdag",
            "I dag",
            "Dagsændring %"
        ]
    )

    df = df.sort_values(
        by="Dagsændring %"
    )

    store_fald = df[
        df["Dagsændring %"] <= -10
    ]

    mellem_fald = df[
        (df["Dagsændring %"] > -10)
        & (df["Dagsændring %"] <= -5)
    ]

    st.subheader("🚨 Fald større end 10 %")

    if len(store_fald) == 0:

        st.success(
            "Ingen C25-aktier er faldet mere end 10 % i dag."
        )

    else:

        st.dataframe(
            store_fald,
            use_container_width=True
        )

    st.subheader("⚠️ Fald mellem 5 % og 10 %")

    if len(mellem_fald) == 0:

        st.success(
            "Ingen C25-aktier er faldet mellem 5 % og 10 % i dag."
        )

    else:

        st.dataframe(
            mellem_fald,
            use_container_width=True
        )

    st.subheader("📊 Hele C25")

    st.dataframe(
        df,
        use_container_width=True
    )

    valgt = st.selectbox(
        "📈 Vis kursgraf",
        df["Selskab"]
    )

    ticker = C25[valgt]

    graf = yf.Ticker(
        ticker
    ).history(period="1y")

    st.subheader(
        f"Kursgraf: {valgt}"
    )

    st.line_chart(
        graf["Close"]
    )
