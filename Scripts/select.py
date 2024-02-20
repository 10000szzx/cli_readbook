import argparse
import json
import os

import pandas as pd
pd.options.display.max_colwidth = None

# BOOKSHELF = pd.DataFrame(
#     [
#         (0, "C:/Users/despa/readbook/book_pic/星戒_空神_class_last_20240117_083312.pickle"),
#         (1, "C:/Users/despa/readbook/book_pic/天地23_class_last_20240118_150944.pickle"),
#     ],
#     columns=["idx", "path"]
# )

BOOK_PIC = "C:/Users/despa/readbook/book_pic/"
BOOKSHELF = pd.DataFrame(os.listdir(BOOK_PIC), columns=["path"])
BOOKSHELF["path"] = BOOK_PIC + BOOKSHELF["path"]


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


def update_json_value(json_file_path, key, new_value):
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)

        # 更新指定键的值
        if key in data:
            data[key] = new_value
            print(new_value)
            # 写回JSON文件
            with open(json_file_path, 'w', encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        else:
            print(f"键 '{key}' 不存在于JSON文件中")
    except FileNotFoundError:
        print(f"文件 '{json_file_path}' 不存在")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    BOOK_PIC_PATH = get_book_pic_path("C:/Users/despa/readbook/config.json")
    parser = argparse.ArgumentParser(description="Book Update")
    parser.add_argument('select', nargs='?', default=None, help="Book index to update.")

    args = parser.parse_args()

    if args.select is None:
        print(BOOK_PIC_PATH)
        print(BOOKSHELF)
    else:
        if int(args.select) >= len(BOOKSHELF):
            raise ValueError("参数输入错误：可省略参数查看书目列表")
        try:
            value = BOOKSHELF.loc[int(args.select), "path"]
            update_json_value(
                "C:/Users/despa/readbook/config.json",
                "BOOK_PIC_PATH",
                f"{value}"
            )
        except ValueError:
            print("参数输入错误：可省略参数查看书目列表")
