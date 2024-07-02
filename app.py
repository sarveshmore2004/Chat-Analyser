import pandas as pd
import streamlit as st
from preprocess import preprocess_data
# from preprocess import analyze_format
import helper

import streamlit as st

def sidebar_instructions():
    st.sidebar.write("***Click the X button above to close the instructions guide.***")
    st.sidebar.divider()
    st.sidebar.title("Quick Start Guide")

    st.sidebar.header("Step 1: Export & Upload Your Chat")
    st.sidebar.write("- Open the chat you want to export in the WhatsApp mobile app.")
    st.sidebar.write("  - Tap ⋮ or ⋯, select 'More' > 'Export chat', choose 'Without Media', and save the file.")
    st.sidebar.write("- Extract the .zip file to get the .txt file.")
    st.sidebar.write("- Go to the home page, click 'Upload Chat File', and select the .txt file.")

    st.sidebar.header("Step 2: Select Date Format")
    st.sidebar.write("- Choose the appropriate date format of your chat by selecting the corresponding radio button.")
    st.sidebar.write("- If numerous errors occur, try selecting a format that results in zero errors.")

    st.sidebar.header("Step 3: Select Analysis Option")
    st.sidebar.write("- Click on the radio button next to your preferred analysis option.")

    st.sidebar.header("Step 4: Analyze Chat")
    st.sidebar.write("- Choose a user from the dropdown menu.")
    st.sidebar.write("- Click 'Show Analytics'.")
    st.sidebar.write("- Click on the expanders to reveal specific analysis insights (Overview, Detailed Analysis, Temporal Analysis).")

    st.sidebar.write("OR")

    st.sidebar.header("Step 4: Predict Message Sender")
    st.sidebar.write("- Input a message to predict the sender and press Enter.")
    st.sidebar.write("- Click 'Train the Model Again' to retrain if the accuracy is low.")



st.set_page_config(
    page_title="ChatAnalyser",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.header("WhatsApp Chat Analyser")
st.title('WhatsApp Chat Analyser')
st.text('Explore your chat data and predict message senders.')

# st.set_sidebar_property("expanded", True)
sidebar_instructions()

#
# # Sidebar
# st.sidebar.header("Quick Start Guide")
# st.sidebar.markdown("**Step 1: Export & Upload Your Chat**")
# st.sidebar.markdown("1. Export chat from WhatsApp as a .txt file.")
# st.sidebar.markdown("2. For Exporting the chat , Tap ⋮ or ⋯ at top of the screen, select 'More', then 'Export chat'.")
# st.sidebar.markdown("3. Upload the .txt file on home page. Click 'Upload Chat File'.")
#
# st.sidebar.markdown("**Step 2: Select Analysis Option**")
# st.sidebar.markdown("1. Click on the radio button next to your preferred analysis option.")
#
# st.sidebar.markdown("**Step 3: Analyze Chat**")
# st.sidebar.markdown("1. Choose a user from the dropdown.")
# st.sidebar.markdown("2. Click 'Show Analytics'.")
# st.sidebar.markdown(
#     "3. Click on the expanders to reveal specific analysis insights. (Overview, Detailed Analysis, Temporal Analysis).")
#
# st.sidebar.markdown("**OR**")
#
# st.sidebar.markdown("**Step 3: Predict Message Sender**")
# st.sidebar.markdown("1. Input message to predict sender and press Enter.")
# st.sidebar.markdown("2. Click 'Train the Model Again' to retrain if the accuracy is low.")
st.text("")
uploaded_file = st.file_uploader("Choose a file")

if 'last_processed_file' not in st.session_state:
    st.session_state['last_processed_file'] = None

if 'last_date' not in st.session_state:
    st.session_state['last_date'] = 'date/month/year'
#
# if 'last_hour' not in st.session_state:
#     st.session_state['last_hour'] = '12hr'

if 'key1' not in st.session_state:
    st.session_state['key1'] = 0

if 'key2' not in st.session_state:
    st.session_state['key2'] = 100000
#
# if 'key3' not in st.session_state:
#     st.session_state['key3'] = 200000

if 'model' not in st.session_state:
    st.session_state['model'] = None

if 'accuracy' not in st.session_state:
    st.session_state['accuracy'] = None

if uploaded_file is not None:

    # date_format = st.radio("Select a feature to proceed:", ('Chat Analysis', 'Predict Message Sender'), index=None, horizontal=True, key=st.session_state['key'])
    # hour_format = st.radio("Select a feature to proceed:", ('Chat Analysis', 'Predict Message Sender'), index=None, horizontal=True, key=st.session_state['key'])

    if uploaded_file != st.session_state['last_processed_file']:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        # dform , hform = analyze_format(data.split(" -", 1)[0])
        # st.write(data.split(" -", 1)[0])


        st.session_state.df = preprocess_data(data , 'dmy')
        st.session_state['last_processed_file'] = uploaded_file
        st.session_state['last_date'] = 'dd/mm/yyyy'
        # st.session_state['last_hour'] = '12hr'
        st.session_state.accuracy = None
        st.session_state.model = None

        st.session_state['key1'] += 1
        st.session_state['key2'] += 1
        # st.session_state['key3'] += 1
        # st.write('processing')

    st.divider()
    st.header('Choose your Date-Time Format ')
    st.text("")
    date_format = st.radio("**Select Your Chat's Date Format:**", ('date/month/year', 'month/date/year' , 'year/month/date' , 'year/date/month'), index=0, horizontal=True,
                           key=st.session_state['key2'])
    # hour_format = st.radio("Select Hour Format:", ('12hr', '24hr'), index=0, horizontal=True,
    #                        key=st.session_state['key3'])
    # or hour_format != st.session_state['last_hour']
    if date_format != st.session_state['last_date']:
        # st.write('processing')
        # st.session_state['last_date'] = date_format
        # st.session_state['last_hour'] = hour_format
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        if date_format == 'date/month/year':
            # st.write('processing 1')
            st.session_state.df = preprocess_data(data, 'dmy')

        elif date_format == 'month/date/year':
            # st.write('processing 2')
            st.session_state.df = preprocess_data(data, 'mdy')
            # st.write(st.session_state.df['day'].isna().sum())

        elif date_format == 'year/month/date':
            # st.write('processing 3')
            st.session_state.df = preprocess_data(data, 'ymd')
            # st.write(st.session_state.df['day'].isna().sum())

        elif date_format == 'year/date/month':
            # st.write('processing 4')
            st.session_state.df = preprocess_data(data, 'ydm')
            # st.write(st.session_state.df['day'].isna().sum())

        aaa = st.session_state.df['day'].isna().sum()
        if aaa == 0:
            st.write("***No errors detected. This option appears to be correct.***")
        else:
            st.write(f"***Detected {aaa} errors. Please try a different option.***")

    # if 'df' not in st.session_state:
    # df = preprocess_data(data)
    st.caption("You can also verify the date display for recent messages given below. If incorrect, please select a different option above.")
    with st.expander("Verify Data "):
        st.dataframe(st.session_state.df[['day' , 'month' , 'year' , 'hour' , 'minute', 'username' , 'msg']].tail(10))

    user_list = st.session_state.df['username'].unique().tolist()
    user_list.insert(0, "Overall")
    st.divider()

    st.header('Choose Your Feature')

    # Option buttons
    # if st.session_state['key'] is None:
    # else:else 0 if st.session_state['key'] == 'Chat Analysis' else 1
    #     st.radio("Select a feature to proceed:", ('Chat Analysis', 'Predict Message Sender'), index=None, horizontal=True)

    # st.session_state['key'] = option
    option = st.radio("**Select a feature to proceed:**", ('Chat Analysis', 'Predict Message Sender'), index=None,
                      horizontal=True, key=st.session_state['key1'])
    if option == 'Chat Analysis':
        st.divider()
        st.subheader('Chat Analysis')
        selected_user = st.selectbox(
            "***Select which user's analysis you want :***",
            user_list
        )
        if st.button("Show Analysis"):
            st.divider()
            st.write("***Click on the three sections below to reveal specific analysis insights :***")
            # st.write("***Click on the three sections below to reveal specific analysis insights***")
            # st.caption("Note: The analysis is divided into three sections. If it's displaying less information, it's still loading.In the meantime, feel free to explore the loaded sections.")

            tab1, tab2, tab3 = st.tabs(["**Overview**", "**Detailed Analysis**", "**Temporal Analysis**"])
            with tab1:
                st.title("Overview")
                st.divider()
                total_messages, media_shared, total_words, total_emojis = helper.get_stats(selected_user,
                                                                                           st.session_state.df)

                cols = st.columns(4)
                with cols[0]:
                    # st.metric(label="Total Messages", value=total_messages)
                    st.subheader("Total Messages")
                    st.title(total_messages)

                with cols[1]:
                    # st.metric(label="Media Shared", value=media_shared)
                    st.subheader("Media Shared")
                    st.title(media_shared)

                with cols[2]:
                    # st.metric(label="Total Words", value=total_words)
                    st.subheader("Total Words")
                    st.title(total_words)

                with cols[3]:
                    # st.metric(label="**Total Emojis**", value=total_emojis)
                    st.subheader("Total Emojis")
                    st.title(total_emojis)

                # with cols[4]:
                #     st.header("Average Words in Message")
                #     tmsg = total_messages-media_shared
                #     if tmsg == 0:
                #         avg = 0
                #     else:
                #         avg = total_messages/tmsg
                #     st.title(avg)

                if selected_user == 'Overall':
                    st.divider()
                    st.header("User Message Distribution")
                    x, um = helper.msgs_by_user(st.session_state.df)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.caption('Top Users (Most Messages Sent)')
                        st.pyplot(x)
                    with col2:
                        st.caption('All Users (Sorted by Message Count)')
                        st.dataframe(um)

                    st.divider()
                    st.header("Deleted Messages Distribution")
                    x, um = helper.most_deleted_messages(st.session_state.df)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.caption('Top Users (Most Deleted Messages)')
                        st.pyplot(x)
                    with col2:
                        st.caption('All Users (Sorted by Deleted Message Count)')
                        st.dataframe(um)

            with tab2:
                st.title("Detailed Analysis")
                st.divider()
                st.header("Most Frequent Words")
                col1, col2 = st.columns(2)

                with col1:
                    st.caption('Most Frequently used Words')
                    st.pyplot(helper.most_common_words(1, selected_user, st.session_state.df))
                with col2:
                    st.caption('Most Frequently used Words(excluding stopwords)')
                    st.pyplot(helper.most_common_words(0, selected_user, st.session_state.df))

                st.caption('Note : Stopwords are common words (e.g., "the," "and") that carry little meaning')

                # Length of Messages :
                st.divider()
                st.header("Words per Message")
                len_msg, len_df = helper.words_in_message(selected_user, st.session_state.df)
                col1, col2 = st.columns(2)

                with col1:
                    st.caption('Messages with 1-50 Words ')
                    st.pyplot(len_msg)
                with col2:
                    st.caption('Longest Messages')
                    # st.write('Longest Messages')
                    st.dataframe(len_df)

                st.divider()
                st.header("Most Frequent Emojis")
                st.caption('Most used emojis (Sorted by Count)')

                st.dataframe(helper.most_common_emojis(selected_user, st.session_state.df))

            with tab3:
                # Monthly_timeline :
                st.title("Temporal Analysis")
                st.divider()
                st.header("Monthly Timeline")
                month_timeline, month_df = helper.monthly_timeline(selected_user, st.session_state.df)
                col1, col2 = st.columns(2)

                with col1:
                    st.caption('Message Distribution Over Months')
                    st.pyplot(month_timeline)
                with col2:
                    st.caption('Top Months by Message Count')
                    st.dataframe(month_df)

                # Yearly_timeline :
                st.divider()
                st.header("Yearly Timeline")
                year_timeline, year_df = helper.yearly_timeline(selected_user, st.session_state.df)
                col1, col2 = st.columns(2)

                with col1:
                    st.caption('Message Distribution Over Years')
                    st.pyplot(year_timeline)
                with col2:
                    st.caption('Top Years by Message Count')
                    st.dataframe(year_df)

                # Day_timeline :
                st.divider()
                st.header("Day-wise Message Distribution")
                day_timeline, day_df = helper.day_timeline(selected_user, st.session_state.df)
                col1, col2 = st.columns(2)

                with col1:
                    st.caption('Message Distribution Over Days')
                    st.pyplot(day_timeline)
                with col2:
                    st.caption('Top Days by Message Count')
                    st.dataframe(day_df)

                # Day_time_Heatmap :
                st.divider()
                st.header("Hourly Messaging Trends")
                time_period_timeline, tp_df = helper.time_period_timeline(selected_user, st.session_state.df)
                col1, col2 = st.columns(2)

                with col1:
                    st.caption("Message Distribution across Hours each Day")
                    st.caption("***Note: Lighter shades indicate high activity***")
                    st.pyplot(time_period_timeline)
                with col2:
                    st.caption('Top Hours by Message Count')
                    st.dataframe(tp_df)

    elif option == 'Predict Message Sender':
        st.divider()
        st.subheader('Predict Message Sender')

        if st.session_state.model is None or st.session_state.accuracy is None:
            st.session_state.accuracy, st.session_state.model = helper.predict_user_preprocess(st.session_state.df)
        # accuracy , model = helper.predict_user_preprocess(st.session_state.df)

        st.write(f'🎯 Estimated Accuracy: {st.session_state.accuracy * 100:.2f}%')
        st.caption('**Accuracy is low !? Try clicking the button below :**')
        if st.button('Retrain Model'):
            st.session_state.accuracy, st.session_state.model = helper.predict_user_preprocess(st.session_state.df)

        st.divider()

        st.header('Input your message')
        user_input = st.text_input("Type your message below and press 'Enter' or click '↲' to check the prediction:")

        if user_input:
            prediction, probability = helper.predict(st.session_state.model,
                                                     user_input)  # Replace with your prediction function
            st.subheader('Prediction Result')
            st.write(f'🔍 The predicted sender is: **{prediction}**')

            st.subheader('Prediction Confidence')
            st.write(f'📊 Probability: {probability * 100:.2f}%')

st.markdown('---')
st.caption('WhatsApp Chat Analyzer v1.0 | Developed by Sarvesh_More')
