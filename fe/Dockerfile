# fe/Dockerfile
FROM node:16.18.1 AS builder

WORKDIR /app

COPY package*.json ./

# RUN npm install -g @angular/cli    
RUN npm install                  

COPY . .

ENV PATH /app/node_modules/.bin:$PATH

CMD ["./node_modules/.bin/ng", "serve", "--host", "0.0.0.0"]
