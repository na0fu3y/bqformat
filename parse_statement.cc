#include "zetasql/parser/parser.h"


int main(int argc, char* argv[]) {
    const std::string sql(std::istreambuf_iterator<char>(std::cin), {});
    const std::unique_ptr<zetasql::ParserOutput> parser_output;

    const absl::Status status = zetasql::ParseStatement(sql, zetasql::ParserOptions(), &parser_output);

    if (!status.ok()) {
        std::cerr << status.ToString() << std::endl;
        return 1;
    }

    std::cout << parser_output->statement()->DebugString();
    return 0;
}
