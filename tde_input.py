import pandas as pd
import http.client
import json

def send_data_to_TDE(csv_file_path, host, port, index_name):
    # HTTP request to Elasticsearch
    connection = http.client.HTTPConnection(host, port)

    # fichier CSV 
    df = pd.read_csv(csv_file_path)

    
    # envoi à elastic search tdE
    for _, row in df.iterrows():
        json_data = json.dumps(row.to_dict())
        connection.request("POST", f"/{index_name}/tmdbdoc/", json_data, headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        print(f"{row.name} : {response.read().decode()}")

    connection.close()

if __name__ == '__main__':
    csv_file_path = './media_list.csv'
    host = "134.214.202.38"
    port = 9200
    index_name = "tmdb"
    send_data_to_TDE(csv_file_path, host, port, index_name)