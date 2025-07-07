FROM node:20

WORKDIR /workspace/frontend

RUN apt-get update && apt-get install -y procps net-tools lsof

COPY package*.json ./
RUN npm install

COPY . ./

EXPOSE 8080

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
