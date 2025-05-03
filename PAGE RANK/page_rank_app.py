from flask import Flask, render_template, request
import os
import re
import numpy as np

app = Flask(__name__)

# Function to read text files from a directory
def read_text_files(directory):
    files_content = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:
                files_content[file_name] = file.read()
    return files_content

# Function to build an inverted index
def build_inverted_index(files):
    inverted_index = {}
    for file_path, content in files.items():
        for term in content.split():
            if term not in inverted_index:
                inverted_index[term] = set()
            inverted_index[term].add(file_path)
    return inverted_index

# Function to process a query using the inverted index
def query_inverted_index(query, inverted_index):
    result = set()
    for term in query.split():
        if term in inverted_index:
            if len(result) == 0:
                result = inverted_index[term]
            else:
                result = result.intersection(inverted_index[term])
    return result

# Function to calculate PageRank
def calculate_pagerank(adj_matrix, num_nodes, d=0.85, max_iterations=100, tol=1e-6):
    pagerank = np.ones(num_nodes) / num_nodes
    for _ in range(max_iterations):
        new_pagerank = np.zeros(num_nodes)
        for i in range(num_nodes):
            for j in range(num_nodes):
                if adj_matrix[j, i] == 1:
                    new_pagerank[i] += pagerank[j] / np.sum(adj_matrix[j])
            new_pagerank[i] = d * new_pagerank[i] + (1 - d) / num_nodes
        if np.linalg.norm(new_pagerank - pagerank) < tol:
            break
        pagerank = new_pagerank
    return pagerank

# Function to combine PageRank scores with other relevancy scores
def combine_scores(pagerank_scores, other_scores):
    # Here you can implement the logic to combine scores, for simplicity, we'll just return the PageRank scores
    return pagerank_scores

# Function to modify URLs
def modify_urls(matching_files):
    urls = [filename.replace("www", "https://www").replace("___", ":").replace("__", ".").replace("_", "/").replace(".txt", "") for filename in matching_files]
    return urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        directory = '3'
        files_content = read_text_files(directory)
        inverted_index = build_inverted_index(files_content)
        relevant_documents = query_inverted_index(query, inverted_index)
        num_nodes = len(files_content)
        adj_matrix = np.eye(num_nodes)
        pagerank_scores = calculate_pagerank(adj_matrix, num_nodes)
        combined_scores = combine_scores(pagerank_scores, relevant_documents)
        matching_files = list(relevant_documents)  # Assuming relevant_documents contains file names
        urls = modify_urls(matching_files)
        results = [{'url': url, 'pagerank_score': pagerank_scores[idx]} for idx, url in enumerate(urls)]
        return render_template('results.html', query=query, results=results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
