#!/usr/bin/env python3
# 测试脚本，验证基础功能
import os
import json
from datetime import datetime

print("=== 系统测试 ===")
print(f"当前时间: {datetime.now()}")
print(f"当前目录: {os.getcwd()}")
print(f"目录内容: {os.listdir('.')}")

# 创建测试文件
test_data = {
    "test": "success",
    "timestamp": datetime.now().isoformat(),
    "message": "系统正常运行"
}

os.makedirs("output/test", exist_ok=True)
with open("output/test/test.json", "w") as f:
    json.dump(test_data, f, indent=2)

print("✅ 测试文件创建成功")
print("=== 测试完成 ===")
