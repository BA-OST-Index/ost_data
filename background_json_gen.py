import os
import json

all_files = list(os.listdir("background"))
all_files.remove("_all.json")

json_content = {}
for i in all_files:
    name = f"[{i[:-5]}_NAME]"
    desc = f"[{i[:-5]}_DESC]"
    json_content[name] = i[:-5]
    json_content[desc] = f"{i[:-5]} Description"

fp = "i18n/en/background.json"
fp2 = "i18n/zh_cn/background.json"
for i in [fp, fp2]:
    with open(i, encoding="UTF-8", mode="w") as file:
        json.dump(json_content, file, ensure_ascii=False,
                  indent=2)
