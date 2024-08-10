import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='COE dashboard',
    page_icon=':car:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.


@st.cache_data
def get_coe_data():
    DATA_FILENAME = Path(__file__).parent/'data/coe_parsed.csv'
    coe_df = pd.read_csv(DATA_FILENAME, parse_dates=["date"])
    print(coe_df.head())
    return coe_df


coe_df = get_coe_data()


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :car: COE dashboard

Browse COE data from the [Data.gov.sg](https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view) website.
'''

# Add some spacing
''
''

min_value = coe_df['year'].min()
max_value = coe_df['year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[max_value - 4, max_value])

vehicle_class = coe_df['vehicle_class'].unique()

if not len(vehicle_class):
    st.warning("Select at least one category")

selected_class = st.multiselect(
    'Which vehicle class would you like to view?',
    vehicle_class,
    ['Category A', 'Category B'])


''
''

# Filter the data
filtered_coe_df = coe_df[
    (coe_df['vehicle_class'].isin(selected_class))
    & (coe_df['year'] <= to_year)
    & (from_year <= coe_df['year'])
]

st.header('COE over time', divider='gray')

''

st.line_chart(
    filtered_coe_df,
    x='date',
    y='premium',
    color='vehicle_class',
)

st.markdown(
    """
ℹ️ Vehicle class TLDR: 
- Category A: small car
- Category B: big car
- Category C: bus
- Category D: motorcycle
- Category E: open category
    """
)
