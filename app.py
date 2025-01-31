import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import time

class NewsApp:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)  # Load the data from the provided file
        self.language_code = 'hi'  # Default language set to Hindi

    def get_category(self):
        # User selects category
        return st.selectbox('Select a Category', self.data['category'].unique())

    def filter_data_by_category(self, category):
        # Filter data based on selected category
        return self.data[self.data['category'] == category]

    def generate_audio(self, text):
        # Generate audio from the translated summary (always in Hindi)
        tts = gTTS(text=text, lang=self.language_code, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)  # Use write_to_fp instead of save
        audio_buffer.seek(0)  # Reset the pointer to the beginning of the buffer
        return audio_buffer

    def display_news(self, category):
        # Display news articles in the selected category
        filtered_data = self.filter_data_by_category(category)

        st.write(f"Showing news from category: {category}")
        for _, row in filtered_data.iterrows():
            st.subheader(row['header'])
            st.write(f"Content (English): {row['content']}")
            st.write(f"Summary (English): {row['summary']}")
            st.write(f"Translated Summary (Hindi): {row['translated_summary']}")

            # Generate audio for the translated summary (in Hindi)
            audio_buffer = self.generate_audio(row['translated_summary'])

            # Play the audio
            st.audio(audio_buffer, format='audio/mp3', start_time=0)

            st.markdown("---")

    def run(self):
        # Main method to run the app
        st.title('News App with Translated Audio')

        # Get user input for category
        category = self.get_category()

        # Display the news and audio
        self.display_news(category)


if __name__ == "__main__":
    # Create an instance of the NewsApp class and run the app
    app = NewsApp('summarized_translated_news.csv')
    app.run()
