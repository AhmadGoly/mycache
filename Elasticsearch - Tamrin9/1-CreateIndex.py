import requests

endpoint = 'http://localhost:9200'
index_name = 'my_index3'
index_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "url": {"type": "keyword"},
            "contributors": {"type": "keyword"},
            "date": {"type": "keyword"},
            "format": {"type": "keyword"},
            "full_text_url": {"type": "keyword"},
            "trove_id": {"type": "keyword"},
            "language": {"type": "keyword"},
            "rights": {"type": "keyword"},
            "pages": {"type": "integer"},
            "form": {"type": "keyword"},
            "volume": {"type": "keyword"},
            "children": {"type": "keyword"},
            "parent": {"type": "keyword"},
            "text_downloaded": {"type": "keyword"},
            "text_file": {"type": "keyword"}
        }
    }
}

response = requests.put(f'{endpoint}/{index_name}', json=index_mapping)
if response.status_code == 200:
    print("Index created successfully!")
else:
    print("Failed to create the index.")
