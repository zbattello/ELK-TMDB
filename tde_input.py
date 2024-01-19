import pandas as pd
import http.client
import json

def send_data_to_elasticsearch(csv_file_path, es_host, es_port, index_name):
    # Connexion au serveur Elasticsearch
    connection = http.client.HTTPConnection(es_host, es_port)

    # Lecture du fichier CSV avec Pandas
    df = pd.read_csv(csv_file_path)

    
    # Envoi des données à Elasticsearch
    for _, row in df.iterrows():
        json_data = json.dumps(row.to_dict())
        connection.request("POST", f"/{index_name}/tmdbdoc/", json_data, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        # print row number
        print(f"{row.name} : {response.read().decode()}")

    # Fermeture de la connexion
    connection.close()

if __name__ == '__main__':
    csv_file_path = './media_list.csv'
    es_host = "134.214.202.38"
    es_port = 9200
    index_name = "tmdb"
    send_data_to_elasticsearch(csv_file_path, es_host, es_port, index_name)