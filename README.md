| Author | Last Updated | Version |
| :----: | :-----------------: | :-----: |
| wx | 2024-02-21 00:08:03 | 1.1.alpha.1 |

## 在命令行使用命令进行编辑的阅读文本小说~~

> 使用简单的命令在命令行实现阅读文本小说的功能。比如：
>
> - 使用 `read n` 命令查看第 n 章节



### 制作一个小说的 pickle 文件

> 这个文件包含了一本小说的封装类，这个类包含了小说的所有章节名与章节内容，这些不可变；还包含了一个章节的整数索引，作为书签使用。

#### 解析 txt 文本，得到“结构化”的小说

```python
now_time = CTime()

# 通过txt文本的路径解析小说，注意修改编码格式
# 对于不同的txt文本，还需要修改不同的章节名通配符，在splitChapters函数中容易找到
with open('星戒-空神.txt', 'r', encoding='ANSI', errors='ignore') as file:
    text = file.read()
chapters = splitChapters(text, savename=f"星戒_空神_dataframe_{now_time}.pickle")
```

#### 实例化小说类

```python
data = loadPic(f"星戒_空神_dataframe_{now_time}.pickle")
XJ = BooK(data)
# XJ.printChapterName() # 打印章节列表
savePic(XJ, f"星戒_空神_class_last_{now_time}.pickle")
```

#### 小说类的初步使用

```python
# 读取pic文件
filepath = "星戒_空神_class_last_{now_time}.pickle"
data = loadPic(filepath)

# 打印章节列表
data.printChapterName()

# 书签位置
print("当前书签位置：", data.CPosition)

# 阅读某一章
data.read(100)

# 更新书签位置
data.update(100)
savePic(data, filepath)
```

### 通过脚本实现命令行调用

> 具体的脚本在`./Scripts` 中，将dat脚本放于全局环境的路径下即可，可能需要修改其中的路径。
> 此处只说明调用。

1. 查看书架：`ect` （将打印书架中的所有书籍路径与对应的索引）
2. 修改书籍：`ect index` （其中 `index` 是一个整数参数，单独 `ect` 命令中的对应索引，用于设定书籍）
3. 不记得书签位置，获取书签前后的章节名列表：`read` （将打印书签前后的部分章节名）
4. 阅读某一章：`read index` （其中 `index` 是一个整数参数，用于选择章节）
5. 更新书签：`update index` （其中 `index` 是一个整数参数，用于设置章节位置）

```shell
# 命令行任意位置输入 read ，打印部分章节名
D:\>read
        95: 第一卷 地球卷 第九十五章 实力的划分！
        96: 第一卷 地球卷 第九十六章 病毒样本！
        97: 第一卷 地球卷 第九十七章 生化克星！
        98: 第一卷 地球卷 第九十八章 丧尸解决！
        99: 第一卷 地球卷 第九十九章 见家长！
------> 100: 第一卷 地球卷 第一百章 星形钥匙！ <------ (书签.)
        101: 第一卷 地球卷 第一百零一章 龙凌天！
        102: 第一卷 地球卷 第一百零二章 魔幻世界！
        103: 第一卷 地球卷 第一百零三章 好消息连连！
        104: 第一卷 地球卷 第一百零四章 天香城！
        105: 第一卷 地球卷 第一百零五章 决斗（上）
        106: 第一卷 地球卷 第一百零六章 决斗！（中）
        107: 第一卷 地球卷 第一百零七章 决斗！（下）
        108: 第一卷 地球卷 第一百零八章 第一次死亡！
        109: 第一卷 地球卷 第一百零九章 天阴神脉！
        110: 第一卷 地球卷 第一百一十章 吸血鬼的报复！
        111: 第一卷 地球卷 第一百一十一章 巨龙！
        112: 第一卷 地球卷 第一百一十二章 巨额界力！
        113: 第一卷 地球卷 第一百一十三章 没金币用的日子！
        114: 第一卷 地球卷 第一百一十四章 认了个妹妹！
        115: 第一卷 地球卷 第一百一十五章 焰火！
```

