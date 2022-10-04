import streamlit as st

def on_click(nr, nc):
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(
        np.random.randn(nr, nc),
        columns=('col %d' % i for i in range(nc)))
    st.dataframe(df)

st.title("Query DB")
st.markdown("Click button to query DB and get all data")

n_row = st.number_input("Number of rows", 1, 100, 10)
n_col = st.number_input("Number of columns", 1, 100, 10)
choose = st.button("Query")
if choose:
    on_click(n_row,n_col)