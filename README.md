# BQ Format

BigQuery StandardSQL のフォーマットや列名ルールを強制します。

# インストール

``` bash
$ curl https://raw.githubusercontent.com/na0fu3y/bqformat/master/bqformat > bqformat
$ chmod +x bqformat
$ mv bqformat /usr/local/bin/bqformat
```

# 使い方

以下のコマンドで、フォーマット結果が formatted.sql に書き込まれます。

``` bash
$ cat example.sql | bqformat > formatted.sql
```
