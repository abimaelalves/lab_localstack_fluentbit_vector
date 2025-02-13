import os
import gzip
import json
import pandas as pd
import pyarrow.parquet as pq
import boto3

# Configuração do LocalStack
S3_BUCKET = "fluentbit-logs"
LOCALSTACK_ENDPOINT = "http://localhost:4566"
VECTOR_LOGS_DIR = "/Users/abimael/workspace/lab_localstack_fluentbit_vector/vector-logs"  # Caminho onde os logs do Vector são salvos

# Inicializa o cliente S3 para LocalStack
s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT)

def list_gzip_files():
    """Lista todos os arquivos .json.gz no diretório do Vector"""
    files = []
    for root, _, filenames in os.walk(VECTOR_LOGS_DIR):
        for filename in filenames:
            if filename.endswith(".json.gz"):
                files.append(os.path.join(root, filename))
    return files

def convert_gzip_to_parquet(gzip_path):
    """Converte um arquivo .json.gz para .parquet"""
    try:
        # Define o nome do arquivo Parquet
        parquet_path = gzip_path.replace(".json.gz", ".parquet")

        # Descompacta e lê o arquivo JSON
        with gzip.open(gzip_path, "rt") as f:
            logs = [json.loads(line) for line in f]

        # Converte para DataFrame
        df = pd.DataFrame(logs)

        # Salva como Parquet
        df.to_parquet(parquet_path, engine="pyarrow")

        print(f"✔ Convertido: {gzip_path} → {parquet_path}")
        return parquet_path

    except Exception as e:
        print(f"❌ Erro ao converter {gzip_path}: {e}")
        return None

def upload_to_s3(parquet_path):
    """Faz o upload do arquivo .parquet para o LocalStack S3"""
    try:
        s3_key = f"logs/{os.path.basename(parquet_path)}"
        s3_client.upload_file(parquet_path, S3_BUCKET, s3_key)
        print(f"📤 Enviado para S3: {s3_key}")

        # Remove os arquivos locais após o envio bem-sucedido
        os.remove(parquet_path)

    except Exception as e:
        print(f"❌ Erro ao enviar {parquet_path} para o S3: {e}")

def main():
    """Executa a conversão e upload para S3"""
    gzip_files = list_gzip_files()
    if not gzip_files:
        print("⚠ Nenhum arquivo .json.gz encontrado para conversão.")
        return

    for gzip_file in gzip_files:
        parquet_file = convert_gzip_to_parquet(gzip_file)
        if parquet_file:
            upload_to_s3(parquet_file)

if __name__ == "__main__":
    main()
