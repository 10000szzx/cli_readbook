import argparse
import chardet
import pickle
import re
from datetime import datetime
from typing import Any, Union

import h5py
import pandas as pd


def CTime(name=True):
    if name:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def savePic(obj: Any, filepath: str = f"./val_{CTime()}.pickle"):
    """
    将Python对象序列化并保存为Pickle文件。
    :param obj: 要序列化的Python对象
    :param filepath: 保存Pickle文件的路径
    """
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def loadPic(filepath: str) -> Any:
    """
    从Pickle文件中加载Python对象。
    :param filepath: 要加载的Pickle文件路径
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def detect_encoding(file_path: str) -> str:
    """
    返回目标文件的编码格式
    :param file_path: 目标文本文件路径
    :return: 目标文件的可能编码格式（使用 chatdet 库进行识别，可能会出错）
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']

    if confidence < 0.5:  # 设置一个容错阈值
        # 当置信度较低时，返回一个默认的编码格式，比如UTF-8
        print(f"Low confidence ({confidence}), using default encoding: UTF-8")
        return "UTF-8"

    # 常见编码格式的容错处理
    if encoding in ["ISO-8859-1", "ASCII"]:
        return "UTF-8"
    elif encoding in ["EUC-TW", "GB18030", "GBK", "GB2312"]:
        return "GB18030"
    elif encoding in ["UTF-16", "UTF-32"]:
        return "UTF-8"

    # 其他情况，返回检测到的编码
    return encoding


def splitChapters(text: str, chapter_pattern=None, savename=None) -> pd.DataFrame:
    """
    从文本内容解析章节，按章节输出二维列表，包括章节名与章节正文
    :param text: 待解析文本
    :param chapter_pattern: 章节名称的匹配通配符
    :param savename: 是否保存，默认为空不保存，若保存则使用该变量传入存储路径
    :return:
    """
    if not chapter_pattern:
        chapter_pattern = re.compile(
            r'第[0-9]+章.{0,100}\n'

            # r'第[0-9零一二三四五六七八九十百千万]+卷.{0,100}第[0-9零一二三四五六七八九十百千万]+章.{0,100}\n'
        )
    chapters = list(chapter_pattern.finditer(text))

    res = pd.DataFrame(columns=["CHName", "CHText"])

    for idx in range(len(chapters)):
        # 如果第一章，则加一个介绍
        # 如果不是第一章，直接

        if idx > 0:
            start = chapters[idx].end()
        else:
            res.loc[len(res), :] = ["书籍介绍：", text[0:chapters[idx].start()].strip()]
            start = chapters[idx].end()

        if idx != len(chapters) - 1:
            end = chapters[idx + 1].start()
        else:
            end = -1
        chapter_text = text[start:end].strip()
        chapter_name = text[chapters[idx].start():chapters[idx].end()].strip()

        res.loc[len(res), :] = [chapter_name, chapter_text]
    if savename:
        savePic(res, savename)
    return res


def save2hdf5(chapters, hdf5path=f"./chapters_{CTime()}.h5"):
    """
    将 splitChapters 函数的输出存储到 hdf5 文件中
    【弃用】：插入后会乱序，不好调用
    :param chapters: splitChapters 函数的输出，包含章节名与章节正文
    :param hdf5path: 存储的文件路径
    :return:
    """
    with h5py.File(hdf5path, 'w') as h5f:
        for chapter_name, chapter_text in chapters:
            h5f.create_dataset(chapter_name, data=chapter_text)


def get_chapter(chapter_idx: int, hdf5_path):
    """
    根据索引调取 hdf5 文件中的章节
    【弃用】：插入后乱序，不好调用相应的章节
    :param chapter_idx: 章节索引
    :param hdf5_path: hdf5 文件路径
    :return:
    """
    with h5py.File(hdf5_path, 'r') as h5f:
        chapter_name = list(h5f.keys())[chapter_idx]
        if chapter_name in h5f:
            return chapter_name, h5f[chapter_name][()].decode('utf-8')
        else:
            return None, None


class BooK:
    def __init__(self, chapters: pd.DataFrame):
        self._chapters = chapters
        self.CPosition = 0

    def getChapterName(self):
        """返回章节标题的列表"""
        return self._chapters['CHName']

    def printChapterName(self):
        """打印章节标题的列表"""
        print(self._chapters['CHName'])

    def getText(self, index_or_name: Union[int, str]):
        """根据章节索引获取章节内容"""
        if isinstance(index_or_name, int):
            if 0 <= index_or_name < len(self._chapters):
                self.CPosition = index_or_name
                return self._chapters.iloc[index_or_name]['CHText']
            else:
                return "章节索引超出范围"
        elif isinstance(index_or_name, str):
            if index_or_name in self._chapters["CHName"]:
                return self._chapters[self._chapters["CHName"] == index_or_name]['CHText']
            else:
                return "不存在指定章节"

    def read(self, index_or_name: Union[int, str]):
        """根据章节索引获取章节内容"""
        if isinstance(index_or_name, int):
            if 0 <= index_or_name < len(self._chapters):
                self.CPosition = index_or_name
                print(self._chapters.iloc[index_or_name]['CHName'])
                print(self._chapters.iloc[index_or_name]['CHText'])
            else:
                print("章节索引超出范围")
        elif isinstance(index_or_name, str):
            if index_or_name in self._chapters["CHName"]:
                print(index_or_name)
                print(self._chapters[self._chapters["CHName"] == index_or_name]['CHText'])
            else:
                print("不存在指定章节")

    def update(self, new_position):
        """更新当前阅读位置的索引"""
        if 0 <= new_position < len(self._chapters):
            self.CPosition = new_position
        else:
            self.CPosition = len(self._chapters) - 1


if __name__ == '__main1__':
    # 读取文本文件

    now_time = CTime()

    with open('星戒-空神.txt', 'r', encoding='ANSI', errors='ignore') as file:
        text = file.read()
    
    chapters = splitChapters(text, savename=f"星戒_空神_dataframe_{now_time}.pickle")

    # 保存为一个类的变量
    data = loadPic(f"星戒_空神_dataframe_{now_time}.pickle")
    XJ = BooK(data)
    # XJ.printChapterName()
    savePic(XJ, f"星戒_空神_class_last_{now_time}.pickle")

    # 看文本与更新文件
    filepath = "星戒_空神_class_last_{now_time}.pickle"
    data = loadPic(filepath)
    data.printChapterName()
    print("当前书签位置：", data.CPosition)

    # 阅读某一章
    data.read(100)

    # 更新书签位置
    data.update(100)
    savePic(data, filepath)


if __name__ == '__main__':
    # 读取文本文件

    now_time = CTime()

    with open('../洪荒少年猎艳录_天地23.txt', 'r', encoding='ANSI', errors='ignore') as file:
        text = file.read()
    
    chapters = splitChapters(text, savename=f"天地23_dataframe_{now_time}.pickle")

    # 保存为一个类的变量
    data = loadPic(f"天地23_dataframe_{now_time}.pickle")
    XJ = BooK(data)
    # XJ.printChapterName()
    savePic(XJ, f"天地23_class_last_{now_time}.pickle")

    # # 看文本与更新文件
    # filepath = "天地23_class_last_{now_time}.pickle"
    # data = loadPic(filepath)
    # data.printChapterName()
    # print("当前书签位置：", data.CPosition)

    # # 阅读某一章
    # data.read(100)

    # # 更新书签位置
    # data.update(100)
    # savePic(data, filepath)
