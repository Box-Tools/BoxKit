import os.path
dll_name = "MyCDLL.dll"
dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name

print(dllabspath)
