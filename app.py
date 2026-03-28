import streamlit as st

st.title("IPL Predictor")

team1 = st.selectbox("Team 1", ["MI","CSK","RCB","KKR","SRH"])
team2 = st.selectbox("Team 2", ["MI","CSK","RCB","KKR","SRH"])

score = st.number_input("Score")
overs = st.number_input("Overs")
wickets = st.number_input("Wickets")

if st.button("Predict"):
    if score > 150:
        st.success(f"{team1} likely to win")
    else:
        st.warning(f"{team2} likely to win")
