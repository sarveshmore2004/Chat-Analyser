import streamlit as st
from preprocess import preprocess_data
import helper

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

# Sidebar
st.sidebar.header("Quick Start Guide")
st.sidebar.markdown("**Step 1: Export & Upload Your Chat**")
st.sidebar.markdown("1. Export chat from WhatsApp as a .txt file.")
st.sidebar.markdown("2. For Exporting the chat , Tap ⋮ or ⋯ at top of the screen, select 'More', then 'Export chat'.")
st.sidebar.markdown("3. Upload the .txt file on home page. Click 'Upload Chat File'.")

st.sidebar.markdown("**Step 2: Select Analysis Option**")
st.sidebar.markdown("1. Click on the radio button next to your preferred analysis option.")

st.sidebar.markdown("**Step 3: Analyze Chat**")
st.sidebar.markdown("1. Choose a user from the dropdown.")
st.sidebar.markdown("2. Click 'Show Analytics'.")
st.sidebar.markdown("3. Click on the expanders to reveal specific analysis insights. (Overview, Detailed Analysis, Temporal Analysis).")

st.sidebar.markdown("**OR**")

st.sidebar.markdown("**Step 3: Predict Message Sender**")
st.sidebar.markdown("1. Input message to predict sender and press Enter.")
st.sidebar.markdown("2. Click 'Train the Model Again' to retrain if the accuracy is low.")

uploaded_file = st.file_uploader("Choose a file")

if 'last_processed_file' not in st.session_state:
    st.session_state['last_processed_file'] = None

if 'selected_option' not in st.session_state:
    st.session_state['selected_option'] = 0

if 'model' not in st.session_state:
    st.session_state['model'] = None

if 'accuracy' not in st.session_state:
    st.session_state['accuracy'] = None


if uploaded_file is not None :
    # To read file as bytes:

    if uploaded_file != st.session_state['last_processed_file']:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        st.session_state.df = preprocess_data(data)
        st.session_state['last_processed_file'] = uploaded_file
        st.session_state['selected_option'] += 1
        st.session_state.accuracy = None
        st.session_state.model = None
        # st.write('processing')


    # if 'df' not in st.session_state:
    # df = preprocess_data(data)
    # st.dataframe(df)

    user_list = st.session_state.df['username'].unique().tolist()
    user_list.insert(0, "Overall")
    st.divider()

    st.header('Choose Your Feature')

    # Option buttons
    # if st.session_state['selected_option'] is None:
    # else:else 0 if st.session_state['selected_option'] == 'Chat Analysis' else 1
    #     st.radio("Select a feature to proceed:", ('Chat Analysis', 'Predict Message Sender'), index=None, horizontal=True)

    # st.session_state['selected_option'] = option
    option = st.radio("Select a feature to proceed:", ('Chat Analysis', 'Predict Message Sender'), index=None, horizontal=True, key=st.session_state['selected_option'])
    if option == 'Chat Analysis':
        st.divider()
        st.subheader('Chat Analysis')
        selected_user = st.selectbox(
            "Select which user's analysis you want :",
            user_list
        )
        if st.button("Show Analysis"):
            st.text("Click on the sections below to reveal specific analysis insights:")
            st.caption("Note: The analysis is divided into three sections. If it's displaying less information, it's still loading.In the meantime, feel free to explore the loaded sections.")
            with st.expander("Overview"):
                st.title("Overview")
                st.divider()
                total_messages, media_shared, total_words, total_emojis = helper.get_stats(selected_user, st.session_state.df)

                cols = st.columns(4)
                with cols[0]:
                    st.subheader("Total Messages")
                    st.title(total_messages)

                with cols[1]:
                    st.subheader("Media Shared")
                    st.title(media_shared)

                with cols[2]:
                    st.subheader("Total Words")
                    st.title(total_words)

                with cols[3]:
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

            with st.expander("Detailed Analysis"):
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

            with st.expander("Temporal Analysis"):

            # Monthly_timeline :
                st.header("Temporal Analysis")
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
                    st.caption("Note: Lighter shades indicate high activity")
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

        st.header('Input your message')
        user_input = st.text_input("Type your message and press 'Enter' to check the prediction:")

        if user_input:
            prediction, probability = helper.predict(st.session_state.model , user_input)  # Replace with your prediction function
            st.subheader('Prediction Result')
            st.write(f'🔍 The predicted sender is: **{prediction}**')

            st.subheader('Prediction Confidence')
            st.write(f'📊 Probability: {probability * 100:.2f}%')


st.markdown('---')
st.caption('WhatsApp Chat Analyzer v1.0 | Developed by Sarvesh_More')
