import streamlit as st
from BBtLB_Optimizer import prop_picker

st.title("BBtLB Prop Picker")

try:
    sim_df = prop_picker.run_monte_carlo()
    picks = prop_picker.pick_props(sim_df)

    st.subheader("Top Prop Picks")
    for p in picks:
        st.write(p)
except Exception as e:
    st.error(f"An error occurred: {e}")