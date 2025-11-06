#!/usr/bin/env python3
"""
从 Cursor 数据库中提取聊天记录并导出为 Markdown
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def extract_chat_from_db():
    """从数据库提取聊天记录"""
    db_path = Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"
    
    if not db_path.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        return None
    
    print(f"✅ 找到数据库: {db_path}\n")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    all_chats = []
    
    # 检查 ItemTable 中的聊天相关数据
    print("=" * 60)
    print("搜索 ItemTable 中的聊天记录...")
    print("=" * 60)
    
    try:
        cursor.execute("SELECT key, value FROM ItemTable;")
        rows = cursor.fetchall()
        
        for key, value in rows:
            if isinstance(value, str):
                # 查找包含聊天相关关键词的键
                if any(keyword in key.lower() for keyword in ['chat', 'conversation', 'message', 'aichat', 'composer']):
                    try:
                        # 尝试解析 JSON
                        data = json.loads(value) if value.startswith('{') or value.startswith('[') else value
                        if isinstance(data, dict) or isinstance(data, list):
                            all_chats.append({
                                'key': key,
                                'data': data,
                                'type': 'ItemTable'
                            })
                            print(f"✅ 找到聊天数据: {key[:80]}...")
                    except:
                        if len(value) > 100:  # 可能是聊天内容
                            all_chats.append({
                                'key': key,
                                'data': value,
                                'type': 'ItemTable'
                            })
                            print(f"✅ 找到可能的聊天内容: {key[:80]}...")
    except Exception as e:
        print(f"❌ 查询 ItemTable 时出错: {e}")
    
    # 检查 cursorDiskKV 表
    print("\n" + "=" * 60)
    print("搜索 cursorDiskKV 中的聊天记录...")
    print("=" * 60)
    
    try:
        cursor.execute("SELECT key, value FROM cursorDiskKV WHERE value IS NOT NULL;")
        rows = cursor.fetchall()
        
        for key, value in rows:
            if value is None:
                continue
                
            if isinstance(value, bytes):
                try:
                    value_str = value.decode('utf-8')
                    # 查找包含聊天相关内容的键
                    if any(keyword in key.lower() for keyword in ['chat', 'conversation', 'message', 'composer', 'bubble']):
                        try:
                            data = json.loads(value_str)
                            all_chats.append({
                                'key': key,
                                'data': data,
                                'type': 'cursorDiskKV'
                            })
                            print(f"✅ 找到聊天数据: {key[:80]}...")
                        except:
                            if len(value_str) > 200:  # 可能是聊天内容
                                all_chats.append({
                                    'key': key,
                                    'data': value_str,
                                    'type': 'cursorDiskKV'
                                })
                                print(f"✅ 找到可能的聊天内容: {key[:80]}...")
                except:
                    pass
            elif isinstance(value, str):
                if any(keyword in key.lower() for keyword in ['chat', 'conversation', 'message', 'composer']):
                    try:
                        data = json.loads(value) if value.startswith('{') or value.startswith('[') else value
                        all_chats.append({
                            'key': key,
                            'data': data,
                            'type': 'cursorDiskKV'
                        })
                        print(f"✅ 找到聊天数据: {key[:80]}...")
                    except:
                        pass
    except Exception as e:
        print(f"❌ 查询 cursorDiskKV 时出错: {e}")
    
    conn.close()
    
    return all_chats

def extract_text_from_rich_text(rich_text_str: str) -> str:
    """从 richText JSON 字符串中提取纯文本"""
    try:
        if isinstance(rich_text_str, str):
            rich_text = json.loads(rich_text_str)
        else:
            rich_text = rich_text_str
        
        def extract_text_from_node(node):
            """递归提取文本"""
            text_parts = []
            
            if isinstance(node, dict):
                # 如果有 text 字段
                if 'text' in node:
                    text_parts.append(node['text'])
                
                # 如果有 children 字段，递归处理
                if 'children' in node:
                    for child in node['children']:
                        text_parts.extend(extract_text_from_node(child))
                
                # 如果是数组，遍历处理
                if isinstance(node.get('children'), list):
                    for child in node['children']:
                        text_parts.extend(extract_text_from_node(child))
            
            elif isinstance(node, list):
                for item in node:
                    text_parts.extend(extract_text_from_node(item))
            
            return text_parts
        
        # 提取所有文本
        texts = extract_text_from_node(rich_text)
        return '\n'.join(texts)
    except Exception as e:
        return str(rich_text_str)

def format_chat_to_markdown(chats: List[Dict[str, Any]]) -> str:
    """将聊天记录格式化为 Markdown"""
    md_content = []
    md_content.append("# Cursor 聊天记录导出\n\n")
    md_content.append(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    md_content.append("---\n\n")
    
    for idx, chat in enumerate(chats, 1):
        md_content.append(f"## 聊天记录 #{idx}\n\n")
        md_content.append(f"**来源**: {chat['type']}\n\n")
        md_content.append(f"**键**: `{chat['key']}`\n\n")
        
        data = chat['data']
        
        # 如果是字典，尝试提取有用信息
        if isinstance(data, dict):
            # 查找 richText 字段
            if 'richText' in data:
                text = extract_text_from_rich_text(data['richText'])
                md_content.append("**内容**:\n\n")
                md_content.append(f"{text}\n\n")
            # 查找其他可能的文本字段
            elif 'text' in data:
                md_content.append("**内容**:\n\n")
                md_content.append(f"{data['text']}\n\n")
            elif 'message' in data:
                md_content.append("**内容**:\n\n")
                md_content.append(f"{data['message']}\n\n")
            else:
                # 显示整个 JSON（格式化）
                md_content.append("**数据**:\n\n")
                md_content.append("```json\n")
                md_content.append(json.dumps(data, indent=2, ensure_ascii=False))
                md_content.append("\n```\n\n")
        # 如果是字符串
        elif isinstance(data, str):
            # 尝试解析为 JSON
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict) and 'richText' in parsed:
                    text = extract_text_from_rich_text(parsed['richText'])
                    md_content.append("**内容**:\n\n")
                    md_content.append(f"{text}\n\n")
                else:
                    md_content.append("**内容**:\n\n")
                    md_content.append(f"{data}\n\n")
            except:
                md_content.append("**内容**:\n\n")
                md_content.append(f"{data}\n\n")
        else:
            md_content.append("**数据**:\n\n")
            md_content.append(f"{str(data)}\n\n")
        
        md_content.append("---\n\n")
    
    return ''.join(md_content)

def main():
    print("=" * 60)
    print("Cursor 聊天记录提取工具")
    print("=" * 60)
    print()
    
    # 提取聊天记录
    chats = extract_chat_from_db()
    
    if not chats:
        print("\n❌ 未找到聊天记录")
        print("\n💡 提示:")
        print("1. 聊天记录可能存储在其他位置")
        print("2. 可以尝试在 Cursor 中手动复制聊天内容")
        print("3. 或者检查 Cursor 的 workspaceStorage 目录")
        return
    
    print(f"\n✅ 找到 {len(chats)} 条聊天相关的数据\n")
    
    # 格式化为 Markdown
    md_content = format_chat_to_markdown(chats)
    
    # 保存到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(f"cursor_chat_export_{timestamp}.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ 聊天记录已导出到: {output_file.absolute()}")
    print(f"📄 共提取 {len(chats)} 条记录")
    
    # 显示预览
    print("\n" + "=" * 60)
    print("预览（前 500 字符）:")
    print("=" * 60)
    print(md_content[:500] + "..." if len(md_content) > 500 else md_content)

if __name__ == "__main__":
    main()


