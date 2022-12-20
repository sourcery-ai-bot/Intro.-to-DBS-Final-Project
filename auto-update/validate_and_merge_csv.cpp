#include <cmath>
#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <algorithm>

std::vector<std::string> get_cryptocurrency_types();
void add_Type_column_to_csv(std::string);
std::vector<std::string> get_lines(std::string);
void validate_line(std::string&);
void output_lines(std::vector<std::string>, std::string);
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

    system("rename __output__ __output__.csv");

    std::cout << "All records are validated.\n";
    std::cout << "The result is in __output__.csv\n";
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
    std::vector<std::string> lines(get_lines(cryptocurrency_type));
    for (auto line = lines.begin() + 1, end = lines.end(); line < end; line++)
        validate_line(*line);
    output_lines(lines, cryptocurrency_type);
}
std::vector<std::string> get_lines(std::string cryptocurrency_type) {
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

    return lines;
}
void validate_line(std::string& line) {
    // "Dec 05, 2022","16,936.60","17,145.48","17,399.99","16,837.61","0.00K","-1.22%"
    // 
    std::string result(line.substr(0, line.find(",\"")) + ",");
    line = line.substr(line.find(",\"") + 1);

    // "16,936.60","17,145.48","17,399.99","16,837.61","0.00K","-1.22%"
    // "Dec 05, 2022",
    auto remove_comma = [](std::string str) -> std::string {
        if (str == "\"-\"") return "";
        std::string result;
        for (auto& i : str)
            if (i != ',')
                result.push_back(i);
        return result;
    };
    for (int i = 0; i < 4; ++i) {
        result += remove_comma(line.substr(0, line.find(",\""))) + ",";
        line = line.substr(line.find(",\"") + 1);
    }

    // "0.00K","-1.22%"
    // "Dec 05, 2022","16936.60","17145.48","17399.99","16837.61",
    auto to_number = [](std::string str) -> std::string {
        if (str == "-") return ",";
        std::vector<char> magnitude({ 'K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y' });
        auto position = std::find(magnitude.begin(), magnitude.end(), str.back());
        if (position == magnitude.end()) return str;
        return "\"" + std::to_string(std::stold(str) * pow(1000, position - magnitude.begin() + 1)) + "\",";
    };
    result += to_number(line.substr(1, line.find(",\"") - 2));
    line = line.substr(line.find(",\"") + 2);

    // -1.22%"
    // "Dec 05, 2022","16936.60","17145.48","17399.99","16837.61","0.00",
    auto remove_percent = [](std::string str) -> std::string {
        if (str == "-\"") return "";
        return "\"" + std::to_string(std::stold(str) * static_cast<long double>(0.01)) + "\"";
    };
    line = result + remove_percent(line);
}
void output_lines(std::vector<std::string> lines, std::string cryptocurrency_type) {
    std::ofstream fout("__output__", std::ios::out|std::ios::app);

    if (fout.fail()) throw std::runtime_error("Failed to open __output__\n");

    // fout << "\"Type\"," << lines[0] << '\n';
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