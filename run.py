import sys  
import collections
import json
import os
import operator

# Output Json
output_json = "jibun_list.json"

# 현재 디렉토리
path = os.path.join(os.getcwd(), "2019_06_DB")

# .txt 파일 디렉토리 리스트
entries = []

for entry in os.scandir(path): 
    if entry.path.endswith(".txt"):
        entries.append(entry.path)

# Main Dictionary
dic = {}

for entry in entries:
    with open(entry,'r',encoding="euc-kr") as f:
        
        for line in f:
            # 데이터 스플릿
            line_to_list = line.split('|')
            # 시도
            sido = line_to_list[3].strip()
            # 구시군
            gun = line_to_list[4].strip()
            # 읍면동
            dong = line_to_list[5].strip()

            # 리 처리
            if line_to_list[6] != "":
                dong = dong+" "+line_to_list[6]

            # Build nested dict
            if sido not in dic:
                dic[sido] = {}
            if gun not in dic[sido]:
                dic[sido][gun] = set()

            dic[sido][gun].add(dong)

# Order dong, li name 
def set_default(obj):
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError

# Sort Dic by each key (not top level key)
sorted_dic = {k:collections.OrderedDict(sorted(v.items())) for k,v in dic.items()}

# Write in json
with open(output_json, 'w') as f:
    json.dump(sorted_dic, f, ensure_ascii=False, indent=4, default=set_default)