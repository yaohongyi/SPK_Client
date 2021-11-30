# -*- coding:utf-8 -*-
# 都君丨大魔王
import os
import json
import requests
from PyQt5 import QtCore
from pathlib import Path


sep = os.sep


class CreateV2C(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    def __init__(self, client_info):
        super(CreateV2C, self).__init__()
        self.client_info = client_info

    def get_level_2_dir_paths(self):
        """获得一级目录下的二级目录"""
        level_1_dir = self.client_info['level_1_dir']
        if level_1_dir is False:
            self.msg.emit('请先选择一级目录！！！')
        else:
            dir_exists = Path(level_1_dir).exists()
            if dir_exists:
                level_2_dir_name_list = os.listdir(level_1_dir)
                if level_2_dir_name_list:
                    level_2_dir_path_list = list()
                    for level_2_dir_name in level_2_dir_name_list:
                        level_2_dir_path = os.path.join(level_1_dir, level_2_dir_name)
                        level_2_dir_path_list.append(level_2_dir_path)
                    return level_2_dir_path_list
                else:
                    self.msg.emit(f'一级目录 {level_1_dir} 下没有加密狗文件夹，请详细阅读使用须知！！！')
            else:
                self.msg.emit(f'所选一级目录[{level_1_dir}]不存在！！！')

    @staticmethod
    def get_hardware_info(level_2_dir_path):
        file_name_list = os.listdir(level_2_dir_path)
        for file_name in file_name_list:
            if file_name.endswith('txt'):
                hardware_info_file_name = file_name
                hardware_info_file_path = os.path.join(level_2_dir_path, hardware_info_file_name)
                with open(hardware_info_file_path, encoding='utf-8') as f:
                    hardware_info = f.readline()
                return hardware_info

    @staticmethod
    def get_c2v_info(level_2_dir_path):
        file_name_list = os.listdir(level_2_dir_path)
        for file_name in file_name_list:
            if file_name.endswith('c2v'):
                c2v_file_path = os.path.join(level_2_dir_path, file_name)
                with open(c2v_file_path, 'rb') as f:
                    hardware_info = f.read()
                return hardware_info

    def create_features_info(self):
        """生成特征信息"""
        feature_id_list = self.client_info['feature_list']
        expire_date = self.client_info['expire_date']
        feature_list = list()
        for feature_id in feature_id_list:
            simple_feature_info = {
                "id": feature_id,
                "name": "特征名称",
                "license_properties": {
                    "expiration_date": f"{expire_date}",
                    "remote_desktop_access": "No"}
            }
            feature_list.append(simple_feature_info)
        return feature_list

    def create_resources_info(self, level_2_dir_path):
        """生成绑定硬件信息及加密狗备注信息"""
        hardware_info = self.get_hardware_info(level_2_dir_path)
        remark_info = level_2_dir_path.split(sep)[-1]
        resources_info = [
            {"id": 1, "content": hardware_info},
            {"id": 2, "content": remark_info}
        ]
        return resources_info

    def get_json_content(self, level_2_dir_path):
        """生成接口请求的update信息，以json文件保存"""
        update_content = dict()
        update_content['features'] = self.create_features_info()
        update_content['resources'] = self.create_resources_info(level_2_dir_path)
        update_content = json.dumps(update_content, indent=4, ensure_ascii=False, separators=(',', ':'))
        json_file_path = os.path.join(level_2_dir_path, 'def.json')
        with open(json_file_path, 'w+', encoding='utf-8') as f:
            f.write(update_content)
        with open(json_file_path, 'rb') as f2:
            json_content = f2.read()
        return json_content

    def interface_request(self, level_2_dir_path):
        """"""
        url = "http://localhost:7777/update"
        files = {
            'c2v': ('license.c2v', self.get_c2v_info(level_2_dir_path), 'application/octet-stream'),
            'update': ('def.json', self.get_json_content(level_2_dir_path), 'application/json')
        }
        res = requests.post(url, files=files).text
        return res

    def create_c2v_file(self):
        level_2_dir_paths = self.get_level_2_dir_paths()
        if level_2_dir_paths:
            for level_2_dir_path in level_2_dir_paths:
                res = self.interface_request(level_2_dir_path)
                v2c_file_path = os.path.join(level_2_dir_path, 'license.v2c')
                with open(v2c_file_path, 'w+', encoding='utf-8') as f:
                    f.write(res)
                self.msg.emit(f'已完成{level_2_dir_path.split(sep)[-1]}加密狗授权！')

    def run(self) -> None:
        self.create_c2v_file()


if __name__ == '__main__':
    test_client_info = {
        'level_1_dir': r'C:\Users\yaoch\Desktop\加密狗授权'
    }
    create_v2c = CreateV2C(test_client_info)
    test_level_2_dir_path = r'C:\Users\yaoch\Desktop\加密狗授权\深圳办测试机正40号'
    create_v2c.create_resources_info(test_level_2_dir_path)
