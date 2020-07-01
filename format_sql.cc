#include "zetasql/public/sql_formatter.h"


int main(int argc, char* argv[]) {
    const std::string sql(std::istreambuf_iterator<char>(std::cin), {});
    const std::string formatted_sql;

    const absl::Status status = zetasql::FormatSql(sql, &formatted_sql);

    if (!status.ok()) {
        std::cerr << status.ToString() << std::endl;
        return 1;
    }

    std::cout << formatted_sql << std::endl;
    return 0;
}

