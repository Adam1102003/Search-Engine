from flask import Flask, render_template, request
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

output_dir = "3"
documents = []
filenames = []
vectorizer = None
tfidf_matrix = None

# Function to read all text files from a directory
def read_files_from_directory(directory):
    global documents, filenames
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
                filenames.append(filename)

# Directory containing text files
directory_path = output_dir

# Read files
read_files_from_directory(directory_path)

# Create a TfidfVectorizer and fit the documents
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

# Function to convert filenames to URLs
def convert_filenames_to_urls(filenames):
    urls = [filename.replace("___", ":").replace("__", ".").replace("_", "/").replace(".txt", "").replace("www", "https://www").replace("__", ".") for filename in filenames]
    return urls

# Convert filenames to URLs
urls = convert_filenames_to_urls(filenames)

# Function to search the documents
def search(query, tfidf_matrix, vectorizer, urls):
    query_tfidf = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_tfidf, tfidf_matrix).flatten()  
    related_docs_indices = cosine_similarities.argsort()[::-1]
    
    results = []
    for index in related_docs_indices:
        results.append({
            'url': urls[index],
            'score': cosine_similarities[index]
        })
    return results

@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        query = request.form['query']
        results = search(query, tfidf_matrix, vectorizer, urls)
        return render_template('results.html', query=query, results=results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
