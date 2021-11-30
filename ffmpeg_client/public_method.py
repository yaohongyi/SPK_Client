# -*- coding:utf-8 -*-
# 都君丨大魔王
import subprocess
import json
import time
import uuid
import os
import logging
from configparser import ConfigParser

windows_sep = os.sep


def log_config():
    root_logger = logging.getLogger()
    root_logger.setLevel('INFO')
    basic_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)
    # fh = logging.FileHandler(log_path, encoding='utf-8')
    # fh.setFormatter(formatter)
    # root_logger.addHandler(fh)


log_config()


def read_ini(section, option):
    cp = ConfigParser()
    cp.read('./config/config.ini', encoding='utf-8-sig')
    value = cp.get(section, option)
    return value


def dict_format_beautify(dict_data):
    """字典类型数据格式化"""
    beautify_object = json.dumps(dict_data, indent=4, ensure_ascii=False, separators=(',', ':'))
    return beautify_object


def get_file_name(file_path):
    """获取文件名"""
    file_path_split = file_path.split('/')
    file_name = file_path_split[-1]
    return file_name


def tencent2other(input_file, output_path, temp_pcm_sampling=16000):
    """QQ微信语音文件转其他格式，包括：*.amr;*.silk;*.slk;*.aud;"""
    exists_result = os.path.exists(input_file)
    temp_file = f"{os.environ['TMP']}{os.sep}temp.pcm"
    if exists_result:
        tencent2pcm = f"./bin/silk_v3_decoder.exe {input_file} {temp_file} -Fs_API {temp_pcm_sampling} -quiet"
        logging.info(f'腾讯专有格式转PCM格式：\n{tencent2pcm}')
        subprocess.Popen(tencent2pcm, shell=True, stdout=subprocess.PIPE)
        pcm2other = f"./bin/ffmpeg.exe -y -f s16le -ar {temp_pcm_sampling} -ac 1 -i {temp_file} -v quiet {output_path}"
        logging.info(f'PCM格式转其他格式：\n{pcm2other}')
        subprocess.Popen(pcm2other, shell=True, stdout=subprocess.PIPE)
        return output_path
    else:
        logging.warning(f'输入文件{input_file}文件不存在！~')


class FFmpegTool:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_info(self):
        """获取文件信息"""
        if self.file_path.endswith(('amr', 'silk', 'slk', 'aud')):
            output_path = f"{os.environ['TMP']}{os.sep}{uuid.uuid4()}.wav"
            file_path = tencent2other(self.file_path, output_path)
            logging.info(f'临时文件存放路径：{file_path}。')
            command = f'./bin/ffprobe.exe -show_format -of json -show_streams -v quiet {file_path}'
            time.sleep(1)
        else:
            command = f'./bin/ffprobe.exe -show_format -of json -show_streams -v quiet {self.file_path}'
        logging.info(f'获取文件信息：\n{command}')
        result = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE).stdout
        list_std = result.readlines()
        str_temp = ''
        for i in list_std:
            str_temp += bytes.decode(i.strip())
        file_info = json.loads(str_temp)
        return file_info

    @staticmethod
    def get_format_name(file_info):
        """获取文件格式"""
        format_name = file_info.get('format').get('format_name')
        format_long_name = file_info.get('format').get('format_long_name')
        return format_name, format_long_name

    @staticmethod
    def get_duration(file_info):
        """获取文件时长"""
        duration = float(file_info.get('format').get('duration'))
        return f"{duration:.3f}"

    @staticmethod
    def get_file_size_with_unit(file_info):
        """获取文件大小(带单位)"""
        size = int(file_info.get('format').get('size'))
        if size < 1024:  # B
            result = f'{size:.2f}Byte'
        elif 1024 <= size < 1048576:  # KB
            size = size / 1024
            result = f'{size:.2f}KB'
        elif 1048576 <= size < 1073741824:  # M
            size = size / 1024 / 1024
            result = f'{size:.2f}M'
        else:  # G
            size = size / 1024 / 1024 / 1024
            result = f'{size:.2f}G'
        return result

    @staticmethod
    def get_file_size_no_unit(file_info):
        """获取文件大小(不带单位)"""
        size = int(file_info.get('format').get('size'))
        return size

    @staticmethod
    def get_audio_streams_info(file_info):
        """获取音频流信息"""
        streams = file_info.get('streams')
        audio_info_list = list()
        for stream in streams:
            codec_type = stream.get('codec_type')
            if codec_type == 'audio':
                audio_info = dict()
                audio_info['sample_rate'] = stream.get('sample_rate')  # 采样率Hz
                audio_info['channels'] = stream.get('channels')  # 声道数
                audio_info['bit_rate'] = stream.get('bit_rate')  # 比特率
                audio_info_list.append(audio_info)
        return audio_info_list

    @staticmethod
    def get_video_streams_info(file_info):
        """获取视频流信息"""
        streams = file_info.get('streams')
        video_info_list = list()
        for stream in streams:
            codec_type = stream.get('codec_type')
            if codec_type == 'video':
                video_info = dict()
                # 获取视频分辨率
                width = stream.get('width')
                height = stream.get('height')
                resolution = f"{width}*{height}"
                video_info['resolution'] = resolution
                video_info_list.append(video_info)
        return video_info_list


def cut_by_size(cut_file_path, cut_size, save_file_name):
    """按大小切割音视频文件"""
    command = rf"./bin/ffmpeg.exe -i {cut_file_path} -y -c:a copy -fs {cut_size} {save_file_name}"
    logging.info(f'音频指定大小切割：\n{command}')
    subprocess.Popen(command, shell=False)


def cut_by_time(cut_file_path, save_dir, start_time, end_time):
    """指定时间段切割"""
    file_name = cut_file_path.split('/')[-1]
    save_path = f"{save_dir}/切割音频_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}_{file_name}"
    command = rf"./bin/ffmpeg.exe -i {cut_file_path} -ss {start_time} -to {end_time} -y -c:a copy {save_path}"
    logging.info(f'音频指定时间段切割：\n{command}')
    subprocess.Popen(command, shell=False)


def list_dir_wav_paths(target_dir):
    """获取指定目录下所有wav音频文件的绝对路径，其他格式文件丢弃"""
    file_list = os.listdir(target_dir)
    file_paths = list()
    for file in file_list:
        file_format = file.split('.')[-1]
        if file_format == 'wav':
            file_path = f"{target_dir}/{file}"
            file_paths.append(file_path)
    return file_paths


conversion_general_format = read_ini('filter', 'conversion_general_format').split('、')
conversion_tencent_format = read_ini('filter', 'conversion_tencent_format').split('、')
conversion_all_format = []
conversion_all_format.extend(conversion_general_format)
conversion_all_format.extend(conversion_tencent_format)


def list_dir_media_paths(target_dir):
    """"""
    file_list = os.listdir(target_dir)
    file_paths = list()
    for file in file_list:
        file_format = file.split('.')[-1]
        if file_format in conversion_all_format:
            file_path = f"{target_dir}/{file}"
            file_paths.append(file_path)
    return file_paths


def count_format_num(file_paths):
    """"""
    file_formats = set()
    for file_path in file_paths:
        file_format = file_path.split('.')[-1]
        file_formats.add(file_format)
    format_num = len(file_formats)
    if format_num > 1:
        return format_num, None
    else:
        return format_num, list(file_formats)[0]


def write_list_file(file_list):
    """将音频文件绝对路径写入文件"""
    with open('file_list.txt', 'w', encoding='utf-8') as f:
        for file in file_list:
            f.write(f"file '{file}'\n")


def stitch_audio(save_dir, save_format, list_file_path='file_list.txt'):
    """音频拼接"""
    save_path = f"{save_dir}/音频拼接.{save_format}"
    command = f'ffmpeg.exe -f concat -safe 0 -i {list_file_path} -y -c copy {save_path}'
    logging.info(f'音频拼接：\n{command}')
    subprocess.Popen(command, shell=False)


def resample(source_file_path, sample_rate, save_path):
    """音频重采样"""
    command = f"ffmpeg.exe -i {source_file_path} -ar {sample_rate} {save_path}"
    logging.info(f'音频重采样：\n{command}')
    subprocess.Popen(command, shell=False)


if __name__ == '__main__':
    tencent2other(r'D:\tencent-amr.amr', r'D:\out_amr.wav')
