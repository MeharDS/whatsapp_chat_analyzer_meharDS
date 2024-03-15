import streamlit as st
import preprocesser, helper_funtions
import matplotlib.pyplot as plt
import seaborn as sns

st.header('* - Whatsapp Chat Analyzer by meharDS - *', divider='rainbow')
st.sidebar.subheader("Upload Whatsapp Chat File.Txt", divider='rainbow')
Time_Formate = st.sidebar.selectbox("What's your Time Formate :",("12-Hours", "24-Hours"), index=None, placeholder="Select an Option")
uploaded_file = st.sidebar.file_uploader('Choose a File')

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    

    if Time_Formate =='12-Hours':
        df = preprocesser.preprocess(data)
        # fetch unique users
        user_list = df['users'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
        selected_user = st.sidebar.selectbox('Show Analysis WRT :', user_list)

    elif Time_Formate =='24-Hours':
        df = preprocesser.preprocess_24(data)
        # fetch unique users
        user_list = df['users'].unique().tolist()
        #user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
        selected_user = st.sidebar.selectbox('Show Analysis WRT :', user_list)

    else:
        st.write('')  
    

    if st.sidebar.button('Show Analysis'):

        st.write('Analysis With Respect to :', selected_user)
        #st.divider()  # 👈 Draws a horizontal rule
        
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper_funtions.fatch_stats(selected_user, df)
        st.subheader("Top Statistics :", divider='rainbow')
        col1, col2, col3, col4 = st.columns(4, gap='large')

        with col1:
            st.header('Total Massages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)

        with col4:
            st.header('Link Shared')
            st.title(num_links)

        st.divider()  # 👈 Draws a horizontal rule

        #Monlty Timeline
        st.subheader('Monlty Timeline :', divider='rainbow')
        montly_timeline=helper_funtions.montly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,3))
        ax.plot(montly_timeline['time'], montly_timeline['massages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.divider()  # 👈 Draws a horizontal rule

        #Daily Timeline
        st.subheader('Daily Timeline :', divider='rainbow')
        daily_timeline=helper_funtions.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,3))
        ax.plot(daily_timeline['only_date'], daily_timeline['massages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.divider()  # 👈 Draws a horizontal rule


        #Activity Map
        st.subheader('Activity Map :', divider='rainbow')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Most Busy Day :')
            busy_day=helper_funtions.busy_day(selected_user, df)
            fig, ax=plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader('Most Busy Month :')
            busy_month=helper_funtions.busy_month(selected_user, df)
            fig, ax=plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.subheader('Activity Heat Map', divider='rainbow')
        activity_heatmap=helper_funtions.activity_heatmap(selected_user, df)
        fig, ax=plt.subplots(figsize=(10,3))
        ax= sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        st.divider()  # 👈 Draws a horizontal rule


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.subheader('Most Busy Users :', divider='rainbow')
            x,Busy_users_df = helper_funtions.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                ax.bar_label(ax.containers[0]) # show valus on bars
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(Busy_users_df)

            st.divider()  # 👈 Draws a horizontal rule

        # WordCloud
        st.subheader('WordCloud :', divider='rainbow')
        df_wc = helper_funtions.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,3))
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.divider()  # 👈 Draws a horizontal rule

        #Most Common words
        st.subheader('Most Common Words :', divider='rainbow')
        most_common_words_df = helper_funtions.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,3))
        ax.barh(most_common_words_df[0], most_common_words_df[1])
        ax.bar_label(ax.containers[0]) # show valus on bars
        st.pyplot(fig)

        st.divider()  # 👈 Draws a horizontal rule

        # emoji analysis
        st.subheader('Emoji Analysis :', divider='rainbow')
        emoji_df = helper_funtions.emoji_analysis(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(10,3))
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        with col2:
            st.dataframe(emoji_df)
        











    







