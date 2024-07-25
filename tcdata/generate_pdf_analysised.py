import os
import pandas as pd
import pdfplumber
 
# 输入PDF文件的目录和输出CSV文件的目录
pdf_directory = '/mnt/workspace/bs_challenge/tcdata/bs_challenge_financial_14b_dataset/pdf'
output_file_dir = '/mnt/workspace/bs_challenge/tcdata/data/pdf_analysised'
 
# 确保输出目录存在
os.makedirs(output_file_dir, exist_ok=True)
 
 
# 从PDF文件中提取文本和表格并保存为CSV文件的函数
def extract_text_and_tables_to_csv(pdf_path, output_dir):
    pdf_name = os.path.basename(pdf_path).replace('.PDF', '')
    output_csv_path = os.path.join(output_dir, f"{pdf_name}.PDF.csv")
 
    text_content = []
    table_content = []
 
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            text_content.append({'页码': page_num, '纯文本': text, '位置文本': page.extract_words()})
 
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    table_content.append({'页码': page_num, '表格': table})
 
    text_df = pd.DataFrame(text_content)
    table_df = pd.DataFrame(table_content)
    combined_df = pd.concat([text_df, table_df], axis=1)
 
    combined_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
 
 
# 处理目录中的所有PDF文件
for file_name in os.listdir(pdf_directory):
    if file_name.endswith('.PDF'):
        pdf_path = os.path.join(pdf_directory, file_name)
        print(file_name)
        extract_text_and_tables_to_csv(pdf_path, output_file_dir)