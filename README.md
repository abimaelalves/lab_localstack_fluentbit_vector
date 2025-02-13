# 🚀 LAB: Captura e Armazenamento de Logs com Fluent Bit, Vector e LocalStack

Este projeto configura um ambiente para capturar logs do **Fluent Bit**, processá-los com o **Vector**, armazená-los no **LocalStack S3**, e converter os arquivos JSON.GZ para **Parquet** usando um script Python.

---

## 📂 Estrutura do Projeto

```bash
LAB_LOCALSTACK_FLUENTBIT_VECTOR/
├── vector-logs/               # Pasta onde os logs do Vector são salvos
├── convert_to_parquet.py       # Script Python para conversão de logs para Parquet
├── docker-compose.yml          # Definição dos containers
├── Dockerfile                  # Configuração do Fluent Bit
├── fluent-bit.conf             # Configuração do Fluent Bit
├── init-localstack.sh          # Script para inicializar o bucket S3 no LocalStack
├── README.md                   # Documentação do projeto
└── vector.yaml                  # Configuração do Vector
```

---

## 🏗️ Configuração e Execução

### 1️⃣ **Subindo o Ambiente Docker**

```sh
docker-compose up -d
```

### 2️⃣ **Criando o Bucket no LocalStack**
Após iniciar os containers, execute:

```sh
bash init-localstack.sh
```

Isso criará um bucket chamado `fluentbit-logs` no LocalStack.

### 3️⃣ **Executando a Conversão de Logs para Parquet**
Após alguns minutos de coleta de logs, rode:

```sh
python3 convert_to_parquet.py
```

Isso converterá os logs armazenados em **JSON.GZ** para **Parquet** e enviará ao LocalStack S3.

---

## 🐳 Configuração dos Containers

### **Docker Compose**
Arquivo: `docker-compose.yml`

```yaml
version: "3.8"

services:
  localstack:
    image: localstack/localstack:latest
    container_name: localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3
      - AWS_ACCESS_KEY_ID=test
      - AWS_SECRET_ACCESS_KEY=test
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    networks:
      - log-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
      interval: 10s
      retries: 5
      start_period: 5s
      timeout: 5s

  fluent-bit:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fluent-bit
    networks:
      - log-network

  vector:
    image: timberio/vector:0.33.0-debian
    container_name: vector
    volumes:
      - ./vector.yaml:/etc/vector/vector.yaml:ro
      #- ./vector-logs:/tmp/vector-logs  # Mapeia a pasta de logs para o host (caso seja necessario testar a conversao para parquet)
    networks:
      - log-network
    depends_on:
      localstack:
        condition: service_healthy
      fluent-bit:
        condition: service_started
    environment:
      - AWS_ACCESS_KEY_ID=test
      - AWS_SECRET_ACCESS_KEY=test

networks:
  log-network:
    driver: bridge
```

---

## 🔍 Configuração do **Fluent Bit**
Arquivo: `fluent-bit.conf`

```ini
[SERVICE]
    Flush        1
    Log_Level    info
    Daemon       off

[INPUT]
    Name         cpu
    Tag          cpu_metrics
    Interval_Sec 1

[OUTPUT]
    Name stdout
    Match *

[OUTPUT]
    Name         forward
    Match        *
    Host         vector
    Port         5170
```

---

## 📜 Conversão para Parquet 
Arquivo: `convert_to_parquet.py` (use esse script para testar a conversao para .parquet, se atente a variavel VECTOR_LOGS_DIR)
```

---
