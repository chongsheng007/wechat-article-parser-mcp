
#!/usr/bin/env python3
"""
检查 Cursor 数据库中的聊天记录
"""

import sqlite3
import json
from pathlib import Path

def check_chat_in_db():
    db_path = Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"
    
    if not db_path.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 检查 ItemTable
    print("=" * 60)
    print("检查 ItemTable 表")
    print("=" * 60)
    try:
        cursor.execute("SELECT key, value FROM ItemTable LIMIT 20;")
        rows = cursor.fetchall()
        print(f"找到 {len(rows)} 条记录（前20条）:\n")
        
        for key, value in rows:
            if isinstance(value, bytes):
                try:
                    value_str = value.decode('utf-8')
                    if len(value_str) > 200:
                        value_str = value_str[:200] + "..."
                    print(f"Key: {key[:80]}...")
                    print(f"Value: {value_str[:200]}...")
                except:
                    print(f"Key: {key[:80]}...")
                    print(f"Value: <binary data, {len(value)} bytes>")
            else:
                print(f"Key: {key[:80]}...")
                print(f"Value: {str(value)[:200]}...")
            print("-" * 60)
    except Exception as e:
        print(f"❌ 查询 ItemTable 时出错: {e}")
    
    # 检查 cursorDiskKV
    print("\n" + "=" * 60)
    print("检查 cursorDiskKV 表")
    print("=" * 60)
    try:
        cursor.execute("SELECT key, value FROM cursorDiskKV LIMIT 20;")
        rows = cursor.fetchall()
        print(f"找到 {len(rows)} 条记录（前20条）:\n")
        
        for key, value in rows:
            if isinstance(value, bytes):
                try:
                    value_str = value.decode('utf-8')
                    if 'chat' in value_str.lower() or 'conversation' in value_str.lower():
                        print(f"🔍 找到可能的聊天记录！")
                        print(f"Key: {key}")
                        print(f"Value length: {len(value_str)}")
                        # 尝试解析 JSON
                        try:
                            data = json.loads(value_str)
                            print(f"✅ 是 JSON 格式")
                            print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                        except:
                            print(f"Value preview: {value_str[:500]}...")
                    elif len(value_str) > 200:
                        value_str = value_str[:200] + "..."
                        print(f"Key: {key[:80]}...")
                        print(f"Value: {value_str[:200]}...")
                except:
                    print(f"Key: {key[:80]}...")
                    print(f"Value: <binary data, {len(value)} bytes>")
            else:
                print(f"Key: {key[:80]}...")
                print(f"Value: {str(value)[:200]}...")
            print("-" * 60)
    except Exception as e:
        print(f"❌ 查询 cursorDiskKV 时出错: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_chat_in_db()


