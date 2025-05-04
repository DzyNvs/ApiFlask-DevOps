# Usa uma versão mais recente do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (otimiza cache de build)
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos restantes do projeto
COPY . .

# Exporta a porta usada pelo Flask
EXPOSE 5000

# Define a variável de ambiente para iniciar o Flask corretamente
ENV FLASK_APP=app.py

# Usa Gunicorn para rodar o servidor em produção
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
