# Usando a versão debug mais recente do Fluent Bit
FROM fluent/fluent-bit:3.2.6-debug

# Copia o arquivo de configuração customizado para dentro do container
COPY fluent-bit.conf /fluent-bit/etc/fluent-bit.conf

# Define o ponto de entrada para iniciar o Fluent Bit com logs detalhados
CMD ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf", "-v"]
