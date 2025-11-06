#!/usr/bin/env python3
"""
查看导出的聊天记录中的实际对话内容
"""

import json
import re
from pathlib import Path

def extract_text_from_rich_text(rich_text_str):
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
            
            elif isinstance(node, list):
                for item in node:
                    text_parts.extend(extract_text_from_node(item))
            
            return text_parts
        
        # 提取所有文本
        texts = extract_text_from_node(rich_text)
        return ' '.join(texts)
    except Exception as e:
        return str(rich_text_str)

def view_chat_content():
    """查看聊天记录中的实际内容"""
    export_file = Path('cursor_chat_export_20251105_120818.md')
    
    if not export_file.exists():
        print(f"❌ 未找到导出文件: {export_file}")
        return
    
    print("=" * 60)
    print("Cursor 聊天记录内容查看器")
    print("=" * 60)
    print()
    
    content = export_file.read_text(encoding='utf-8')
    
    # 分割成各个记录
    sections = content.split('## 聊天记录 #')
    
    chat_messages = []
    
    for section in sections[1:]:  # 跳过第一个空部分
        # 查找 composerData
        if 'composerData' in section:
            # 提取键名
            key_match = re.search(r'\*\*键\*\*: `([^`]+)`', section)
            if not key_match:
                continue
            
            key = key_match.group(1)
            
            # 提取 JSON 数据
            json_match = re.search(r'```json\n(.*?)\n```', section, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    
                    # 查找 richText
                    if 'richText' in data:
                        text = extract_text_from_rich_text(data['richText'])
                        if text and len(text.strip()) > 10:  # 只显示有实际内容的
                            chat_messages.append({
                                'key': key,
                                'text': text,
                                'type': 'user_message'
                            })
                
                except json.JSONDecodeError:
                    # 尝试查找其他格式
                    pass
    
    print(f"✅ 找到 {len(chat_messages)} 条包含实际聊天内容的记录\n")
    
    if not chat_messages:
        print("⚠️  未找到可读的聊天消息内容")
        print("\n💡 提示：聊天消息可能存储在其他格式中")
        return
    
    # 显示前10条消息
    print("=" * 60)
    print("实际聊天内容预览（前10条）")
    print("=" * 60)
    print()
    
    for i, msg in enumerate(chat_messages[:10], 1):
        print(f"【消息 #{i}】")
        print(f"来源: {msg['key']}")
        print(f"内容: {msg['text'][:200]}..." if len(msg['text']) > 200 else f"内容: {msg['text']}")
        print("-" * 60)
        print()
    
    # 保存所有消息到单独文件
    output_file = Path('cursor_chat_messages_only.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Cursor 聊天消息内容\n\n")
        f.write(f"共提取 {len(chat_messages)} 条消息\n\n")
        f.write("---\n\n")
        
        for i, msg in enumerate(chat_messages, 1):
            f.write(f"## 消息 #{i}\n\n")
            f.write(f"**来源**: `{msg['key']}`\n\n")
            f.write(f"**内容**:\n\n{msg['text']}\n\n")
            f.write("---\n\n")
    
    print(f"✅ 所有聊天消息已保存到: {output_file.absolute()}")
    print(f"📄 共 {len(chat_messages)} 条消息")

if __name__ == "__main__":
    view_chat_content()


