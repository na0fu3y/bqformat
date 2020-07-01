load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "com_google_zetasql",
    strip_prefix = "zetasql-2020.04.1",
    urls = [
      "https://github.com/google/zetasql/archive/2020.04.1.tar.gz",
    ],
    sha256 = "b1eab290101a3e4899a30f459579c590b0168bdd82fceede8bde1214eb01843d"
)

load("@com_google_zetasql//bazel:zetasql_deps_step_1.bzl", "zetasql_deps_step_1")

zetasql_deps_step_1()

load("@com_google_zetasql//bazel:zetasql_deps_step_2.bzl", "zetasql_deps_step_2")

zetasql_deps_step_2()
