#!/usr/bin/env python3

import zipfile
import os
from pathlib import Path
import minsearch

def extract_md_files_from_zip(zip_path):
    """
    Extract .md and .mdx files from zip archive and return their content with processed filenames.
    """
    documents = []
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            # Check if file is .md or .mdx
            if file_info.filename.endswith(('.md', '.mdx')) and not file_info.is_dir():
                try:
                    # Read file content
                    content = zip_ref.read(file_info.filename).decode('utf-8', errors='ignore')
                    
                    # Process filename: remove first part of path
                    # "fastmcp-main/docs/getting-started/welcome.mdx" -> "docs/getting-started/welcome.mdx"
                    path_parts = file_info.filename.split('/')
                    if len(path_parts) > 1:
                        processed_filename = '/'.join(path_parts[1:])
                    else:
                        processed_filename = file_info.filename
                    
                    documents.append({
                        'content': content,
                        'filename': processed_filename
                    })
                    print(f"Extracted: {processed_filename}")
                    
                except Exception as e:
                    print(f"Error reading {file_info.filename}: {e}")
                    continue
    
    return documents

def create_search_index(documents):
    """
    Create and populate minsearch index with documents.
    """
    # Initialize minsearch index
    index = minsearch.Index(
        text_fields=['content', 'filename'],  # Search in both content and filename
        keyword_fields=[]  # No keyword fields for now
    )
    
    # Add documents to index
    index.fit(documents)
    print(f"Indexed {len(documents)} documents")
    
    return index

def search_documents(index, query, num_results=5):
    """
    Search for documents and return top num_results.
    """
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict={'content': 1.0, 'filename': 0.5},  # Boost content over filename
        num_results=num_results
    )
    
    return results

def main():
    """
    Main function to test the search implementation.
    """
    zip_path = "fastmcp-main.zip"
    
    # Check if zip file exists
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found. Please download it first.")
        return
    
    print("Extracting .md and .mdx files from zip...")
    documents = extract_md_files_from_zip(zip_path)
    
    if not documents:
        print("No .md or .mdx files found in the zip archive.")
        return
    
    print(f"\nFound {len(documents)} documents")
    print("\nCreating search index...")
    index = create_search_index(documents)
    
    print("\nSearch index created successfully!")
    
    # Answer the specific question about "demo" query
    print("\n" + "="*60)
    print("ANSWERING THE QUESTION: What's the first file for 'demo'?")
    print("="*60)
    
    demo_results = search_documents(index, "demo", num_results=5)
    
    if demo_results:
        print(f"\nSearching for: 'demo'")
        print(f"First file returned: {demo_results[0]['filename']}")
        print("\nAll results for 'demo':")
        for i, doc in enumerate(demo_results, 1):
            print(f"{i}. {doc['filename']}")
    else:
        print("No results found for 'demo'")
    
    # Test other searches
    print("\n" + "="*50)
    print("Testing other search functionality")
    print("="*50)
    
    # Test searches
    test_queries = [
        "getting started",
        "installation", 
        "FastMCP",
        "tools",
        "configuration"
    ]
    
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 30)
        results = search_documents(index, query, num_results=3)
        
        if results:
            for i, doc in enumerate(results, 1):
                print(f"{i}. {doc['filename']}")
                # Show first 100 chars of content
                content_preview = doc['content'][:100].replace('\n', ' ')
                print(f"   Preview: {content_preview}...")
                print()
        else:
            print("   No results found.")
            print()

if __name__ == "__main__":
    main()