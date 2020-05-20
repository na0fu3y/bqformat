FROM python:3.6 AS production

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY setup.py /usr/src/app/
COPY src /usr/src/app/src
RUN pip install .

FROM node:12.16.3-buster AS node
COPY package.json .
RUN npm install

FROM production AS debug
COPY --from=node /usr/local/bin/node /usr/local/bin/
COPY --from=node /node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/textlint/bin/textlint.js /usr/local/bin/textlint
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
