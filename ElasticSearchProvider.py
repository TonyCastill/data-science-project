from elasticsearch import Elasticsearch, helpers
import json
import time

class ElasticSearchProvider:
    def __init__(self):
        self.host = "http://localhost:9200"  # Elastic IP
        # self.user = str(user)
        # Changed to person2 from person
        self.index = "mexico-divorces"
        self.index_type = "_doc"
        self.connection = Elasticsearch(
            self.host,
            verify_certs=False,
            # headers={"Content-Type": "application/json", "Accept": "application/json"}
        )  # auth.()

    def __enter__(self):
        # Primer método que se ejecuta con el constructor
        try:
            self.connection = Elasticsearch(
                self.host,
                # headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            return self
        except Exception as e:
            # Error
            return {"StatusCode": 500, "body": json.dumps({"message": str(e)})}
        # Cuando se sale, cierra la conexión

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.transport.close()
    
    def bulk_insert(self,data):
        documents=[
            {
                "_index": self.index,
                "_source": document
            }
            for document in data
        ]
        # Perform the bulk insert
        try:
            success, failed = helpers.bulk(self.connection, documents)
            print(f"Successfully inserted {success} documents.")
            if failed:
                print(f"Failed to insert {len(failed)} documents.")
            return success
        except Exception as e:
            print(f"An error occurred during bulk insert: {e}")