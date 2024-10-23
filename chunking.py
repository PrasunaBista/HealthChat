import os
import re
import spacy
import csv

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

def extract_text_from_md(md_path):
    """Extract text from a Markdown file."""
    with open(md_path, 'r', encoding='utf-8') as file:
        text = file.read()  # Read the entire file
    return text

def preprocess_text(text):
    """Clean up the text by removing unnecessary characters."""
    text = re.sub(r'\.\.\.+', '', text)  # Remove ellipses
    text = re.sub(r'\s{4,}', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()  # Strip leading/trailing whitespace

def split_text_by_sentences(text):
    """Split text into chunks of sentences."""
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    chunks = [sentences[i:i + 4] for i in range(0, len(sentences), 4)]  # Create chunks of 4 sentences
    chunks = [' '.join(chunk) for chunk in chunks]  # Join sentences in each chunk
    return chunks

def save_chunks_to_csv(chunks, file_path):
    """Save the text chunks to a CSV file."""
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i, chunk in enumerate(chunks):
            writer.writerow([i + 1, chunk])  # Write row index and chunk

# Directory containing the Markdown files
md_directory = '/Users/prasunabista/Documents/HealthChat/scrapped data'
# Output file for the CSV
output_file_path = '/Users/prasunabista/Documents/HealthChat/chunks.csv'

all_chunks = []  # To store all chunks from all Markdown files

# Iterate through all files in the Markdown directory
for filename in os.listdir(md_directory):
    if filename.endswith('.md'):  # Check if the file is a Markdown file
        md_path = os.path.join(md_directory, filename)  # Create full path
        print(f"Processing {md_path}")
        
        # Extract and process text
        md_text = extract_text_from_md(md_path)
        processed_text = preprocess_text(md_text)
        chunks = split_text_by_sentences(processed_text)
        
        all_chunks.extend(chunks)  # Add chunks to the list

# Save all chunks to the CSV file
save_chunks_to_csv(all_chunks, output_file_path)

print(f"Custom chunks have been saved to {output_file_path}")
