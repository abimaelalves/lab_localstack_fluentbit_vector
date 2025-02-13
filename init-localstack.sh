#!/bin/bash

docker exec -it localstack aws --endpoint-url=http://localhost:4566 s3 mb s3://fluentbit-logs

docker exec -it localstack aws --endpoint-url=http://localhost:4566 s3 ls
