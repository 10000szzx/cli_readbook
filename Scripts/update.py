import argparse
import json
import pickle
import re
from datetime import datetime
from typing import Any, Union

import pandas as pd


def get_book_pic_path(config_file_path):
    """
    从指定的config.json文件中读取BOOK_PIC_PATH属性的值。
    config_file_path -- config.json文件的路径
    BOOK_PIC_PATH属性的值，如果找不到该属性或读取失败，则返回None
    """
    try:
        with open(config_file_path, 'r', encoding="utf-8") as file:
            config = json.load(file)
            return config.get('BOOK_PIC_PATH')
    except json.JSONDecodeError:
        print("Error: JSON文件解析失败。")
    except FileNotFoundError:
        print(f"Error: 无法找到文件 {config_file_path}。")
    except Exception as e:
        print(f"Error: {e}")

    return None

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
            r'第[0-9零一二三四五六七八九十百千万]+卷.{0,100}第[0-9零一二三四五六七八九十百千万]+章.{0,100}\n'
            # r'第[0-9零一二三四五六七八九十百千万]+卷\s+.*?\s+第[0-9零一二三四五六七八九十百千万]+章\s\n'
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


if __name__ == "__main__":
    BOOK_PIC_PATH = get_book_pic_path("C:/Users/despa/readbook/config.json")

    parser = argparse.ArgumentParser(description="Book Reader")
    parser.add_argument('update', type=int, default=None, help="Bookmark to update")

    args = parser.parse_args()

    book = loadPic(BOOK_PIC_PATH)

    if args.update is None:
        print(f"当前书籍位置：{BOOK_PIC_PATH}\n"
              f"当前书签位置：{book.CPosition}\n"
              f"若要更新书签，请重新执行 update 并输入待更新参数")
    else:
        try:
            bookmark = int(args.update)
            book.update(bookmark)
            savePic(book, BOOK_PIC_PATH)
        except ValueError:
            print("参数输入错误：可省略参数查看章节列表")