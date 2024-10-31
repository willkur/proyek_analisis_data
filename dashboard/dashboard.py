import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from main import DataAnalyzer, BrazilMapPlotter

# sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("df_ecommerce.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

geolocation = pd.read_csv('geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.title("William Kurniawan")
    st.image("spongebob.jpg")
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

st.title("E-Commerce Public Data Analysis")
st.write("**This is a dashboard for analyzing E-Commerce public data.**")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")

# Daily Orders Plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df["order_approved_at"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
    ax=ax
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)
plt.close(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

with col1:
    total_spend = sum_spend_df["total_spend"].sum()
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = sum_spend_df["total_spend"].mean()
    st.markdown(f"Average Spend: **{avg_spend}**")

# Spend Money Plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sum_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#90CAF9",
    ax=ax
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)
plt.close(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

# Order Items Plot
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5), 
    palette=colors, 
    ax=ax1
)
ax1.set_ylabel(None)
ax1.set_xlabel("Number of Sales", fontsize=80)
ax1.set_title("Most sold products", loc="center", fontsize=90)
ax1.tick_params(axis='y', labelsize=55)
ax1.tick_params(axis='x', labelsize=50)

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), 
    palette=colors, 
    ax=ax2
)
ax2.set_ylabel(None)
ax2.set_xlabel("Number of Sales", fontsize=80)
ax2.invert_xaxis()
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_title("Fewest products sold", loc="center", fontsize=90)
ax2.tick_params(axis='y', labelsize=55)
ax2.tick_params(axis='x', labelsize=50)

st.pyplot(fig)
plt.close(fig)

# Review Score
st.subheader("Review Score")
col1, col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")

# Review Score Plot
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=review_score.index, 
    y=review_score.values, 
    order=review_score.index,
    palette=["#90CAF9" if score == common_score else "#D3D3D3" for score in review_score.index],
    ax=ax
)
ax.set_title("Rating by customers for service", fontsize=15)
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)
plt.close(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["State", "Geolocation"])
color1 = ["#90CAF9"]

with tab1:
    most_common_state = state.customer_state.value_counts().index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=state.customer_state.value_counts().index,
        y=state.customer_count.values, 
        data=state,
        palette=color1,
        ax=ax
    )
    ax.set_title("Number customers from State", fontsize=15)
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)
    plt.close(fig)

with tab2:
    map_plot.plot()
    with st.expander("See Explanation"):
        st.write('The area with the highest number of customers is located in the southern region.')

st.caption('Copyright (C) William Kurniawan 2024')