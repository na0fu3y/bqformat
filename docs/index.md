# Design Documents

## プロジェクトの目的
BigQueryの普及により、分析用の大きなSQLが使われるようになっている。
クエリ保守性に関する課題意識がある。

- BigQueryのフォーマッタは、STRUCTやARRAYなどで可読性が落ちる。
- 良い列名を強制できず、第三者に意味の推測できないクエリが乱立する。

そこで、フォーマットや列名ルールを強制するツールを作成する。

## 設計
SQL文字列またはファイルを受け取り、フォーマット後の文字列を返す。
ただしこの時、文字列中のエイリアスの評価を行い、低評価の列名があればエラーを出して終了する。

## 計画
1. 既存フォーマッタに関する調査
2. BigQueryの構文解析器を実装する
3. 構文木からフォーマット済みのSQLを返す実装をする
4. 列名の評価を行う実装をする

## 作成物の使用例

``` bash
cat example.sql | bqformat > formatted.sql
```
