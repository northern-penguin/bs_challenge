import os
import pandas as pd
 
# 输入TXT文件的目录和输出CSV文件的目录
txt_directory = '/mnt/workspace/bs_challenge/tcdata/bs_challenge_financial_14b_dataset/pdf_txt_file'
output_file_dir = '/mnt/workspace/bs_challenge/tcdata/data/txt2csv_normalized'
 
# 确保输出目录存在
os.makedirs(output_file_dir, exist_ok=True)
 
 
# 处理TXT文件并保存为CSV文件的函数
def process_txt_to_csv(txt_path, output_dir):
    txt_name = os.path.basename(txt_path).replace('.txt', '')
    output_csv_path = os.path.join(output_dir, f"{txt_name}.PDF.csv")
 
    text_content = []
 
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for page_num, line in enumerate(lines):
            text_content.append({'页码': page_num, '纯文本': line.strip(), '位置文本': ''})
 
    text_df = pd.DataFrame(text_content)
    text_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
 
 
# 处理目录中的所有TXT文件
for file_name in os.listdir(txt_directory):
    if file_name.endswith('.txt'):
        txt_path = os.path.join(txt_directory, file_name)
        process_txt_to_csv(txt_path, output_file_dir)