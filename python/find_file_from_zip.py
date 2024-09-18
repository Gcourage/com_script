import zipfile
import re

zip_file_path = "/Users/hubinbin/codes/github/burst.zip"

editor_re = re.compile(r"/Unity.Burst.CodeGen/")

with zipfile.ZipFile(zip_file_path, 'r') as f_zip:
    for info in f_zip.infolist():
        find_str = editor_re.findall(info.filename)
        if find_str:
            print(find_str)
            exit(1)