#!/usr/bin/env python3
"""
Cursor 聊天记录导出工具

用于导出 Cursor IDE 的聊天历史记录
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

def find_cursor_data_dir():
    """查找 Cursor 数据目录"""
    home = Path.home()
    cursor_dir = home / "Library/Application Support/Cursor"
    
    if cursor_dir.exists():
        return cursor_dir
    return None

def export_from_state_db(cursor_dir):
    """从 state.vscdb 数据库导出聊天记录"""
    state_db = cursor_dir / "User/globalStorage/state.vscdb"
    
    if not state_db.exists():
        print(f"❌ 未找到 state.vscdb: {state_db}")
        return None
    
    try:
        conn = sqlite3.connect(str(state_db))
        cursor = conn.cursor()
        
        # 查询所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 数据库中的表: {[t[0] for t in tables]}")
        
        # 尝试查找聊天相关的表
        for table in tables:
            table_name = table[0]
            if 'chat' in table_name.lower() or 'conversation' in table_name.lower():
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
                rows = cursor.fetchall()
                print(f"\n📝 表 {table_name} 的前10条记录:")
                for row in rows:
                    print(f"  {row}")
        
        conn.close()
        return None
    except Exception as e:
        print(f"❌ 读取数据库时出错: {e}")
        return None

def export_from_storage_json(cursor_dir):
    """从 storage.json 导出数据"""
    storage_file = cursor_dir / "User/globalStorage/storage.json"
    
    if not storage_file.exists():
        print(f"❌ 未找到 storage.json: {storage_file}")
        return None
    
    try:
        with open(storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 查找聊天相关的键
        chat_keys = [k for k in data.keys() if 'chat' in k.lower() or 'conversation' in k.lower()]
        
        if chat_keys:
            print(f"✅ 找到聊天相关的键: {chat_keys}")
            return data
        else:
            print("⚠️  storage.json 中未找到聊天相关的数据")
            return None
    except Exception as e:
        print(f"❌ 读取 storage.json 时出错: {e}")
        return None

def export_chat_to_markdown(chat_data, output_file):
    """将聊天数据导出为 Markdown 格式"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_file) if output_file else Path(f"cursor_chat_export_{timestamp}.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Cursor 聊天记录导出\n\n")
        f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        # 这里需要根据实际的数据结构来格式化
        f.write(json.dumps(chat_data, indent=2, ensure_ascii=False))
    
    print(f"✅ 聊天记录已导出到: {output_path}")
    return output_path

def main():
    print("=" * 60)
    print("Cursor 聊天记录导出工具")
    print("=" * 60)
    
    cursor_dir = find_cursor_data_dir()
    if not cursor_dir:
        print("❌ 未找到 Cursor 数据目录")
        return
    
    print(f"✅ 找到 Cursor 数据目录: {cursor_dir}\n")
    
    # 尝试从 storage.json 导出
    print("📂 尝试从 storage.json 读取...")
    storage_data = export_from_storage_json(cursor_dir)
    
    # 尝试从数据库导出
    print("\n📂 尝试从 state.vscdb 读取...")
    db_data = export_from_state_db(cursor_dir)
    
    print("\n" + "=" * 60)
    print("💡 提示:")
    print("=" * 60)
    print("1. 如果上述方法无法找到聊天记录，可以尝试:")
    print("   - 在 Cursor 中手动复制聊天内容")
    print("   - 检查 Cursor 设置中是否有导出选项")
    print("   - 查看 Cursor 的更新日志，了解新版本的导出功能位置")
    print("\n2. 调整聊天面板位置:")
    print("   - 拖拽聊天面板标题栏到右侧")
    print("   - 右键点击标题栏，选择 '移动到右侧'")
    print("   - 快捷键 Cmd+L 打开/关闭面板")

if __name__ == "__main__":
    main()


