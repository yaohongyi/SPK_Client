# -*- coding:utf-8 -*-
# 都君丨大魔王
import random
import time
import docx
from datetime import datetime
from faker import Faker
from source_file.identity_card_prefix import identity_card_prefix
from source_file.bank_card_prefix import bank_card_prefix
from source_file.field_map_info import field_map_info
from source_file.relation import relative_relation, normal_relation, interrelation
from source_file.letter_num_str import upper_letter, letter, other_element, split_str_list
from source_file.desc_key import phone_desc_keys, education_desc_keys
from source_file.education_level import education_level_list
from source_file.political_status import political_status_list
from source_file.brigade import brigade_list
from source_file.gat_region import gat_region
from source_file.wechat_nickname import wechat_nickname_list


zh_fake = Faker('zh_CN')
en_fake = Faker('en')


def create_zh_name() -> str:
    """生成中文名"""
    name = zh_fake.name()
    return name


def create_en_name():
    """生成英文名"""
    name = en_fake.name()
    return name


def create_email():
    """生成邮箱"""
    email = zh_fake.email()
    return email


def create_qq():
    """生成QQ号"""
    qq = random.randint(10000, 9999999999)
    return qq


def create_wei_xin():
    """生成微信账号"""
    account_prefix = random.choice(other_element)
    account_residue_len = random.randint(5, 19)
    account_postfix_list = list()
    for x in range(account_residue_len):
        account_postfix_list.append(random.choice(other_element))
    account_postfix = ''.join(account_postfix_list)
    wei_xin_account = account_prefix + account_postfix
    return wei_xin_account


def create_wechat_nickname():
    """生成微信昵称"""
    wechat_nickname = random.choice(wechat_nickname_list)
    return wechat_nickname


wechat_nickname_prefix_list = ['微信昵称', '昵称']


def create_wechat_nickname_desc():
    """生成微信昵称描述"""
    wechat_nick_name_prefix = random.choice(wechat_nickname_prefix_list)
    wechat_nickname_desc = f"{wechat_nick_name_prefix}：{create_wechat_nickname()}"
    return wechat_nickname_desc


def create_twitter():
    """生成推特账号"""
    account_prefix = random.choice(letter)
    account_residue_len = random.randint(1, 49)
    account_postfix_list = list()
    for x in range(account_residue_len):
        account_postfix_list.append(random.choice(other_element))
    account_postfix = ''.join(account_postfix_list)
    twitter_account = account_prefix + account_postfix
    return twitter_account


with open('./source_file/nickname.txt', 'r') as file:
    content = file.read()
    nicknames = content.split(' ')


def create_nickname():
    """生成绰号"""
    nickname = random.choice(nicknames)
    return nickname


def create_education():
    """生成学历"""
    education = random.choice(education_level_list)
    return education


def create_education_desc():
    """生成文化程度描述信息"""
    education = create_education()
    desc_key = random.choice(education_desc_keys)
    if desc_key == '学历':
        education_desc = f"{education}{desc_key}"
    elif desc_key == '':
        education_desc = f"{education}"
    else:
        split_str = random.choice(split_str_list)
        education_desc = f"{desc_key}{split_str}{education}"
    return education_desc


def create_political_status():
    """生成政治面貌"""
    political_status = random.choice(political_status_list)
    return political_status


def create_brigade_info():
    """生成大队信息"""
    brigade = random.choice(brigade_list)
    return brigade


def create_job():
    """生成职业"""
    job = zh_fake.job()
    return job


def create_id_card():
    """生成国内身份证"""
    id_card = zh_fake.ssn()
    return id_card


with open('./source_file/nation.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    nation_list = content.split('、')


def create_nation():
    """生成民族"""
    nation = random.choice(nation_list)
    return nation


def create_gender():
    """生成性别"""
    gender = random.choice(['男', '女'])
    return gender


def create_domicile():
    """生成籍贯、户籍地"""
    domicile_list = list(identity_card_prefix.values())
    domicile_list.extend(gat_region)
    domicile = random.choice(domicile_list)
    return domicile


def create_gat_domicile():
    """生成港澳台户籍地址"""
    domicile_list = gat_region
    domicile = random.choice(domicile_list)
    return domicile


with open('./source_file/community.txt', 'r', encoding='utf-8') as file:
    community_content = file.read()
    community_list = community_content.split(' ')


def create_reside_address():
    """生成居住地"""
    reside_list = list(identity_card_prefix.values())
    reside_list.extend(gat_region)
    reside = random.choice(reside_list)
    community = random.choice(community_list)
    build_num = str(random.randint(1, 100))
    room_num = str(random.randint(1, 100))
    reside_address = f"{reside}{community}{build_num}栋{room_num}单元"
    return reside_address


def create_gat_reside_address():
    """生成港澳台居住地"""
    reside_list = gat_region
    reside = random.choice(reside_list)
    community = random.choice(community_list)
    build_num = str(random.randint(1, 100))
    room_num = str(random.randint(1, 100))
    reside_address = f"{reside}{community}{build_num}栋{room_num}单元"
    return reside_address


def create_phone_num():
    """生成手机号"""
    phone_num = zh_fake.phone_number()
    return phone_num


def create_phone_desc():
    """生成手机描述信息"""
    phone_desc_key = random.choice(phone_desc_keys)
    phone_num = create_phone_num()
    split_str = random.choice(split_str_list)
    phone_desc = f"{phone_desc_key}{split_str}{phone_num}"
    return phone_desc


bank_card_prefix_list = list(bank_card_prefix.keys())


def create_bank_card():
    """生成银行卡号"""
    # 获取银行卡前缀
    card_prefix = random.choice(bank_card_prefix_list)
    # 生成16或者19位长度银行卡
    card_prefix_len = len(card_prefix)
    card_len_list = [16, 19]
    card_len = random.choice(card_len_list)
    card_residue_len = card_len - card_prefix_len
    card_residue_list = list()
    for x in range(card_residue_len):
        card_residue_list.append(str(random.randint(0, 9)))
    card_postfix = ''.join(card_residue_list)
    card_num = card_prefix + card_postfix
    return card_num


def create_tw_to_land_pass():
    """
    台湾省居民往来内地通行证/台湾省回乡证/台湾省居民通行证：8位数字
    :return:
    """
    tw_pass_list = list()
    for x in range(8):
        tw_pass_list.append(str(random.randint(0, 9)))
    tw_pass = ''.join(tw_pass_list)
    return tw_pass


def create_land_to_tw_pass():
    """
    台湾省通行证：L+8位数字、T+8位数字
    :return:
    """
    pass_prefix = random.choice(['L', 'T'])
    land_to_tw_pass_list = list()
    for x in range(8):
        land_to_tw_pass_list.append(str(random.randint(0, 9)))
    land_to_tw_pass = pass_prefix + ''.join(land_to_tw_pass_list)
    return land_to_tw_pass


def create_tw_id():
    """
    台湾省身份证：1位字母+9位数字
    :return:
    """
    tw_id_prefix = random.choice(upper_letter)
    tw_id_postfix_list = list()
    for x in range(9):
        tw_id_postfix_list.append(str(random.randint(0, 9)))
    tb_postfix = ''.join(tw_id_postfix_list)
    tb_id = tw_id_prefix + tb_postfix
    return tb_id


def create_hk_to_land_pass_1():
    """
    香港居民往来内地通行证/香港回乡证/香港居民通行证：H + 8位数字 +2位数字（代表换证次数），总位数11位
    :return: 香港居民往来内地通行证/香港回乡证/香港居民通行证
    """
    hk_pass_postfix_list = list()
    for x in range(10):
        hk_pass_postfix_list.append(str(random.randint(0, 9)))
    hk_pass_postfix = ''.join(hk_pass_postfix_list)
    hk_pass = f"H{hk_pass_postfix}"
    return hk_pass


def create_hk_to_land_pass_2():
    """
    香港居民往来内地通行证/香港回乡证/香港居民通行证：H + 8位数字，相较于上面的方法少两位位数字
    :return: 香港居民往来内地通行证/香港回乡证/香港居民通行证
    """
    hk_pass_postfix_list = list()
    for x in range(8):
        hk_pass_postfix_list.append(str(random.randint(0, 9)))
    hk_pass_postfix = ''.join(hk_pass_postfix_list)
    hk_pass = f"H{hk_pass_postfix}"
    return hk_pass


def create_hk_to_land_pass():
    """
    生成香港回乡证，随机调用2种生成方法中的一种
    :return:
    """
    method_list = [create_hk_to_land_pass_1, create_hk_to_land_pass_2]
    finally_method = random.choice(method_list)
    hk_id = finally_method()
    return hk_id


def create_hk_id_1():
    """
    香港身份证：1位字母+6位数字+(1位数字)，英文括号
    :return: 香港身份证
    """
    hk_id_prefix = random.choice(upper_letter)
    hk_id_postfix_list = list()
    for x in range(6):
        hk_id_postfix_list.append(str(random.randint(0, 9)))
    hk_postfix = ''.join(hk_id_postfix_list)
    hk_id = f"{hk_id_prefix}{hk_postfix}({random.randint(0, 9)})"
    return hk_id


def create_hk_id_2():
    """
    香港身份证：1位字母+6位数字+（1位数字），中文括号
    :return: 香港身份证
    """
    hk_id_prefix = random.choice(upper_letter)
    hk_id_postfix_list = list()
    for x in range(6):
        hk_id_postfix_list.append(str(random.randint(0, 9)))
    hk_postfix = ''.join(hk_id_postfix_list)
    hk_id = f"{hk_id_prefix}{hk_postfix}（{random.randint(0, 9)}）"
    return hk_id


def create_hk_id_3():
    """
    香港身份证：1位字母+6位数字，没有括号及括号内的数字
    :return: 香港身份证
    """
    hk_id_prefix = random.choice(upper_letter)
    hk_id_postfix_list = list()
    for x in range(6):
        hk_id_postfix_list.append(str(random.randint(0, 9)))
    hk_postfix = ''.join(hk_id_postfix_list)
    hk_id = f"{hk_id_prefix}{hk_postfix}"
    return hk_id


def create_hk_id():
    """
    生成香港身份证，随机调用3种生成的香港身份证的方法之一进行生成。
    :return:
    """
    method_list = [create_hk_id_1, create_hk_id_2, create_hk_id_3]
    finally_method = random.choice(method_list)
    hk_id = finally_method()
    return hk_id


def create_mc_to_land_pass_1():
    """
    澳门居民往来内地通行证/澳门回乡证：M+8位数字+2位数字（代表换证次数）
    :return: 澳门居民往来内地通行证/澳门回乡证
    """
    mc_pass_postfix_list = list()
    for x in range(10):
        mc_pass_postfix_list.append(str(random.randint(0, 9)))
    mc_pass_postfix = ''.join(mc_pass_postfix_list)
    mc_pass = f"M{mc_pass_postfix}"
    return mc_pass


def create_mc_to_land_pass_2():
    """
    澳门居民往来内地通行证/澳门回乡证：M+8位数字
    :return: 澳门居民往来内地通行证/澳门回乡证
    """
    mc_pass_postfix_list = list()
    for x in range(8):
        mc_pass_postfix_list.append(str(random.randint(0, 9)))
    mc_pass_postfix = ''.join(mc_pass_postfix_list)
    mc_pass = f"M{mc_pass_postfix}"
    return mc_pass


def create_mc_to_land_pass():
    """
    生成澳门居民往来内地通行证/澳门回乡证，调用2种随机方法之一生成
    :return:
    """
    method_list = [create_mc_to_land_pass_1, create_mc_to_land_pass_2]
    finally_method = random.choice(method_list)
    mc_pass = finally_method()
    return mc_pass


def create_mc_id_1():
    """
    澳门身份证：7位数字+（1位数字），中文括号
    :return:
    """
    mc_id_prefix = random.choice(['1', '5', '7'])
    mc_id_middle_list = list()
    for x in range(6):
        mc_id_middle_list.append(str(random.randint(0, 9)))
    mc_id_middle = ''.join(mc_id_middle_list)
    mc_id = f"{mc_id_prefix}{mc_id_middle}（{random.randint(0, 9)}）"
    return mc_id


def create_mc_id_2():
    """
    澳门身份证：7位数字+(1位数字)，英文括号
    :return:
    """
    mc_id_prefix = random.choice(['1', '5', '7'])
    mc_id_middle_list = list()
    for x in range(6):
        mc_id_middle_list.append(str(random.randint(0, 9)))
    mc_id_middle = ''.join(mc_id_middle_list)
    mc_id = f"{mc_id_prefix}{mc_id_middle}({random.randint(0, 9)})"
    return mc_id


def create_mc_id_3():
    """
    澳门身份证：7位数字
    :return:
    """
    mc_id_prefix = random.choice(['1', '5', '7'])
    mc_id_middle_list = list()
    for x in range(6):
        mc_id_middle_list.append(str(random.randint(0, 9)))
    mc_id_middle = ''.join(mc_id_middle_list)
    mc_id = f"{mc_id_prefix}{mc_id_middle}"
    return mc_id


def create_mc_id():
    """
    生成澳门身份证，调用3种随机方法之一生成
    :return:
    """
    method_list = [create_mc_id_1, create_mc_id_2, create_mc_id_3]
    finally_method = random.choice(method_list)
    mc_id = finally_method()
    return mc_id


def create_land_to_gm_pass_1():
    """
    往来港澳通行证/港澳通行证：（新） C +8位数字
    :return:
    """
    num_list = list()
    for x in range(8):
        num_list.append(str(random.randint(0, 9)))
    land_to_gm_pass = 'C' + ''.join(num_list)
    return land_to_gm_pass


def create_land_to_gm_pass_2():
    """
    往来港澳通行证/港澳通行证：C+1位字母+7位数字
    :return:
    """
    num_list = list()
    for x in range(7):
        num_list.append(str(random.randint(0, 9)))
    land_to_gm_pass = 'C' + random.choice(upper_letter) + ''.join(num_list)
    return land_to_gm_pass


def create_land_to_gm_pass_3():
    """
    往来港澳通行证/港澳通行证：（旧） W+8位数字
    :return:
    """
    num_list = list()
    for x in range(8):
        num_list.append(str(random.randint(0, 9)))
    land_to_gm_pass = 'W' + ''.join(num_list)
    return land_to_gm_pass


def create_land_to_hm_pass():
    """
    往来港澳通行证/港澳通行证，调用3种随机方法之一生成
    :return:
    """
    method_list = [create_land_to_gm_pass_1, create_land_to_gm_pass_2, create_land_to_gm_pass_3]
    finally_method = random.choice(method_list)
    land_to_gm_pass = finally_method()
    return land_to_gm_pass


def create_passport_1():
    """
    护照：E+8位数字、G + 8位数字
    :return:
    """
    passport_prefix = random.choice(['G', 'E'])
    passport_postfix_list = list()
    for x in range(8):
        passport_postfix_list.append(str(random.randint(0, 9)))
    passport_postfix = ''.join(passport_postfix_list)
    passport = passport_prefix + passport_postfix
    return passport


def create_passport_2():
    """
    护照：E+1位字母+7位数字
    :return:
    """
    passport_postfix_list = list()
    for x in range(7):
        passport_postfix_list.append(str(random.randint(0, 9)))
    passport_postfix = ''.join(passport_postfix_list)
    passport = 'E' + random.choice(upper_letter) + passport_postfix
    return passport


def create_passport():
    """
    生成护照，调用2个随机方法之一
    :return:
    """
    method_list = [create_passport_1, create_passport_2]
    finally_method = random.choice(method_list)
    passport = finally_method()
    return passport


def get_time_stamp(time_object):
    """
    将时间字符串（精确到毫秒）转换为时间戳
    :param time_object:
    :return:
    """
    datetime_obj = datetime.strptime(time_object, "%Y-%m-%d %H:%M:%S.%f")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    print(obj_stamp)
    return obj_stamp


def create_diff_field_document(first_level_field_num: int = 1, file_type: str = 'txt', people_num: int = 1):
    """
    创建不同领域的文档
    :param first_level_field_num: 一级领域数，最大值19
    :param file_type:
    :param people_num: 文档中出现几个人
    :return:
    """
    name = create_zh_name()  # 姓名
    id_num = create_id_card()  # 身份证
    phone_num = create_phone_num()  # 手机号码
    people_info = f"{name}，身份证：{id_num}，手机号：{phone_num}。"
    if people_num > 1:
        name_2 = create_zh_name()  # 姓名
        id_num_2 = create_id_card()  # 身份证
        phone_num_2 = create_phone_num()  # 手机号码
        people_2_info = f"{name_2}，身份证：{id_num_2}，手机号：{phone_num_2}。"
        people_info = people_info + '\n' + people_2_info
    x = 1
    for key, value in field_map_info.items():
        for y in value:
            field_info = f"{key}_{y}"
            case_describe = f"【{field_info}】\n{people_info}"
            if file_type == 'txt':
                with open(f"./file_txt/txt_{name}_{field_info}.txt", 'w', encoding='utf-8') as f:
                    f.write(case_describe)
            else:
                doc_document = docx.Document()
                doc_document.add_paragraph(case_describe)
                doc_document.save(f"./file_doc/doc_{name}_{field_info}.docx")
        if x == first_level_field_num or x == 19:
            break
        else:
            x += 1


def create_relative_relation():
    """生成相对关系数据。例如：张三（男）"""
    relation = random.sample(relative_relation.keys(), 1)[0]
    gender_1 = relative_relation.get(relation)
    if gender_1 == '男':
        gender_2 = '女'
    else:
        gender_2 = '男'
    return relation, gender_1, gender_2


def create_interrelation():
    """生成相互关系数据。例如：张三是李四的relation_1，李四是张三的relation_2"""
    relation_1 = random.sample(interrelation.keys(), 1)[0]
    relation_2_list = interrelation.get(relation_1)
    relation_2 = random.choice(relation_2_list)
    return relation_1, relation_2


def create_normal_relation():
    """生成普通关系数据。例如：张三和李四是同事"""
    relation = random.choice(normal_relation)
    return relation


def create_relation_info_desc(relation_option, people_info_1, people_info_2):
    """"""
    people_desc_list = list()
    # 生成关系描述
    if relation_option == '相对关系':
        relation, gender_1, gender_2 = create_relative_relation()
        people_info_1['gender'] = gender_1
        people_info_2['gender'] = gender_2
        relation_desc = f"据悉，{people_info_1.get('name')}是{people_info_2.get('name')}的{relation}"
    elif relation_option == '相互关系':
        relation_1, relation_2 = create_interrelation()
        relation_desc = f"据悉，{people_info_1.get('name')}是{people_info_2.get('name')}的{relation_1}，" \
            f"{people_info_2.get('name')}是{people_info_1.get('name')}的{relation_2}"
    # relation_option == '普通关系':
    else:
        relation = create_normal_relation()
        relation_desc = f"据悉，{people_info_1.get('name')}是{people_info_2.get('name')}的{relation}"
    # 生成基本信息描述
    attribute_list_1 = list()
    for _, attribute in people_info_1.items():
        attribute_list_1.append(attribute)
    people_1_desc = '，'.join(attribute_list_1)
    people_desc_list.append(people_1_desc)
    attribute_list_2 = list()
    for _, attribute in people_info_2.items():
        attribute_list_2.append(attribute)
    people_2_desc = '，'.join(attribute_list_2)
    people_desc_list.append(people_2_desc)
    people_desc_list.append(relation_desc)
    return people_desc_list


if __name__ == "__main__":
    ...
