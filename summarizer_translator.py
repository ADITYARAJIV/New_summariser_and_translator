from summarizer import Summarizer
from translator import Translator
import pandas as pd

class SummarizerTranslator:
    def __init__(self, input_file, output_file, target_language='hi'):
        self.input_file = input_file
        self.output_file = output_file
        self.summarizer = Summarizer()
        self.translator = Translator(target_language)

    def process_data(self):
        # Read the input CSV file
        df = pd.read_csv(self.input_file)
        
        # Process each article
        summaries = []
        translations = []
        for index, row in df.iterrows():
            content = row['content']  # Assuming 'content' column exists
            summary = self.summarizer.summarize(content)
            translated = self.translator.translate(summary)
            summaries.append(summary)
            translations.append(translated)

        # Store the results
        df['summary'] = summaries
        df['translated_summary'] = translations
        df.to_csv(self.output_file, index=False)

# Example usage:
if __name__ == "__main__":
    input_file = 'filtered_indian_news.csv'  # Your input file path
    output_file = 'summarized_translated_news.csv'  # Your output file path
    summarizer_translator = SummarizerTranslator(input_file, output_file)
    summarizer_translator.process_data()
