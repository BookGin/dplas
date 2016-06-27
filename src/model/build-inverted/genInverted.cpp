#include <cassert>
#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

#include "json.hpp"
using namespace std;

using Map = unordered_map<string, int>;
using Set = unordered_set<string>;
using Json = nlohmann::json;

void mapInsert(Map& vocab, string& term) {
  if (vocab.find(term) == vocab.end())
    vocab.insert({term, 1});
  else
    vocab.at(term) ++;
}

int main(int argc, char* argv[])
{
  int total_len = 0;
  int total_doc = 0;
  Map vocab;
  Map doc_freq;

  ifstream fp(argv[1]);
  assert(fp);

  string line; 
  while (getline(fp, line)) {
    total_doc ++;
    stringstream doc(line);
    string term;
    Set uniq_terms;

    while (getline(doc, term, ' ')) {
      total_len ++;
      mapInsert(vocab, term);
      if (uniq_terms.find(term) == uniq_terms.end())
        mapInsert(doc_freq, term);
      uniq_terms.insert(term);
    }
  }
  fp.close();
  Json json_vocab(vocab);
  Json json_freq(doc_freq);
  Json json_misc;
  json_misc["total_doc"] = total_doc;
  json_misc["total_len"] = total_len;
  json_misc["avg_len"] = double(total_len) / total_doc;

  ofstream out_vocab(string(argv[2]) + string(".vocab"));
  out_vocab << json_vocab.dump();
  ofstream out_freq(string(argv[2]) + string(".freq"));
  out_freq << json_freq.dump();
  ofstream out_misc(string(argv[2]) + string(".misc"));
  out_misc << json_misc.dump();

  out_vocab.close();
  out_freq.close();
  out_misc.close();
  return 0;
}
