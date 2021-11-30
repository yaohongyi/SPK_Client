# -*- coding:utf-8 -*-
# 都君丨大魔王
import subprocess
from PyQt5 import QtCore
import public_method


conversion_general_format = public_method.read_ini('filter', 'conversion_general_format').split('、')
conversion_tencent_format = public_method.read_ini('filter', 'conversion_tencent_format').split('、')


class OriginalInfo(QtCore.QThread):
    original_msg = QtCore.pyqtSignal(str)
    key_msg = QtCore.pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.probe_tool = public_method.FFmpegTool(file_path)

    def get_original_info(self):
        original_info = self.probe_tool.get_file_info()
        # 文件名
        file_name = public_method.get_file_name(self.file_path)
        self.original_msg.emit(f"从'{file_name}'中获得的原始信息：")
        self.original_msg.emit(str(public_method.dict_format_beautify(original_info)))
        # 打印关键信息
        if original_info:
            # 文件格式
            file_format = file_name.split('.')[-1]
            if file_format in ('amr', 'silk', 'slk', 'aud'):
                self.key_msg.emit(f'{file_format}格式的文件不支持直接获取文件信息，以下信息来自转换为wav格式后！！！')
                format_name = file_format
                format_long_name = file_format
            else:
                format_name, format_long_name = self.probe_tool.get_format_name(original_info)
            self.key_msg.emit(f'文件名称：{file_name}')
            self.key_msg.emit(f'文件格式：')
            self.key_msg.emit(f'        - 简称：{format_name}')
            self.key_msg.emit(f'        - 全称：{format_long_name}')
            # 文件大小
            file_size = self.probe_tool.get_file_size_with_unit(original_info)
            self.key_msg.emit(f'文件大小：{file_size}')
            # 时长
            duration = self.probe_tool.get_duration(original_info)
            self.key_msg.emit(f'文件时长：{duration}秒')
            self.key_msg.emit(f'流信息：')
            # 音频流信息
            audio_streams_info = self.probe_tool.get_audio_streams_info(original_info)
            audio_streams_len = len(audio_streams_info)
            self.key_msg.emit(f'        - 音频流：{audio_streams_len}条')
            if audio_streams_len:
                for x in range(audio_streams_len):
                    self.key_msg.emit(f'            - 第{x+1}条音频流：')
                    sample_rate = audio_streams_info[x].get('sample_rate')
                    self.key_msg.emit(f'                - 采样率：{sample_rate}Hz')
                    channels = audio_streams_info[x].get('channels')
                    self.key_msg.emit(f'                - 声道数：{channels}条')
                    bit_rate = audio_streams_info[x].get('bit_rate')
                    if bit_rate:
                        self.key_msg.emit(f'                - 比特率：{bit_rate}kbps')
            # 视频流信息
            video_streams_info = self.probe_tool.get_video_streams_info(original_info)
            video_streams_len = len(video_streams_info)
            if video_streams_len:
                self.key_msg.emit(f'        - 视频流：{video_streams_len}条')
                if video_streams_len:
                    for y in range(video_streams_len):
                        self.key_msg.emit(f'            - 第{y+1}条视频流：')
                        resolution = video_streams_info[y].get('resolution')
                        self.key_msg.emit(f'                - 分辨率：{resolution}')
        else:
            self.key_msg.emit(f'所选文件不支持解析！')

    def run(self) -> None:
        self.get_original_info()


class CutBySize(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    def __init__(self, cut_file_path, cut_size, cut_unit, cut_save_dir):
        super(CutBySize, self).__init__()
        self.cut_file_path = cut_file_path
        self.cut_size = cut_size
        self.cut_unit = cut_unit
        self.cut_save_dir = cut_save_dir

    def to_kb_num(self):
        """将大小的单位换算成KB"""
        if self.cut_unit == 'KB':
            return int(self.cut_size * 1024)
        elif self.cut_unit == 'MB':
            return int(self.cut_size * 1024 * 1024)
        elif self.cut_unit == 'GB':
            return int(self.cut_size * 1024 * 1024 * 1024)

    def cut_by_size(self):
        finally_size = self.to_kb_num()
        file_name = self.cut_file_path.split('/')[-1]
        save_file_name = f"{self.cut_save_dir}/切割音频_{self.cut_size}{self.cut_unit}_{file_name}"
        public_method.cut_by_size(self.cut_file_path, finally_size, save_file_name)
        self.msg.emit(f'音频切割完成，请到{self.cut_save_dir}目录查看！')

    def run(self) -> None:
        self.cut_by_size()


class CutByTime(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    def __init__(self, cut_file_path, start_time, end_time, save_dir):
        super(CutByTime, self).__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.save_dir = save_dir
        self.cut_file_path = cut_file_path

    def cut_by_time(self):
        """获取切割起始时间和截取时长"""
        public_method.cut_by_time(self.cut_file_path, self.save_dir, self.start_time, self.end_time)
        self.msg.emit(f'音频切割完成，请到{self.save_dir}目录查看！')

    def run(self) -> None:
        self.cut_by_time()


class CutPageFileInfo(QtCore.QThread):
    """"""
    msg_size = QtCore.pyqtSignal(str)
    msg_duration = QtCore.pyqtSignal(int)

    def __init__(self, file_path):
        super(CutPageFileInfo, self).__init__()
        self.ffmpeg_tool = public_method.FFmpegTool(file_path)

    def get_file_size_and_duration(self):
        """获取音频文件的时长和大小"""
        file_info = self.ffmpeg_tool.get_file_info()
        duration = self.ffmpeg_tool.get_duration(file_info)
        size = self.ffmpeg_tool.get_file_size_with_unit(file_info)
        self.msg_size.emit(size)
        self.msg_duration.emit(duration)

    def run(self) -> None:
        self.get_file_size_and_duration()


class StitchAudios(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    """合并多个音频文件"""
    def __init__(self, audio_paths, save_dir, save_format):
        super(StitchAudios, self).__init__()
        public_method.write_list_file(audio_paths)
        self.save_dir = save_dir
        self.save_format = save_format

    def stitch_audios(self):
        """"""
        public_method.stitch_audio(self.save_dir, self.save_format)
        self.msg.emit(f'<font color=blue>音频拼接成功，请进入{self.save_dir}目录查看！</font>')

    def run(self) -> None:
        self.stitch_audios()


class AudioResample(QtCore.QThread):
    """音频重采样"""
    msg = QtCore.pyqtSignal(str)

    def __init__(self, source_file_path, sample_rate, save_dir):
        super(AudioResample, self).__init__()
        self.source_file_path = source_file_path
        self.sample_rate = sample_rate
        self.save_dir = save_dir

    def audio_resample(self):
        file_name = self.source_file_path.split('/')[-1]
        save_path = f"{self.save_dir}/重采样_{self.sample_rate}Hz_{file_name}"
        public_method.resample(self.source_file_path, self.sample_rate, save_path)
        self.msg.emit(f'<font color=blue>音频重采样成功，请进入{self.save_dir}目录查看！</font>')

    def run(self) -> None:
        self.audio_resample()


class FormatConversion(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    def __init__(self, input_file_paths, save_dir):
        super(FormatConversion, self).__init__()
        self.input_file_paths = input_file_paths
        self.save_dir = save_dir

    def conversion(self):
        """"""
        for input_file_path in self.input_file_paths:
            file_current_format = input_file_path.split('.')[-1]
            file_full_name = input_file_path.split('/')[-1]
            file_name = file_full_name.split('.')[0]
            save_path = f"{self.save_dir}/16000Hz_{file_name}.wav"
            if file_current_format in conversion_general_format:
                command = f"ffmpeg.exe -y -i {input_file_path} -ar 16000 -ac 1 -map_channel 0.0.0 {save_path}"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            elif file_current_format.upper() == 'PCM':
                command = f"ffmpeg.exe -y -f s16le -ar 16000 -ac 1 -i {input_file_path} {save_path}"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            elif file_current_format in conversion_tencent_format:
                public_method.tencent2other(input_file_path, save_path, 16000)

    def run(self) -> None:
        self.conversion()
