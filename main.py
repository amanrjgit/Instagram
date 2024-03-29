import instagrapi.exceptions
import numpy as np
import pandas as pd
import pickle
import sklearn
import streamlit as st
import base64
import plotly.graph_objects as go
from instagrapi import Client
import joblib
import warnings
warnings.filterwarnings("ignore")

model = joblib.load(open("rf.pkl","rb"))

#functions
def length(string):
    string = str(string)
    return len(string)

def bio(string):
    if string == 0:
        return 0
    else:
        return 1

def count(string):
    counter = 0
    string = str(string)
    for i in string:
        if i.isdigit():
            counter += 1
        else:
            pass
    return counter

def underscore(string):
    counter = 0
    string = str(string)
    for i in string:
        if i == "_":
            counter += 1
        else:
            pass
    return counter


def details(username):
    try:
        info = client.user_info_by_username(username)
        info = dict(info)
        len_username = length(info["username"])
        len_fullname = length(info["full_name"])
        num_in_username = count(info["username"])
        under_in_username = underscore(info["username"])
        is_bio = bio(info["biography"])
        is_verified = int(info["is_verified"])
        is_private = int(info["is_private"])
        is_business = int(info["is_business"])
        media_count = info["media_count"]
        follower_count = info["follower_count"]
        following_count = info["following_count"]
        profile = info["profile_pic_url"]
        client.logout()
        return (len_username,len_fullname,num_in_username,under_in_username,is_bio,is_verified,is_private,is_business,media_count,follower_count,following_count,profile)

    except instagrapi.exceptions.RateLimitError:
        return 0
    except:
        return (9,9,0,0,True,True,False,True,12809,4320045,23,None)

def figure(val=0):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val*100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Real(in %)", 'font': {'size': 50}},
        delta={'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 250], 'color': 'lavenderblush'},
                {'range': [250, 400], 'color': 'darkviolet'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 490}}))

    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})
    return fig


st.set_page_config(page_title="InstaBot Identifier- Aman Kumar Jaiswar",layout="wide")

# image

main_bg = "bg.jpg"
main_bg_ext = "jpg"

with open(main_bg, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

st.markdown(
    f"""
<style>
.stApp {{
    background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    background-size: cover
}}
</style>
""",
    unsafe_allow_html=True
)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''


col1,col2,col3,col4 = st.columns([1,1,1,3],gap="small")


with col1:
    st.title("InstaBot Identifier")

with col4:
    container = st.container()
    container.text("   ")
    input_data = container.text_input(label="Search for a username",value="instagram")
    container.text("   ")
    container.text("   ")
    if input_data == 0:
        st.warning("Maximum Limit Exceded. Please Try After Sometime.")
    elif input_data == 1:
        st.warning("No user found! Please Check Username.")
    else:
        V = details(input_data)
        output = model.predict_proba([[V[0], V[1], V[2], V[3], V[4], V[5], V[6], V[7], V[8], V[9], V[10]]])
        fig = figure(output[0][0])
        container.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
with col2:
    link = V[11]
    st.text("   ")
    st.text("   ")
    st.image("insta.png", width=90)
    st.markdown(hide_img_fs, unsafe_allow_html=True)

with col1:
    st.metric(label="Followers",value=V[9])
    st.subheader(f"{input_data} is {output[0][0]*100}% real")

with col2:
    st.metric(label="Following",value=V[10])
