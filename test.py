import pyang
import pyang.repository
import os

repo = pyang.repository()
print("当前搜索路径：", repo.get_paths())