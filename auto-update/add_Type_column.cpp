#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <iostream>

std::vector<std::string> get_cryptocurrency_types();
void add_Type_column_to_csv(std::string);
void output_cryptocurrency_types(std::vector<std::string>);

int main() {
    std::vector<std::string> cryptocurrency_types;
    try {
        cryptocurrency_types = get_cryptocurrency_types();
        for (auto& i : cryptocurrency_types)
            add_Type_column_to_csv(i);
    }
    catch(std::runtime_error RE) {
        std::cout << RE.what() << '\n';
        return -1;
    }

    std::cout << "Done.\n";
    system("pause");

    return 0;
}

std::vector<std::string> get_cryptocurrency_types() {
    system("del __dir__.txt");
    system("dir >> __dir__.txt");

    std::ifstream fin("__dir__.txt");

    if (fin.fail()) throw std::runtime_error("Failed to open __dir__.txt\n");

    std::string temp;
    std::vector<std::string> cryptocurrency_types;
    while (std::getline(fin, temp, '\n')) {
        if (temp.size() > 4 && temp.substr(temp.size() - 4) == ".csv") {
            int end = temp.find(" Historical Data");
            if (end == std::string::npos) continue;

            // 41 is based on Windows 10 家用版 21H2
            cryptocurrency_types.push_back(temp.substr(41, end - 41));
        }
    }

    fin.close();

    system("del __dir__.txt");

    return cryptocurrency_types;
}
void add_Type_column_to_csv(std::string cryptocurrency_type) {
    std::string file = cryptocurrency_type + " Historical Data - Investing.com.csv";
    std::ifstream fin(file);

    if (fin.fail()) throw std::runtime_error("Failed to open " + file + '\n');

    // i don't know the reason, but there may be a unicode character left in the buffer
    fin.ignore(3);

    std::vector<std::string> lines(1);
    while (std::getline(fin, lines.back(), '\n'))
        lines.push_back("");
    lines.pop_back();

    fin.close();

    std::ofstream fout(file, std::ios::out|std::ios::trunc);

    if (fout.fail()) throw std::runtime_error("Failed to open " + file + '\n');

    fout << "\"Type\"," << lines[0] << '\n';
    for (auto line = lines.begin() + 1, end = lines.end(); line < end; line++)
        fout << '"' << cryptocurrency_type << "\"," << *line << '\n';

    fout.close();
}
void output_cryptocurrency_types(std::vector<std::string> cryptocurrency_types) {
    std::ofstream fout("cyptocurrency_types.txt", std::ios::out|std::ios::trunc);

    for (auto& i : cryptocurrency_types)
        fout << i << '\n';

    fout.close();
}