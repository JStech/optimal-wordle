#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

bool ReadWordsFromFile(const std::string& filename, int n, std::vector<std::string>& list) {
  std::ifstream infile(filename);
  if (!infile.is_open()) {
    return false;
  }
  list.resize(0);
  std::string line;
  while (std::getline(infile, line)) {
    // trim trailing whitespace
    line.erase(std::find_if(line.rbegin(), line.rend(), [](unsigned char c) { return !std::isspace(c); }).base(),
        line.end());
    if (line.size() != n) {
      continue;
    }
    list.push_back(line);
  }
  return true;
}

int main(int argc, char* argv[]) {
  if (argc != 4) {
    std::cerr << "Usage: " << argv[0] << " n wordlist solutionlist" << std::endl;
    std::cerr << "  n:             number of letters" << std::endl;
    std::cerr << "  wordlist:      list of valid guesses" << std::endl;
    std::cerr << "  solutionlist:: list of possible solutions" << std::endl;
    return -1;
  }

  std::vector<std::string> wordlist;
  std::vector<std::string> solutionlist;

  int n = atoi(argv[1]);
  ReadWordsFromFile(std::string(argv[2]), n, wordlist);
  ReadWordsFromFile(std::string(argv[3]), n, solutionlist);
  std::cout << "Words: " << wordlist.size() << std::endl;
  std::cout << "Solutions: " << solutionlist.size() << std::endl;
}
