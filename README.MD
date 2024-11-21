# Uso via curl
## Upload:
curl -X POST -F "file=@/caminho/do/seu/arquivo.txt" http://localhost:5000/upload

## Download:
curl -X POST \
     -F "password=random_password" \
     -L \
     -o arquivo_baixado \
     http://localhost:5000/download/AbC123XyZ
