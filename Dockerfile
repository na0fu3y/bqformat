FROM ubuntu:18.04 AS builder

RUN apt-get update \
 && apt-get install -y curl gnupg make python3 \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && curl https://bazel.build/bazel-release.pub.gpg | apt-key add - \
 && echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
 && apt-get update \
 && apt-get install -y bazel=3.3.0

WORKDIR /app

COPY BUILD format_sql.cc parse_statement.cc WORKSPACE /app/

RUN bazel build -t --cxxopt="-fpermissive" --cxxopt="-std=c++17" ...

FROM python:3.8 AS production

COPY --from=builder /app/bazel-bin/format_sql /app/bazel-bin/parse_statement /

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