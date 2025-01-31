from transformers import MarianMTModel, MarianTokenizer

class Translator:
    def __init__(self, target_language='hi'):
        self.model_name = f'Helsinki-NLP/opus-mt-en-{target_language}'
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)

    def translate(self, text):
        # Prepare the input text
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        
        # Translate the text
        translated = self.model.generate(**inputs)
        
        # Decode the translated text
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

# Example usage:
if __name__ == "__main__":
    translator = Translator(target_language='hi')  # For Hindi translation
    text = "Your news article content here."
    translated_text = translator.translate(text)
    print(translated_text)
