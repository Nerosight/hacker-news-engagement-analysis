import pandas as pd
import streamlit as st
from streamlit import header, pyplot
import matplotlib.pyplot as plt
import numpy as np
st.set_page_config(page_title="Hacnker Posts page analysis", layout="wide")



st.markdown("""
## Project Overview

This project explores engagement patterns on the site Hacker News from a dataset on Kaggle on the posts 
made between 9/6/2016 & 9/6/2015 
analyzing how post characteristics, contributor behavior, and timing relate to community response. 
Using a dataset of Hacker News submissions, the analysis examines relationships between discussion activity, upvote performance, and posting time to identify observable trends in user engagement.

The project begins with an exploration of the relationship between the number of comments and the number of points a post receives, highlighting how discussion and approval represent distinct forms of interaction. It then investigates temporal patterns by analyzing posting volume and average engagement across hours of the day, providing insight into how user activity fluctuates over time.

To further contextualize engagement, contributor-level analysis is performed to identify authors who consistently generate high impact, followed by inspection of their top-performing post titles. Finally, selected high-engagement posts are compared with external Google Trends data to assess whether public interest in related topics aligns with post performance at the time of publication.

All findings are presented through an interactive Streamlit dashboard, allowing for transparent exploration of the data while emphasizing observational insights rather than causal claims.""")




st.title("Omar's Data Analysis p1")

@st.cache_data
def load_data():
    return pd.read_csv("data/HN_posts_year_to_Sep_26_2016.csv")

df = load_data()

min_points = st.slider(
    "Minimum number of Points",
    min_value = 2,
    max_value= int (df["num_points"].max()),
    value = 0
)
filtered_df = df[df["num_points"] >= min_points]


st.header("Comments VS Points")

Y = filtered_df["num_points"]
X = filtered_df["num_comments"]

fig, ax = plt.subplots()

ax.scatter(X,Y, alpha = 0.4, s = 12)


m,b = np.polyfit(X,Y,1)
ax.plot(X, m * X + b)


ax.set_xlabel("Number of Comments", color = 'green')
ax.set_ylabel("Number of Points")

st.pyplot(fig)

st.subheader("The plot shows a positive but highly dispersed relationship between the number of comments"
         "and the number of points. While posts that receive more comments tend to mass more points on average, as reflected"
         "by the positive up ward slopping trend line.\n"
             )
st.subheader(
         "But there is a wide spread of variability in the data, Many posts with similar comment count have different number of points"
         "suggesting that volume of discussion is not enough for approval.\n")
st.subheader( "Additionally, a small number of High-comment, High-points outliers appear influencing the trend.")

st.space()
st.space()
st.space()




st.title("Curiosity of peak post times")
st.markdown("""
Here we check if there's a significant difference between getting points on posts that are created at higher VS lower traffic hours.""")
df["created_at"] = pd.to_datetime(df["created_at"], errors = "coerce")

df["hour"] = df["created_at"].dt.hour

group_sizes = df.groupby('hour').size()

st.bar_chart(group_sizes)


st.subheader("Looking into the average points each hour has")

avg_points_hourly = df.groupby("hour")['num_points'].mean()

avg_comments_hourly = df.groupby("hour")['num_comments'].sum()
st.line_chart(avg_points_hourly)

st.space(3)
st.line_chart(avg_comments_hourly)
st.space(3)
st.space(3)
st.title("Looking Into Authors and Their Stats")

#Here I plan to see the top 5 authors in number of posts, and top 5 in umber of points

top_auth_posts = (
    df.groupby("author").size().sort_values(ascending = False).head(5)
)

top_auth_points = (
    df.groupby("author")["num_points"].sum().sort_values(ascending = False).head(5)
)


st.subheader("This table is for the top 5 authors that posted within the time frame of the dataset")
st.write(top_auth_posts)

st.write(top_auth_points)
st.subheader("This table is for the top 5 authors that received points within the time frame of the dataset")

st.markdown("""
**We see 3 authors consistently:**
- jonbaer
- ingve
- prostoalex

I'd like to check ingve's post titles and dive into their top posts since he has the second most posts but by far
the most amount of points by an incredible margin
""")

#Get the names of the authors with the most points
top_auth_points = (
    df.groupby("author")["num_points"].sum().sort_values(ascending = False).head(1)
)
#Single out the name
top_auth_name = top_auth_points.index[0]

#Search the dataset for this author's posts
author_posts = df[df["author"] == top_auth_name]

sorted_auth_posts = author_posts.sort_values("num_points",ascending= False)


st.markdown(f"""# The top post titles by {top_auth_name}""")

st.dataframe(
    sorted_auth_posts[["title", "num_points"]].head(10)
)

st.markdown("""## I am interested in comparing google trends to the post title's keywords and see if its a point of correlation""")



@st.cache_data
def load_trends():
    af = pd.read_csv("data/multiTimeline.csv", skiprows=1)
    af.columns = ["date", "interest"]
    af["date"] = pd.to_datetime(af["date"])
    af["interest"] = pd.to_numeric(af["interest"], errors="coerce")
    return af

googl_trends_data = load_trends()
googl_trends_data = googl_trends_data.sort_values("date")
Top_date = sorted_auth_posts.iloc[0]["created_at"]
st.subheader(f"For the number one post: Xamarin now free in Visual Studio, and Xamarin SDK being open-sourced on the date {Top_date}")


st.line_chart(googl_trends_data.set_index("date")["interest"])
st.write("The trends show before Mar 01 a downtrend which then is followed up with a spike of interest to 90 in Jun 01, which is within the post's creation date.")