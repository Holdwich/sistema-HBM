FROM node:20-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências e instala
COPY package*.json ./
RUN npm install

# Copia o restante do código
COPY . .

# Exponha a porta do Next.js (geralmente 3000)
EXPOSE 3000

# Comando para iniciar o servidor Next.js
CMD ["npm", "run", "dev"]