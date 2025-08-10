import pandas as pd
import numpy as np
import plotly.express as px
from utils.routing.distances import (
	distance_picking,
	next_location
)
from utils.routing.routes import (
	create_picking_route
)
from utils.batch.mapping_batch import (
	orderlines_mapping,
	locations_listing
)
from utils.cluster.mapping_cluster import (
	df_mapping
)
from utils.batch.simulation_batch import (
	simulation_wave,
	simulate_batch
)
from utils.cluster.simulation_cluster import(
	loop_wave,
	simulation_cluster,
	create_dataframe,
	process_methods
)
from utils.results.plot import (
	plot_simulation1,
	plot_simulation2
)
import streamlit as st
from streamlit import caching

# Set page configuration
st.set_page_config(page_title ="Improve Warehouse Productivity using Order Batching",
                    initial_sidebar_state="expanded",
                    layout='wide',
                    page_icon="🛒")

# Set up the page
@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner= True)
# Preparation of data
def load(filename, n):
    df_orderlines = pd.read_csv(IN + filename).head(n)
    return df_orderlines