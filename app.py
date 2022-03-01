import matplotlib.pyplot as plt
import emoji
from PIL import Image
from pandas import pivot_table
import seaborn as sns
import streamlit as st
import preprocessor
import helper


image = Image.open("E:\Projects\whatsApp\WhatsAppChatAnalysis\\background.jpg")
st.title("WhatsApp Chat Analyzer")
st.image(image, width=500)
uploaded_file= st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data= uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    # st.text(data)
    df= preprocessor.preprocess(data=data)

    # st.dataframe(df)


    # fetch unique users
    user_list= df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user= st.sidebar.selectbox("Show Analysis With Respect To", user_list)



    # Chat Stats

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        num_messages, num_words, num_media_messages, num_links= helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words Texted")
            st.title(num_words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links Shared")
            st.title(num_links)


        # monthly timeline
        timeline= helper.monthly_timeline(
            selected_user, df
        )
        fig, axis = plt.subplots()
        axis.plot(timeline['time'], timeline['message'], color= "green")
        plt.xticks(rotation='vertical')

        st.title("Monthly Timeline")
        st.pyplot(fig)

        # Daily timeline
        daily_timeline= helper.daily_timeline(
            selected_user, df
        )
        fig, axis = plt.subplots()
        axis.plot(daily_timeline['day_num'], daily_timeline['message'], color= "Purple")
        plt.xticks(rotation='vertical')

        st.title("Daily Timeline")
        st.pyplot(fig)


        # Activity Map
        st.title("Activity Map")
        col1, col2= st.columns(2)
        with col1: 
            # st.header("Most Busy Day")
            busy_day= helper.week_activity_map(selected_user, df)
            if not busy_day.empty:
                fig, axis = plt.subplots()
                axis.bar(busy_day.index,
                        busy_day.values, color="magenta")
                plt.xticks(rotation='vertical')

                st.subheader("Most Busy Day")
                st.pyplot(fig)
        with col2: 
            # st.header("Most Busy Day")
            busy_month= helper.month_activity_map(selected_user, df)
            if not busy_month.empty:
                fig, axis = plt.subplots()
                axis.bar(busy_month.index,
                        busy_month.values, color="blue")
                plt.xticks(rotation='vertical')

                st.subheader("Most Busy Month")
                st.pyplot(fig)

        pivot_table= helper.activity_heatmap(selected_user, df)
        if not pivot_table.empty:
            st.header("Weekly Activity Heatmap")
            fig, axis = plt.subplots()
            cmap = sns.color_palette("magma", as_cmap=True)
            axis= sns.heatmap(pivot_table, cmap= cmap)
            st.pyplot(fig)


        # finding the busiest users in the group
        if selected_user =='Overall':
            st.title('Most Busy Users')
            x, new_df= helper.most_busy_users(df)
            fig, axis= plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                axis.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # most common words 
        most_common_df= helper.most_common_words(selected_user, df)
        if not most_common_df.empty:
            fig, axis= plt.subplots()
            axis.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation= 'vertical')
            
            st.title("Most Common Words")
            st.pyplot(fig)
            # st.dataframe(most_common_df)

    if st.sidebar.button("Emoji Data Analysis"):
        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emoji Analysis')
        if not emoji_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, axis = plt.subplots()
                # axis.pie(emoji_df['Usage'], labels= emoji_df['Emoji'], autopct='%.2f')
                axis.pie(emoji_df['Usage'], labels=emoji_df['Emoji'])
                st.pyplot(fig)
        else:
            st.subheader("No Emojis In The Selected Chat " +
                         emoji.emojize(":grinning_face_with_big_eyes:", use_aliases=True))


    if st.sidebar.button("Show Chat Data"):
        st.header("CHAT DATA")
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]
        new_df = df[["user", 'date', 'message']]
        st.dataframe(df[["user", 'date', 'message']])



    