load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "com_google_zetasql",
    strip_prefix = "zetasql-2020.06.1",
    urls = [
      "https://github.com/google/zetasql/archive/2020.06.1.tar.gz",
    ],
    sha256 = "fb82060f525177117181dfad1a629d1dc13f76dd5779e5a393d6405fb627100c"
)

load("@com_google_zetasql//bazel:zetasql_deps_step_1.bzl", "zetasql_deps_step_1")

zetasql_deps_step_1()

load("@com_google_zetasql//bazel:zetasql_deps_step_2.bzl", "zetasql_deps_step_2")

zetasql_deps_step_2()
