import pandas as pd
from transformers import T5ForConditionalGeneration, T5Tokenizer
from googletrans import Translator

# Load the summarization model
def load_model():
    model_name = "t5-small"  # You can change this to a larger model for better quality
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    return model, tokenizer

# Summarize the content
def summarize_content(model, tokenizer, content):
    inputs = tokenizer.encode("summarize: " + content, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Translate content to specified languages
def translate_content(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language).text
    return translated

# Process the dataset: summarize and translate
def process_dataset(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    df = df[['category', 'header', 'content']]  # Only need these columns
    
    # Load model for summarization
    model, tokenizer = load_model()

    # Summarize content and translate
    translated_data = []
    
    for index, row in df.iterrows():
        try:
            # Summarize content
            summary = summarize_content(model, tokenizer, row['content'])
            
            # Translate the summarized content
            hindi_translation = translate_content(summary, 'hi')  # Hindi
            marathi_translation = translate_content(summary, 'mr')  # Marathi
            
            translated_data.append({
                'title': row['header'],
                'summary': summary,
                'hindi_translation': hindi_translation,
                'marathi_translation': marathi_translation
            })
        except Exception as e:
            print(f"Error processing article {row['header']}: {e}")
            continue
    
    # Convert to DataFrame and save to CSV
    translated_df = pd.DataFrame(translated_data)
    translated_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Run the process
input_file = 'historic_articles.csv'  # Input file path
output_file = 'summarized_translated_articles.csv'  # Output file path
process_dataset(input_file, output_file)