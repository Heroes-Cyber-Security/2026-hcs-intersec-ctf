FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3000

CMD sh -c 'RAND=$(head -c 16 /dev/urandom | md5sum | head -c 8) && echo "${CTF_FLAGS}" > /flag-$RAND.txt && node index.js'
