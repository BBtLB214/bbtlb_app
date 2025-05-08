import streamlit as st
from BBtLB_App import prop_picker

st.set_page_config(page_title="BBtLB Optimizer", layout="wide")

st.title("BBtLB Prop Picker")

# Run the simulation and display picks
try:
    sim_df = prop_picker.run_monte_carlo()
    picks = prop_picker.pick_props(sim_df)

    st.subheader("Top Prop Picks")
    for p in picks:
        st.write(p)
except Exception as e:
    st.error(f"Error running prop picker: {e}")
