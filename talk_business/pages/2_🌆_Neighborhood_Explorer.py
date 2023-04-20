import streamlit as st

# Read the data
# Plot the data
# Include plot in layout

st.set_page_config(
    page_title="🌆 Neighborhood Explorer",
    layout="wide",
)
from utils.flows import distributions
from utils.sql import neighborhood_explorer as ne

st.markdown("# 🌆 Negihborhood Explorer")


nta_list = ne.get_nta_list()

county = st.radio("County", nta_list["COUNTYFIPS"].unique(), 0, horizontal=True)

ntas = nta_list.query("COUNTYFIPS == @county")["NTANAME"].unique()
nta = st.selectbox("Negihborhood", ntas, 0)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Age", "Income", "Rent", "Race", "Occupation", "Enrollment"]
)

with tab1:
    plot = distributions.plot_distribution("AGE_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)

with tab2:
    plot = distributions.plot_distribution("FAMILY_INCOME_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)

with tab3:
    plot = distributions.plot_distribution("RENT_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)

with tab4:
    plot = distributions.plot_distribution("RACE_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)

with tab5:
    plot = distributions.plot_distribution("OCCUPATION_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)

with tab6:
    plot = distributions.plot_distribution("ENROLLMENT_GROUPS", nta)
    st.plotly_chart(plot, use_container_width=True)
