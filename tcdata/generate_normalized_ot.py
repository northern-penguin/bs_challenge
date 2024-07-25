import os
import csv
from collections import Counter
import re

# 定义停用词文件路径
baidu_stopwords_path = '/mnt/workspace/bs_challenge/tcdata/stopwords/baidu_stopwords.txt'
hit_stopwords_path = '/mnt/workspace/bs_challenge/tcdata/stopwords/hit_stopwords.txt'

# 初始化一个空集合用于存储停用词，集合自动去重
# stopwords = set()

stopwords = set([
    '根据', '招股意见书', '招股意向书', '报告期内', '截至', '千元', '万元',
    '哪里', '哪些', '哪个', '分别', '知道', '什么', '是否', '分别', '多少',
    '为', '?', '是', '和', '的', '我', '想', '元', '。', '？', '，', '怎样',
    '谁', '以及', '了', '在', '哪', '对'
])

# 定义一个函数来读取停用词文件并更新停用词集合
def read_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除每行的前后空白字符，包括换行符，然后添加到集合中
            stopwords.add(line.strip())

# 读取两个文件中的停用词
# read_stopwords(baidu_stopwords_path)
# read_stopwords(hit_stopwords_path)

# 打印停用词列表的大小，确认是否读取成功
print(f'Total number of stopwords: {len(stopwords)}')



# 定义要遍历的文件夹路径和输出文件路径
texts_folder = '/mnt/workspace/bs_challenge/tcdata/bs_challenge_financial_14b_dataset/pdf_txt_file'
output_csv = '/mnt/workspace/bs_challenge/tcdata/data/AD_normalized_ot-defaultSW.csv'

# 打开输出文件准备写入
with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csvwriter = csv.writer(csvfile)
    # 写入标题行
    csvwriter.writerow(['文件名', 'normalized'])
    
    # 遍历texts文件夹下的所有txt文件
    for filename in os.listdir(texts_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(texts_folder, filename)
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                # 读取文件内容
                text = file.read()
                # 预处理文本：去除停用词和特殊字符
                words = re.findall(r'\b\w+\b', text.lower())
                filtered_words = [word for word in words if word not in stopwords]
                # 计算词频
                word_counts = Counter(filtered_words)
                # 将词频字典转换为字符串
                normalized_dict_str = str(dict(word_counts))
                # 写入CSV文件
                csvwriter.writerow([filename, normalized_dict_str])

print('处理完成，数据已写入:', output_csv)