#!/usr/bin/env python3
"""
标准文件创建工具
确保文件可以在 Cursor 中正常打开
命名规范：小写英文字母 + 中文简体
"""

import os
import sys
from pathlib import Path


def create_file_safely(file_path, content, encoding='utf-8'):
    """
    安全创建文件，确保可以在 Cursor 中正常打开
    
    参数:
        file_path: 文件路径（字符串）
        content: 文件内容（字符串）
        encoding: 编码格式（默认 UTF-8）
    """
    # 确保路径是 Path 对象
    file_path = Path(file_path)
    
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 删除已存在的文件（如果有）
    if file_path.exists():
        # 清理扩展属性
        try:
            import subprocess
            subprocess.run(['xattr', '-c', str(file_path)], 
                         capture_output=True, check=False)
        except:
            pass
        os.remove(file_path)
    
    # 创建文件（使用二进制模式写入，确保编码正确）
    with open(file_path, 'wb') as f:
        # 转换为字节，确保使用 UTF-8 编码
        content_bytes = content.encode(encoding)
        f.write(content_bytes)
    
    # 设置文件权限
    os.chmod(file_path, 0o644)
    
    # 清理扩展属性（防止 macOS 扩展属性导致问题）
    try:
        import subprocess
        subprocess.run(['xattr', '-c', str(file_path)], 
                      capture_output=True, check=False)
    except:
        pass
    
    # 触发文件系统事件，确保 Cursor 能正确索引文件
    # 方法：通过 touch 更新文件时间戳，触发文件系统事件
    try:
        os.utime(file_path, None)
        # 或者重命名再改回来（更可靠，但可能影响其他工具）
        # temp_name = str(file_path) + '.tmp'
        # file_path.rename(temp_name)
        # Path(temp_name).rename(file_path)
    except:
        pass
    
    print(f"✅ 文件已创建: {file_path}")
    return file_path


def validate_filename(filename):
    """
    验证文件名是否符合规范：小写英文字母 + 中文简体
    
    参数:
        filename: 文件名（不含路径）
    
    返回:
        bool: 是否符合规范
    """
    # 允许的字符：小写字母、数字、中文、连字符、下划线、点
    import re
    pattern = r'^[a-z0-9\u4e00-\u9fa5._-]+$'
    return bool(re.match(pattern, filename))


def normalize_filename(filename):
    """
    规范化文件名：转换为小写 + 保留中文
    
    参数:
        filename: 原始文件名
    
    返回:
        str: 规范化后的文件名
    """
    # 提取文件名和扩展名
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        # 只将非中文部分转为小写
        normalized_name = ''.join(
            c.lower() if ord(c) < 128 else c 
            for c in name
        )
        return f"{normalized_name}.{ext.lower()}"
    else:
        # 没有扩展名，只转换非中文部分
        return ''.join(
            c.lower() if ord(c) < 128 else c 
            for c in filename
        )


if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        content = sys.argv[2] if len(sys.argv) > 2 else "# 测试文件\n\n这是一个测试文件。"
        create_file_safely(file_path, content)
    else:
        print("用法: python create_file.py <文件路径> [内容]")



