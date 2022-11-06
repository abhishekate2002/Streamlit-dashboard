import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard",page_icon=":bar_chart:",layout="wide")

df = pd.read_excel(
    io='train1.xlsx',
    engine='openpyxl',
    sheet_name='train',
    skiprows=0, 
    usecols= 'A:L',
    nrows=100
)


st.sidebar.header("Please Fitere Here")

city = st.sidebar.multiselect("Select the City: ",
 options=df["City_Category"].unique(),
default=df["City_Category"].unique())

marital_status = st.sidebar.multiselect("Select the marriage status 0(single), 1(married) : ",
 options=df["Marital_Status"].unique(),
default=df["Marital_Status"].unique())

gender = st.sidebar.multiselect("Select the Gender: ",
 options=df["Gender"].unique(),
default=df["Gender"].unique())

df_selection = df.query(
    "City_Category == @city & Marital_Status == @marital_status & Gender == @gender "
)

st.dataframe(df_selection)

st.title(":bar_chart: Sales Dashboard")
st.markdown('##')

total_sales = int(df_selection["Purchase"].sum())
average_rating = round(df_selection["Product_Category_2"].mean(),1)
star_rating = ":star"*int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Purchase"].mean(),2)

left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales: ")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales for Transactions: ")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

sales_by_product_line = (
    df_selection.groupby(by=["Product_ID"]).sum()[["Purchase"]].sort_values(by="Purchase")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Purchase",
    y = sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083BB"]*len(sales_by_product_line),
    template="plotly_white",

)
fig_product_sales.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis= (dict(showgrid=False))
)
st.plotly_chart(fig_product_sales)


hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)