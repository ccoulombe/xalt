#ifndef PARSEJSONSTR_H
#define PARSEJSONSTR_H

#include "xalt_types.h"
#include "jsmn.h"
void processArray(  const char* name, const char* js, int& i, int ntokens, jsmntok_t* tokens, Vstring& vA);
void processSet(    const char* name, const char* js, int& i, int ntokens, jsmntok_t* tokens, Set& set);
void processTable(  const char* name, const char* js, int& i, int ntokens, jsmntok_t* tokens, Table& t);
void processDTable( const char* name, const char* js, int& i, int ntokens, jsmntok_t* tokens, DTable& t);
void processLibA(   const char* name, const char* js, int& i, int ntokens, jsmntok_t* tokens, std::vector<Libpair>& libA);

void parseRunJsonStr(const char* name, std::string& jsonStr, std::string& usr_cmdline, std::string& hash_id,
                     Table& envT, Table& userT, DTable& userDT, Table& recordT, std::vector<Libpair>& libA,
                     std::vector<ProcessTree>& ptA);
void parseLinkJsonStr(const char* name, std::string& jsonStr, Vstring& linklineA, Table& resultT,
                      std::vector<Libpair>& libA, Set& funcSet);

void parseCompTJsonStr(const char* name, std::string& jsonStr, std::string& compiler, std::string& compilerPath,
                       Vstring& linklineA);


#endif // PARSEJSONSTR_H
