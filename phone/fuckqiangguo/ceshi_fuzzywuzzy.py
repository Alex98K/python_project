from fuzzywuzzy import fuzz, process
import json

all_title = []
all_answer = []
new_question = [1]
new_answer = [1]

print(len(all_title))
print(len(all_answer))

# pp = fuzz.partial_ratio("中国特色社会主义有很多特点和特", "中国特色社会主义有很多特点和特征，但最本质的特征是()")
# lis = ['中国特义有很多特点和特', '中国特色社会主义有和特', '中国特多特点和特']
for index, item in enumerate(all_title):
    # str1 = "中国特色社会主义有很多特点和特"
    # res = process.extract(i, all_title, limit=2)
    # print(res)
    find_title, res = process.extractOne(item, new_question)
    # print(find_title, res)
    if res >= 95:
        continue
    else:
        new_question.append(item)
        new_answer.append(all_answer[index])
# print(new_question)
# print(new_answer)
all_qs = []
double = []
for j in range(1, len(new_question)):
    single = {"title": str(new_question[j]), "answer": str(new_answer[j])}
    double.append(single)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(double, f, ensure_ascii=False)

# Reading data back
# with open('data.json', 'r') as f:
#     data = json.load(f)


# find_title = process.extractOne(str1, all_title)
# find_answer_number = all_title.index(find_title[0])
# print(all_answer[find_answer_number])
# print(process.extract(str1, all_title, limit=10))



