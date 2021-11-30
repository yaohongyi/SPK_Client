# -*- coding:utf-8 -*-
# 都君丨大魔王
from nlp import nlp_tool
from PyQt5 import QtCore


class CreateContent(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, client_info):
        super().__init__()
        self.client_info = client_info

    def create_people_info(self):
        """"""
        people_info = dict()
        if self.client_info.get('name'):
            people_info['name'] = nlp_tool.create_zh_name()  # 中文名
        if self.client_info.get('id_card'):
            people_info['id_card'] = f'身份证：{nlp_tool.create_id_card()}'  # 国内身份证
        if self.client_info.get('hk_mc_pass'):
            people_info['hk_mc_pass'] = f'港澳通行证：{nlp_tool.create_land_to_hm_pass()}'  # 港澳通行证
        if self.client_info.get('tw_pass'):
            people_info['tw_pass'] = f'台湾通行证：{nlp_tool.create_land_to_tw_pass()}'  # 台湾通行证
        if self.client_info.get('passport'):
            people_info['passport'] = f'护照号：{nlp_tool.create_passport()}'  # 护照
        if self.client_info.get('hk_id_card'):
            people_info['hk_id_card'] = f'香港身份证：{nlp_tool.create_hk_id()}'  # 香港身份证
        if self.client_info.get('hk_homecoming_permit'):
            people_info['hk_homecoming_permit'] = f'香港回乡证：{nlp_tool.create_hk_to_land_pass()}'  # 香港回乡证
        if self.client_info.get('mc_id_card'):
            people_info['mc_id_card'] = f'澳门身份证：{nlp_tool.create_mc_id()}'  # 澳门身份证
        if self.client_info.get('mc_homecoming_permit'):
            people_info['mc_homecoming_permit'] = f'澳门回乡证：{nlp_tool.create_mc_to_land_pass()}'  # 澳门回乡证
        if self.client_info.get('tw_id_card'):
            people_info['tw_id_card'] = f'台湾身份证：{nlp_tool.create_tw_id()}'  # 台湾身份证
        if self.client_info.get('tw_homecoming_permit'):
            people_info['tw_homecoming_permit'] = f'台湾回乡证：{nlp_tool.create_tw_to_land_pass()}'  # 台湾回乡证
        if self.client_info.get('foreign_passport'):
            people_info['foreign_passport'] = f'外国人护照：{nlp_tool.create_passport()}'  # 外国人护照
        if self.client_info.get('gender'):
            people_info['gender'] = f'性别：{nlp_tool.create_gender()}'  # 性别
        if self.client_info.get('nickname'):
            people_info['nickname'] = f'绰号"{nlp_tool.create_nickname()}"'  # 绰号
        if self.client_info.get('phone_number'):
            people_info['phone_number'] = nlp_tool.create_phone_desc()  # 手机号
        if self.client_info.get('english_name'):
            people_info['english_name'] = f'英文名：{nlp_tool.create_en_name()}'  # 英文名
        if self.client_info.get('nation'):
            people_info['nation'] = f'民族：{nlp_tool.create_nation()}'  # 民族
        if self.client_info.get('education'):
            people_info['education'] = nlp_tool.create_education_desc()  # 文化程度
        if self.client_info.get('political_status'):
            people_info['political_status'] = f'政治面貌：{nlp_tool.create_political_status()}'  # 政治面貌
        if self.client_info.get('job'):
            people_info['job'] = f'职业：{nlp_tool.create_job()}'  # 职业
        if self.client_info.get('email'):
            people_info['email'] = f'邮箱：{nlp_tool.create_email()}'  # 邮箱
        if self.client_info.get('native_place'):
            people_info['native_place'] = f'籍贯：{nlp_tool.create_domicile()}'  # 籍贯
        if self.client_info.get('domicile'):
            people_info['domicile'] = f'户籍地：{nlp_tool.create_domicile()}'  # 户籍地
        if self.client_info.get('residence'):
            people_info['residence'] = f'居住地：{nlp_tool.create_reside_address()}'  # 居住地
        if self.client_info.get('qq'):
            people_info['qq'] = f'QQ：{nlp_tool.create_qq()}'  # QQ号
        if self.client_info.get('wechat'):
            people_info['wechat'] = f'微信：{nlp_tool.create_wei_xin()}'  # 微信号
        if self.client_info.get('wechat_nickname'):
            people_info['wechat_nickname'] = nlp_tool.create_wechat_nickname_desc()  # 微信昵称
        if self.client_info.get('twitter'):
            people_info['twitter'] = f'推特：{nlp_tool.create_twitter()}'  # 推特号
        if self.client_info.get('bank_card'):
            people_info['bank_card'] = f'银行卡号：{nlp_tool.create_bank_card()}'  # 银行卡
        return people_info

    def create_content(self):
        """"""
        people_desc_list = list()
        people_num = self.client_info.get('people_num')
        brigade = nlp_tool.create_brigade_info()  # 大队信息
        people_relation = self.client_info.get('people_relation')
        if people_relation == '无':
            # 生成多个人员信息，人员间没有关系
            for x in range(people_num):
                people_info = self.create_people_info()
                attribute_list = []
                for _, attribute in people_info.items():
                    attribute_list.append(attribute)
                single_people_desc = '，'.join(attribute_list)
                people_desc_list.append(single_people_desc)
        else:
            people_info_1 = self.create_people_info()
            people_info_2 = self.create_people_info()
            if self.client_info.get('people_relation') == '相对关系':
                people_desc_list = nlp_tool.create_relation_info_desc('相对关系', people_info_1, people_info_2)
            elif self.client_info.get('people_relation') == '相互关系':
                people_desc_list = nlp_tool.create_relation_info_desc('相互关系', people_info_1, people_info_2)
            elif self.client_info.get('people_relation') == '普通关系':
                people_desc_list = nlp_tool.create_relation_info_desc('普通关系', people_info_1, people_info_2)
        all_people_desc = '。\n'.join(people_desc_list)
        case_desc = f"2020年12月25日，在广东省深圳市开展的一次特别活动，代号“秃鹰”，旨在打击法轮功等邪教组织。" \
            f"在领导的有效指挥，和各级部门的配合下，打击效果明晓，获得社会大众认可！其中，抓到了多名邪教骨干。" \
            f"现将涉案嫌疑人信息公布如下：\n{all_people_desc}。\n" \
            f"嫌疑人在广州天河被抓，据其交代，“法轮功”利用一家名为“神韵”的舞蹈公司，组织多个舞蹈团环游世界演出，" \
            f"不仅保障了它的生存和发展，还让其创始人赚得盆满钵满。那些不明真相的观众被蒙在鼓里，还以为自己是在支持一项伟大的慈善事业。" \
            f"2007年成立后，神韵演出扩张迅速，仅2019年6月就计划在4个国家81个城市进行表演。" \
            f"但是，与通过装扮可怜和利用貌似无害的功操来引诱人们加入“法轮功”、掩盖其独裁本质的招数一样，" \
            f"神韵通过华丽的舞美表演来粉饰其“法轮功”宣传工具的本质。\n {brigade}"
        self.text.emit(case_desc)

    def run(self):
        self.create_content()
