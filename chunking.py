import os
import re
import spacy
import csv


nlp = spacy.load('en_core_web_sm')

def extract_text_from_md(md_path):
    """Extract text from a Markdown file."""
    with open(md_path, 'r', encoding='utf-8') as file:
        text = file.read()  
    return text

def preprocess_text(text):
    """Clean up the text by removing unnecessary characters."""
    text = re.sub(r'\.\.\.+', '', text)  
    text = re.sub(r'\s{4,}', ' ', text)  
    return text.strip()  # 

def split_text_by_sentences(text):
    """Split text into chunks of sentences."""
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    chunks = [sentences[i:i + 4] for i in range(0, len(sentences), 4)] 
    chunks = [' '.join(chunk) for chunk in chunks]  
    return chunks

def save_chunks_to_csv(chunks, file_path):
    """Save the text chunks to a CSV file."""
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i, chunk in enumerate(chunks):
            writer.writerow([i + 1, chunk]) 


md_directory = '/Users/prasunabista/Documents/HealthChat/scrapped data'

output_file_path = '/Users/prasunabista/Documents/HealthChat/chunks.csv'

all_chunks = []  


for filename in os.listdir(md_directory):
    if filename.endswith('.md'): 
        md_path = os.path.join(md_directory, filename)  
        print(f"Processing {md_path}")
        
      
        md_text = extract_text_from_md(md_path)
        processed_text = preprocess_text(md_text)
        chunks = split_text_by_sentences(processed_text)
        
        all_chunks.extend(chunks) 


save_chunks_to_csv(all_chunks, output_file_path)

print(f"Custom chunks have been saved to {output_file_path}")
