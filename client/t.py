import re

file_path = "/Users/u03013112/Library/Application Support/Steam/steamapps/common/Inscryption/Inscryption.app/SaveFile.gwsave"

try:
    with open(file_path, "r") as file:
        content = file.read()

        # 使用正则表达式查找 "playTime": 数字 的模式
        playtime_pattern = re.compile(r'"playTime":\s*([\d.]+)')
        match = playtime_pattern.search(content)

        if match:
            playtime = float(match.group(1))
            print(f"playTime: {playtime}")
        else:
            print("playTime not found in the file.")
except FileNotFoundError:
    print(f"File not found: {file_path}")
