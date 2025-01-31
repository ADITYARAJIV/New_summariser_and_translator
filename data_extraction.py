import pandas as pd

class DataExtractor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = None

    def load_data(self):
        try:
            # Load the data from the CSV file
            self.data = pd.read_csv(self.input_file)
            print(f"Data loaded successfully from {self.input_file}")
        except Exception as e:
            print(f"Error loading data: {e}")

    def filter_and_process_data(self):
        try:
            if self.data is not None:
                # Select only required columns
                self.data = self.data[['category', 'header', 'content']]
                
                # Keep only 2 records per category
                self.data = self.data.groupby('category').head(2)

                # Truncate content to first 25 words if it exceeds 25 words
                self.data['content'] = self.data['content'].apply(self.summarize_content)

                print("Data filtered and processed successfully")
            else:
                print("Data is not loaded yet")
        except Exception as e:
            print(f"Error processing data: {e}")

    def summarize_content(self, text):
        """Keep only the first 25 words if the text is longer than 25 words."""
        words = text.split()
        return ' '.join(words[:25]) if len(words) > 25 else text

    def save_data(self):
        try:
            if self.data is not None:
                self.data.to_csv(self.output_file, index=False)
                print(f"Data saved successfully to {self.output_file}")
            else:
                print("No data to save")
        except Exception as e:
            print(f"Error saving data: {e}")

if __name__ == "__main__":
    input_file = "historic_articles.csv"
    output_file = "filtered_indian_news.csv"

    extractor = DataExtractor(input_file, output_file)
    extractor.load_data()
    extractor.filter_and_process_data()
    extractor.save_data()
