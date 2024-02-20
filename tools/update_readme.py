from datetime import datetime
import re

""" 自动修改 README 文件中的最后修改时间 """

# 获取当前时间
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 读取 README.md 文件
with open("README.md", "r", encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式替换最后修改时间
# new_content = re.sub(r"Last Modified: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", f"Last Updated: {current_time}", content)
new_content = re.sub(r"\s*\|\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s*\|\s*", f" | {current_time} | ", content)



# 将新内容写回 README.md 文件
with open("README.md", "w", encoding='utf-8') as f:
    f.write(new_content)
