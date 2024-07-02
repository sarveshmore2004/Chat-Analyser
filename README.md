# WhatsApp Chat Analyzer

Welcome to the WhatsApp Chat Analyzer! This tool allows you to gain insights into your WhatsApp conversations quickly and efficiently.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation) 
- [Quick Start Guide](#quick-start-guide)

## Project Overview

The WhatsApp Chat Analyzer is an interactive web application designed to analyze and visualize your WhatsApp chat data. By uploading your chat history, you can gain valuable insights into various aspects of your conversations, including message statistics, user activity, frequent words and emojis, and temporal trends. Additionally, the tool includes a machine learning model to predict the sender of a message.

## Features

- **Comprehensive Chat Analysis**: Analyze total messages, word counts, user message distribution, frequent words and emojis, message trends over time, and many more features!!!
- **Message Sender Prediction**: Predict the sender of a message using a Naive Bayes model built with scikit-learn.
- **Interactive Visualizations**: View data through intuitive charts and graphs for a better understanding of your chat history.
- **User-Friendly Interface**: Simple and intuitive interface with step-by-step instructions for ease of use.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Pandas, scikit-learn, re (Regular Expressions), Matplotlib, Seaborn, Collections (Counter), emoji

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
    cd whatsapp-chat-analyzer
    ```

2. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app**:
    ```sh
    streamlit run app.py
    ```

## Quick Start Guide

### Step 1: Export & Upload Your Chat

1. Export your chat from WhatsApp as a .txt file:
   - Tap ⋮ or ⋯ at the top of the screen.
   - Select 'More', then 'Export chat'.
   - Choose the conversation you want to analyze.
   - Select 'Without Media'.
   - Finally, select 'Export' and save the file.

2. Extract the .zip file to obtain the .txt file, then navigate to the home page of our tool.

3. Click on 'Upload Chat File' and select the .txt file you just exported from WhatsApp.

### Step 2: Select Date Format

1. Choose the appropriate date format of your chat by selecting the corresponding radio button.
   - If you encounter numerous errors during analysis, try selecting a different date format until you achieve satisfactory results.

### Step 3: Select Analysis Option

1. Click on the radio button next to your preferred analysis option.
   - Choose between different analysis options available.

### Step 4: Analyze Chat

1. If you selected analysis by user:
   - Choose a user from the dropdown menu.
   - Click 'Show Analytics'.
   - Explore the insights provided, including Overview, Detailed Analysis, and Temporal Analysis.

2. If you selected prediction of message sender:
   - Input a message to predict the sender and press Enter.
   - If the accuracy of prediction is low, click 'Train the Model Again' to retrain.

That's it! You're now ready to explore and gain valuable insights from your WhatsApp conversations using our WhatsApp Chat Analyzer. If you encounter any issues or have suggestions for improvements, feel free to reach out to us.

---

Happy analyzing! 🚀
