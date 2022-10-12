# Install express, express-sessions and fetch
# run index.js on port 3000
FROM node:16.17.1

WORKDIR /app
COPY index.js .
COPY package.json .
COPY package-lock.json .
COPY static ./static

RUN npm install

EXPOSE 3000
CMD ["node", "index.js"]
