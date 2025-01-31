from transformers import pipeline

class Summarizer:
    def __init__(self):
        # Load the BART summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def chunk_text(self, text, max_tokens=500):
        """Splits long texts into smaller chunks for summarization."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_tokens):
            chunks.append(" ".join(words[i:i + max_tokens]))
        return chunks

    def summarize(self, text):
        """Summarizes text with length control and chunking."""
        if len(text.split()) > 500:
            # Split into chunks and summarize separately
            chunks = self.chunk_text(text)
            summaries = [self.summarizer(chunk, max_length=150, min_length=50, truncation=True)[0]['summary_text'] for chunk in chunks]
            # Summarize the summarized chunks again
            final_summary = " ".join(summaries)
            return self.summarizer(final_summary, max_length=150, min_length=50, truncation=True)[0]['summary_text']
        else:
            # Directly summarize shorter text
            return self.summarizer(text, max_length=150, min_length=50, truncation=True)[0]['summary_text']
