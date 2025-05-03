from flask import Flask, render_template, request
import os
import nltk
from collections import defaultdict
from nltk.tokenize import word_tokenize

app = Flask(__name__)
nltk.download('punkt')  # Download NLTK tokenizer data

output_dir = "INVERTED INDEX/3"
index = defaultdict(set)

def build_index():
    for filename in os.listdir(output_dir):
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = word_tokenize(content.lower())  # Tokenize using NLTK
            for token in set(tokens):  # Use set to avoid duplicate tokens
                index[token].add(filename)

@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        query = request.form['query']
        if not index:
            build_index()
        urls = search(query.lower())
        return render_template('results.html', query=query, urls=urls)
    else:
        return render_template('index.html')

def search(query):
    query_tokens = set(word_tokenize(query))
    matching_files = None
    for token in query_tokens:
        files_with_token = index.get(token, set())
        if matching_files is None:
            matching_files = files_with_token
        else:
            matching_files = matching_files.intersection(files_with_token)
    urls = [filename.replace("www", "https://www").replace("___", ":").replace("__", ".").replace("_", "/").replace(".txt", "") for filename in matching_files]
    return urls

if __name__ == '__main__':
    app.run(debug=True)
