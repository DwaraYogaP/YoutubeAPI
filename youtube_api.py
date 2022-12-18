import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from streamlit_option_menu import option_menu

from PIL import Image
import requests
from io import BytesIO

from textblob import TextBlob


# AIzaSyCIaPpLGaclpND5omnwOARYkVREM9tnjwc
# AIzaSyAZSDUm8hWQAZViG3qDCpDvQVJ3EPb9Q2Y
# AIzaSyABe6tx-O5aIOIeG1Bo0L6NIxMhCXQsLEE
# AIzaSyCQp1kPLvmXUnAKAQeBqRScojcyt4GWQww
# AIzaSyCLz6Zd7CV_yHgOZ5_M6dp1Z02RfF2fuSY

api = "AIzaSyAZSDUm8hWQAZViG3qDCpDvQVJ3EPb9Q2Y"
yt = build('youtube', 'v3', developerKey=api)

with st.sidebar:
    choice = option_menu("Menu", ["About", 'Search Video', 'Search Channel', 'Popular Videos', 'Contact'], 
                icons=['house-fill', 'youtube', 'person-fill', 'bar-chart-fill', 'envelope-fill'], menu_icon="menu-button-wide-fill", default_index=1,
                styles={
                    "nav-link-selected": {"background-color": "#00ABB3"},                   
                }
                )


st.title("YOUTUBE API")

def convert_df(df):
    return df.to_csv().encode('utf-8')

if choice == "About": 

    st.markdown("""
    <style>
    #content {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 5px;
        padding-bottom: 40px;
        text-align: justify;
    }
    h1 {
        text-align: center;
    }
    li {
        text-align: justify;
    }
    </style>
    """
    ,unsafe_allow_html=True)

    st.markdown("""
    <div id='content'>
        Fitur-fitur yang tersedia di situs web ini adalah:
        <ol>
            <li>Pencarian video: Pengguna dapat mencari video di YouTube dengan menggunakan kata kunci yang diberikan. Hasil pencarian akan menampilkan daftar video yang sesuai dengan kata kunci tersebut.</li>
            <li>Pencarian channel: Pengguna juga dapat mencari channel di YouTube dengan menggunakan kata kunci yang diberikan. Hasil pencarian akan menampilkan daftar channel yang sesuai dengan kata kunci tersebut.</li>
            <li>Video populer: Selain itu, situs web juga menyediakan fitur untuk menampilkan video-video populer di YouTube. Pengguna dapat mengakses daftar video-video populer di negara tertentu yang tersedia di option menu.</li>
        </ol>

        Untuk mengimplementasikan fitur-fitur ini, situs web ini menggunakan YouTube 
        API untuk mengambil data dari YouTube dan menampilkannya ke pengguna. 
        Dengan menggunakan YouTube API, situs web dapat mengambil data seperti 
        judul video, deskripsi video, thumbnail video, dan banyak lagi.
    </div>
    """,
    unsafe_allow_html=True)

if choice == "Search Video":

    st.markdown("""
    <style>
    h1 {
        text-align:center;
    }
    </style>
    """
    ,unsafe_allow_html=True)

    searchVideo = st.text_input("Masukkan teks")
    option = st.radio("Video Duration", ('Default', 'Short', 'Medium', 'Long'))
    slider3 = st.slider("Hasil", 1, 50)
    if st.button("Cari", key=slider3+1):
        if option == 'Default':
            search = yt.search().list(part='snippet',maxResults=slider3, q=searchVideo, type='video', regionCode='ID')
            search_response = search.execute()
        elif option == 'Short':
            search = yt.search().list(part='snippet',maxResults=slider3, q=searchVideo, type='video', regionCode='ID', videoDuration='short')
            search_response = search.execute()  
        elif option == 'Medium':
            search = yt.search().list(part='snippet',maxResults=slider3, q=searchVideo, type='video', regionCode='ID', videoDuration='medium')
            search_response = search.execute()   
        elif option == 'Long':
            search = yt.search().list(part='snippet',maxResults=slider3, q=searchVideo, type='video', regionCode='ID', videoDuration='long')
            search_response = search.execute()
        
        dataFrame2 = pd.json_normalize(search_response['items'])
        csv = convert_df(dataFrame2[['id.videoId', 'snippet.channelId', 'snippet.title', 'snippet.publishedAt', 'snippet.description']])

        st.download_button(
            label="Download data",
            data=csv,
            file_name='search video.csv',
            mime='text/csv',
        )
        videoId = dataFrame2['id.videoId']
        idVideo = []
        for data in videoId:
            idVideo.append(data)
        button = []
        for data in range(50):
            button.append(data)

        for data in range(len(idVideo)):
            request = yt.videos().list(part="snippet,contentDetails,statistics", regionCode="ID", id=idVideo[data])
            response = request.execute()

            df3 = pd.json_normalize(response['items'])

            _id = df3['id']
            id = []
            for data in _id:
                id.append(data)

            channelTitle = df3['snippet.channelTitle']
            idTitle = []
            for data in channelTitle:
                x = data.replace(" ", "")
                idTitle.append(x)

            title_data = df3['snippet.title']
            title = []
            for data in title_data:
                title.append(data)
            
            thumbnail_url = df3['snippet.thumbnails.high.url']
            thumbnail = []
            for data in thumbnail_url:
                thumbnail.append(data)
            
            desc_data = df3['snippet.description']
            desc = []
            for data in desc_data:
                desc.append(data)

            view_count = df3['statistics.viewCount']
            view = []
            for data in view_count:
                view.append(data)
            
            like_count = df3['statistics.likeCount']
            like = []
            for data in like_count:
                like.append(data)
            
            comment_count = df3['statistics.commentCount']
            comment = []
            for data in comment_count:
                comment.append(data)
 
            for i in range(len(title)):
                st.subheader(title[i])

                videoLink = f"https://www.youtube.com/watch?v={id[i]}&ab_channel={idTitle[i]}"
                st.video(videoLink)


                st.text("Deskripsi : ")
                st.write(desc[i])
                analysis = TextBlob(desc[i])
                if analysis.sentiment.polarity > 0.0:
                    st.info("Sentiment Analysis : Positif")
                elif analysis.sentiment.polarity == 0.0:
                    st.info("Sentiment Analysis : Netral")
                else:
                    st.info("Sentiment Analysis : Negatif")

                col1, col2, col3 = st.columns(3)
                col1.metric("View", view[i])
                col2.metric("Like Count", like[i])
                col3.metric("Comment Count", comment[i])

                # if st.button("Lihat Komentar", key=button[i]):
                comment_search = yt.commentThreads().list(part='snippet', videoId=id[i])
                comment_response = comment_search.execute()
                df = pd.json_normalize(comment_response['items'])

                st.write(df[['snippet.topLevelComment.snippet.authorDisplayName', 'snippet.topLevelComment.snippet.textOriginal']])


if choice == "Search Channel":

    st.markdown("""
    <style>
    h1 {
        text-align:center;
    }
    </style>
    """
    ,unsafe_allow_html=True)

    search2 = st.text_input("Masukkan teks")
    slider2 = st.slider("Jumlah", 1, 50)
    if st.button("Cari", key=0):
        search = yt.search().list(part='snippet',maxResults=slider2, q=search2, type='video', regionCode='ID')
        search_response = search.execute()
        dataFrame = pd.json_normalize(search_response['items'])
        
        channelid = dataFrame['snippet.channelId']
        idChannel = []
        for data in channelid:
            idChannel.append(data)
        
        for i in range(len(idChannel)):
            channel = yt.channels().list(part='snippet,contentDetails,statistics', id=idChannel[i])
            response = channel.execute()
            
            df2 = pd.json_normalize(response['items'])

            title_data = df2['snippet.title']
            title = []
            for data in title_data:
                title.append(data)

            desc_data = df2['snippet.description']
            desc = []
            for data in desc_data:
                desc.append(data)
            
            date_data = df2['snippet.publishedAt']
            date = []
            for data in date_data:
                date.append(data)
            
            image_data = df2['snippet.thumbnails.high.url']
            image = []
            for data in image_data:
                image.append(data)

            
            #STATISTICS
            view_data = df2['statistics.viewCount']
            view = []
            for data in view_data:
                view.append(data)
            
            subscriber_data = df2['statistics.subscriberCount']
            subs = []
            for data in subscriber_data:
                subs.append(data)
            
            video_data = df2['statistics.videoCount']
            video = []
            for data in video_data:
                video.append(data)
            
            for i in range(len(title)):
                st.subheader(title[i])

                response = requests.get(image_data[i])
                image = Image.open(BytesIO(response.content))
                st.image(image)
                
                st.text("Deskripsi Channel: ")
                st.write(desc[i])
                st.write("Dibuat pada : " + date[i])

                col1, col2, col3 = st.columns(3)
                col1, col2, col3 = st.columns(3)
                col1.metric("View", view[i])
                col2.metric("Like Count", subs[i])
                col3.metric("Comment Count", video[i])
    

if choice == "Popular Videos":

    st.markdown("""
    <style>
    h1 {
        text-align:center;
    }
    </style>
    """
    ,unsafe_allow_html=True)

    slider = st.slider("Hasil", 1, 50)
    region = st.selectbox("Negara", ["Australia", "Brazil", "Canada", "Dominican Republik", "Egypt", "France", "Germany", "Hong Kong", "Indonesia", "United States"], index=8)
    if region == "Australia":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="AU", maxResults=slider)
        response = request.execute()
    elif region == "Brazil":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="BR", maxResults=slider)
        response = request.execute()
    elif region == "Canada":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="CA", maxResults=slider)
        response = request.execute()
    elif region == "Dominican Republik":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="DO", maxResults=slider)
        response = request.execute()
    elif region == "Egypt":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="EG", maxResults=slider)
        response = request.execute()
    elif region == "France":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="FR", maxResults=slider)
        response = request.execute()
    elif region == "Germany":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="DE", maxResults=slider)
        response = request.execute()
    elif region == "Hong Kong":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="HK", maxResults=slider)
        response = request.execute()
    elif region == "Indonesia":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="ID", maxResults=slider)
        response = request.execute()
    elif region == "United States":
        request = yt.videos().list(part="snippet,contentDetails,statistics", chart="mostPopular", regionCode="US", maxResults=slider)
        response = request.execute()
        
    df = pd.json_normalize(response['items'])
    
    idVideo = df['id']
    videoId = []
    for data in idVideo:
        videoId.append(data)
    
    for data in range(len(idVideo)):
            request = yt.videos().list(part="snippet,contentDetails,statistics", regionCode="ID", id=videoId[data])
            response = request.execute()

            df3 = pd.json_normalize(response['items'])

            _id = df3['id']
            id = []
            for data in _id:
                id.append(data)

            channelTitle = df3['snippet.channelTitle']
            idTitle = []
            for data in channelTitle:
                x = data.replace(" ", "")
                idTitle.append(x)

            title_data = df3['snippet.title']
            title = []
            for data in title_data:
                title.append(data)
            
            thumbnail_url = df3['snippet.thumbnails.high.url']
            thumbnail = []
            for data in thumbnail_url:
                thumbnail.append(data)
            
            desc_data = df3['snippet.description']
            desc = []
            for data in desc_data:
                desc.append(data)

            view_count = df3['statistics.viewCount']
            view = []
            for data in view_count:
                view.append(data)
            
            like_count = df3['statistics.likeCount']
            like = []
            for data in like_count:
                like.append(data)
            
            comment_count = df3['statistics.commentCount']
            comment = []
            for data in comment_count:
                comment.append(data)

            
            
            for i in range(len(title)):
                st.subheader(title[i])

                videoLink = f"https://www.youtube.com/watch?v={id[i]}&ab_channel={idTitle[i]}"
                st.video(videoLink)


                st.text("Deskripsi : ")
                st.write(desc[i])

                col1, col2, col3 = st.columns(3)
                col1.metric("View", view[i])
                col2.metric("Like Count", like[i])
                col3.metric("Comment Count", comment[i])

                # if st.button("Lihat Komentar", key=button[i]):
                comment_search = yt.commentThreads().list(part='snippet', videoId=id[i])
                comment_response = comment_search.execute()
                df = pd.json_normalize(comment_response['items'])

                st.write(df[['snippet.topLevelComment.snippet.authorDisplayName', 'snippet.topLevelComment.snippet.textOriginal']])
    
    
if choice == 'Contact':
    
    st.markdown(
        """
        <style>
            h1 {
                text-align: center;
            }
            .contact-box {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 20px;
                margin: 20px 0;
                margin-bottom: 50px;
            }

            ul li a:hover {
                color: white;
            }
        </style>
        """
        , unsafe_allow_html=True)

   
    st.header("Contact Information")

    st.markdown(
        """
        <div class="contact-box">
        To contact the developer, please send an email to <a href="mailto:dwarayoga.2020@student.uny.ac.id">dwarayoga.2020@student.uny.ac.id</a>.
        <br><br>
        You can also follow us on social media:
        <ul>
            <li><a href="https://twitter.com/dwara_pradana">Twitter</a></li>
            <li><a href="https://www.facebook.com/dwara.pradana/">Facebook</a></li>
            <li><a href="https://www.instagram.com/dwara_yoga_pradana/">Instagram</a></li>
        </ul>
        </div>
        """
        , unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("foto.png", width=200)
    with col3:
        st.write(' ')

    st.markdown(
    """
    <style>
    #footer {
        text-align: center;
        padding-bottom: 10px;
        border: 0.5px solid lightblue;
        border-radius: 5px;
        margin-top: 50px;
    }
    footer {
        visibility: hidden;
    }
    </style>

    <div id='footer'>Copyright &copy;2022 by Dwara Yoga Pradana</div>
    """
    , unsafe_allow_html=True)

