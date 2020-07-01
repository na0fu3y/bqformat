# BQ Format

BigQuery StandardSQLのフォーマットや列名ルールを強制します。

# インストール

Dockerが必要です。

``` bash
$ curl https://raw.githubusercontent.com/na0fu3y/bqformat/master/bqformat > bqformat
$ chmod +x bqformat
$ mv bqformat /usr/local/bin/bqformat
```

# 使い方

以下のコマンドで、フォーマット結果がformatted.sqlに書き込まれます。
意味の薄いエイリアスが含まれている場合エラーになります。

``` bash
$ cat example.sql | bqformat > formatted.sql
```
