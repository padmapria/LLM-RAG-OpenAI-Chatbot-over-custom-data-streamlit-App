import os
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm

# Load environment variables from .env file
load_dotenv()

# Elasticsearch configuration
ELAST_SEARCH_PWD = os.getenv('ELASTIC_SEARCH_PWD')
es_connection = Elasticsearch("http://localhost:9200", basic_auth=('elastic', ELAST_SEARCH_PWD))
index_name = "wiki_qa_questions"

# Connect to Elasticsearch
def connect_to_es():
    for _ in range(10):  # Retry up to 10 times
        try:
            es = Elasticsearch("http://elasticsearch:9200", basic_auth=('elastic', ELAST_SEARCH_PWD))
            if es.ping():
                print("Connected to Elasticsearch")
                return es
        except Exception as e:
            print(f"Connection failed, retrying... ({e})")
            time.sleep(10)
    raise Exception("Failed to connect to Elasticsearch after several retries")


# Prepare data
def prepare_data(name):
    print('preparing_data');
    dataset = load_dataset(name)
    train_df = pd.DataFrame(dataset['validation'])
    doc_list = [row.to_dict() for index, row in train_df.iterrows()]
    return doc_list

# Index documents in Elasticsearch
def index_document(index_name, documents):
    es = connect_to_es()
    print('connected')
    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "answer": {"type": "text"},
                "document_title": {"type": "text"},
                "question": {"type": "text"},
                "question_id": {"type": "keyword"}
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_settings)
        print("Index created")
    else:
        print("Index already exists")
    
    for doc in tqdm(documents):
        doc_id = doc['question_id']
        es.index(index=index_name, id=doc_id, document=doc)

doc_list = prepare_data("microsoft/wiki_qa")
index_document(index_name, doc_list)
