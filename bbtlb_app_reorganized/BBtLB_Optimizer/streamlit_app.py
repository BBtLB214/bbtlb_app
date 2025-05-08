# BBtLB_Optimizer/streamlit_app.py

import streamlit as st
import pandas as pd
import sys
import os

# Ensure root path is in sys.path for import compatibility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BBtLB_Optimizer import prop_picker, ownership_leverage, dk_fd_builder, projection_engine

st.set_page_config(page_title="BBtLB Optimizer", layout="wide")
st.title("🏈 BBtLB Optimizer Dashboard")

module = st.sidebar.selectbox("Select Module", [
    "Prop Picker",
    "Ownership Leverage",
    "DK/FD Lineup Builder",
    "Projection Engine"
])

if module == "Prop Picker":
    st.subheader("🎯 Prop Picker")
    sim_df = prop_picker.run_monte_carlo()
    picks = prop_picker.pick_props(sim_df)
    st.dataframe(pd.DataFrame(picks))

elif module == "Ownership Leverage":
    st.subheader("📊 Ownership Leverage")
    ownership_leverage.main()
    st.success("Check logs or console for printed output.")

elif module == "DK/FD Lineup Builder":
    st.subheader("🧮 DK/FD Lineup Builder")
    st.warning("Lineup builder integration pending.")

elif module == "Projection Engine":
    st.subheader("🔍 Projection Engine")
    projections = projection_engine.generate_projections()
    st.dataframe(pd.DataFrame(projections))
