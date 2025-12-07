import re
import csv
import datetime
import email
from io import StringIO
from bs4 import BeautifulSoup
from email.policy import default

# --- 配置 ---
# 根据您的账单周期 (2025/11/06-2025/12/05) 设置年份
STATEMENT_YEAR = "2025"
INPUT_FILENAME = "8_transaction.eml"
OUTPUT_FILENAME = "8_transaction.csv"


def extract_html_from_eml(eml_path):
    """从 EML 文件中找到并提取主要的 HTML 邮件体内容。"""
    try:
        with open(eml_path, 'rb') as f:
            # 使用 email.parser 解析 EML 文件
            msg = email.message_from_bytes(f.read(), policy=default)
    except FileNotFoundError:
        print(f"❌ 错误：文件 '{eml_path}' 未找到。请确保文件路径正确。")
        return None
    except Exception as e:
        print(f"❌ 解析 EML 文件时发生错误: {e}")
        return None

    # 遍历邮件的所有部分（处理多部分 MIME 邮件）
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get('Content-Disposition'))

            # 寻找主要的 HTML 内容部分
            if ctype == 'text/html' and 'attachment' not in cdisp:
                # 尝试解码内容
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    return part.get_payload(decode=True).decode(charset, errors='replace')
                except Exception as e:
                    print(f"解码 HTML 内容失败: {e}")
                    # 如果解码失败，尝试默认的 UTF-8
                    return part.get_payload(decode=True).decode('utf-8', errors='replace')
    
    # 如果邮件不是多部分（但通常 e-bills 是多部分的）
    elif msg.get_content_type() == 'text/html':
        charset = msg.get_content_charset() or 'utf-8'
        return msg.get_payload(decode=True).decode(charset, errors='replace')

    print("⚠️ 警告：未在 EML 文件中找到 'text/html' 部分。")
    return None


def clean_text(text):
    """移除货币符号、逗号和不必要的空格，用于处理金额和'其他'值。"""
    if isinstance(text, str):
        text = text.replace('¥', '').replace('&yen;', '').replace(',', '').strip()
    # 如果是负数的话，转成正数，是正数的话，转成负数
    if text.startswith('-'):
        text = text[1:]
    else:
        text = '-' + text
    return text

def format_date(mmdd_text):
    """将'MMDD'格式的日期转换为'YYYY-MM-DD'。"""
    # time is
    # 获取当前的日期和时间
    now = datetime.datetime.now()
    # 格式化时间为 "小时:分钟" 的形式
    current_time = now.strftime("%H:%M")
    mmdd_text = mmdd_text.strip()
    if len(mmdd_text) == 4 and mmdd_text.isdigit():
        return f"{STATEMENT_YEAR}/{mmdd_text[:2]}/{mmdd_text[2:]} {current_time}"
    return mmdd_text

def classify_spend_or_income(cost_data):
    """根据交易类型判断是支出还是收入。"""
    if cost_data.startswith('-'):
        return '支出'
    else:
        return '收入'

def classify_transaction(description):
    """根据交易描述分类交易类型。"""
    # 简单的规则匹配示例
    if '餐饮' in description or '美食' in description or "速派" in description or "潘多拉" in description:
        return '用餐'
    elif '购物' in description or '购买' in description or "天猫" in description or "多点" in description:
        return '杂货'
    elif '交通' in description or '地铁' in description:
        return '公共交通: 地铁'
    elif '公交' in description:
        return '公共交通: 公交车'
    elif '公园' in description or '宫' in description or "寺" in description:
        return '娱乐'
    elif '奥塔奇' in description or "电费" in description:
        return '日常开支: 电费'
    else:
        return '其他'

def extract_transactions(html_content):
    """解析HTML内容并提取所有交易数据。"""
    soup = BeautifulSoup(html_content, 'html.parser')
    transactions = []
    
    # 1. 找到交易详情的主容器（通常包裹在 id='reportPanel1' 的SPAN标签内）
    report_panel = soup.find('span', id='reportPanel1') or soup

    # 2. 找到所有可能是交易记录的表格行
    # 交易数据行通常有固定的列数 (8个内容列 + 1个TD用于包装)
    all_rows = report_panel.find_all('tr')
    
    # 3. 筛选出有效的交易行：
    #    a) 包含至少8个TD元素（包括表格的左右边距TD）。
    #    b) 第二个TD（交易日）的文本是4位数字（MMDD）。
    transaction_rows = [
        row for row in all_rows 
        if len(row.find_all('td')) >= 8 and 
           row.find_all('td')[1].get_text(strip=True).isdigit()
    ]
    
    for row in transaction_rows:
        cells = row.find_all('td')

        if len(cells) < 8:
            continue

        try:
            # 提取并清理数据
            trans_date_mmdd = cells[1].get_text(strip=True)
            # post_date_mmdd = cells[2].get_text(strip=True)
            description = cells[3].get_text(strip=True)
            amount_raw = cells[4].get_text(strip=True)
            card_suffix = cells[5].get_text(strip=True)
            other_value = cells[6].get_text(strip=True)
            transaction_type = classify_transaction(description)
            spend_or_income = classify_spend_or_income(clean_text(amount_raw))
            transaction = {
                '交易日': format_date(trans_date_mmdd),
                # '记账日': format_date(post_date_mmdd),
                # '交易摘要': description,
                '交易金额 (CNY)': clean_text(amount_raw),
                '类别': transaction_type,
                '交易类型': spend_or_income,
                '账户': "招行",
                # '外币/积分/余额': clean_text(other_value),
            }
            
            print(transaction['交易日'])
            # 确保日期格式化成功才被认为是有效交易
            if re.match(r'^\d{4}/\d{2}/\d{2}', transaction['交易日']):
                 transactions.append(transaction)

        except Exception as e:
            # 打印错误信息，跳过无法解析的行
            # print(f"解析行时出错: {e}")
            continue

    return transactions

# --- 主程序执行 ---
html_content = extract_html_from_eml(INPUT_FILENAME)
# 假设您已将文件内容成功读取到 html_content 变量中

if html_content is None:
    print("❌ 未能从 EML 文件中提取 HTML 内容。")
    exit(1)

# 提取数据
transaction_data = extract_transactions(html_content)

# 写入 CSV 文件
if transaction_data:
    # 使用StringIO在内存中创建CSV内容，方便直接展示和复制
    csv_output = StringIO()
    fieldnames = transaction_data[0].keys()
    
    writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(transaction_data)
    
    csv_string = csv_output.getvalue()

    # 将内容写入本地文件
    with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvfile.write(csv_string)

    print(f"✅ 成功提取 {len(transaction_data)} 条交易记录。")
    print(f"✅ 数据已保存到文件：'{OUTPUT_FILENAME}'")
    
    print("\n--- 完整的 CSV 内容 ---")
    print(csv_string)
else:
    print("❌ 未能在HTML文件中找到任何交易记录。")