# -*- coding:utf-8 -*-
# 都君丨大魔王
import json

with open('./setting.json', encoding='utf-8') as f:
    system_info_json = json.load(f)

system_info_list = system_info_json.items()
