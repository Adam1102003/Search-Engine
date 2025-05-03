import os
import re
import numpy as np

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

# Main function
def main():
    # Directory containing the text files
    directory = '3'

    # Read text files
    files_content = read_text_files(directory)

    # Build inverted index
    inverted_index = build_inverted_index(files_content)

    # Sample query
    query = 'machine learning'

    # Process query using inverted index
    relevant_documents = query_inverted_index(query, inverted_index)

    # Prepare data for PageRank (assuming adjacency matrix is identity matrix for simplicity)
    num_nodes = len(files_content)
    adj_matrix = np.eye(num_nodes)

    # Calculate PageRank scores for relevant documents
    pagerank_scores = calculate_pagerank(adj_matrix, num_nodes)

    # Combine PageRank scores with other relevancy scores
    combined_scores = combine_scores(pagerank_scores, relevant_documents)

    # Print results
    print("Relevant Documents:")
    for doc in relevant_documents:
        print(doc)
    print("\nPageRank Scores:")
    for idx, score in enumerate(pagerank_scores):
        print(f"Document {idx + 1}: {score}")
    print("\nCombined Scores:")
    for idx, score in enumerate(combined_scores):
        print(f"Document {idx + 1}: {score}")

if __name__ == "__main__":
    main()
