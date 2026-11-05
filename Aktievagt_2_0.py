import streamlit as st
import yfinance as yf
import pandas as pd

from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Aktievagt 2.4",
    layout="wide"
)

st_autorefresh(
    interval=300000,
    key="refresh"
)

st.title("📈 Aktievagt 2.4")

st.caption(
    f"Sidst opdateret: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

st.write(
    "Scanner C25 og vurderer selskabernes kvalitet med en Buffett-inspireret score."
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

data = []

with st.spinner("Scanner C25..."):

    for selskab, ticker in C25.items():

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

            info = aktie.info

            score = 0

            roe = info.get("returnOnEquity")
            margin = info.get("profitMargins")
            pe = info.get("trailingPE")
            fcf = info.get("freeCashflow")
            debt = info.get("debtToEquity")

            if roe and roe > 0.15:
                score += 20

            if margin and margin > 0.15:
                score += 20

            if fcf and fcf > 0:
                score += 20

            if debt and debt < 100:
                score += 20

            if pe and pe < 25:
                score += 20

            kategori = "Lav"

            if score >= 80:
                kategori = "⭐⭐⭐ Høj"

            elif score >= 60:
                kategori = "⭐⭐ God"

            elif score >= 40:
                kategori = "⭐ Middel"

            status = "✅"

            if ændring <= -10:
                status = "🚨"

            elif ændring <= -5:
                status = "⚠️"

            data.append([
                selskab,
                round(idag, 2),
                round(ændring, 2),
                score,
                kategori,
                status
            ])

        except Exception:
            pass

if len(data) > 0:

    df = pd.DataFrame(
        data,
        columns=[
            "Selskab",
            "Kurs",
            "Dagsændring %",
            "Buffett-score",
            "Kvalitet",
            "Alarm"
        ]
    )

    st.subheader("🚨 Dagens muligheder")

    muligheder = df[
        (df["Dagsændring %"] <= -5)
    ].sort_values(
        by=["Buffett-score"],
        ascending=False
    )

    if len(muligheder):

        st.dataframe(
            muligheder,
            use_container_width=True
        )

    else:

        st.success(
            "Ingen C25-aktier er faldet mere end 5 % i dag."
        )

    st.subheader("📊 Hele C25")

    st.dataframe(
        df.sort_values(
            by="Dagsændring %"
        ),
        use_container_width=True
    )

    valgt = st.selectbox(
        "📈 Vælg aktie",
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

    info = yf.Ticker(
        ticker
    ).info

    st.subheader("🏦 Buffett-analyse")

    roe = info.get("returnOnEquity")
    margin = info.get("profitMargins")
    pe = info.get("trailingPE")
    debt = info.get("debtToEquity")

    col1, col2, col3, col4
