import json
import csv
import pandas as pd
import copy 
n = 30
cap = 4
import re
from collections import Counter
import math

pattern1 = r'截至'
pattern2 = r'\d{1,4}年\d{1,2}月\d{1,2}日'

q_file_dir = '/mnt/workspace/bs_challenge/app/intermediate/A02_question_classify_entity.csv'
q_file =  pd.read_csv(q_file_dir,delimiter = ",",header = 0)


pdf_csv_file_dir = '/mnt/workspace/bs_challenge/tcdata/data/pdf_analysised'
from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download
from modelscope import GenerationConfig

model_dir = '/mnt/workspace/bs_challenge/tcdata/models/Tongyi-Finance-14B-Chat-Int4'

# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

def counter_cosine_similarity(c1, c2): #使用截断的ccs
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    
    if magA * magB != 0:
        return dotprod / (magA * magB)
    else:
        return 0
    
    
g = open('/mnt/workspace/bs_challenge/app/intermediate/AB01_question_with_related_text_rp.csv', 'w', newline='', encoding = 'utf-8-sig') 
csvwriter = csv.writer(g)
csvwriter.writerow(['问题id','问题','对应实体','csv文件名','top_n_pages_index','top_n_pages_similarity','top_n_pages'])

stopword_list = ['根据','招股意见书','招股意向书','报告期内','截至','千元','万元','哪里','哪些','哪个','分别','知道',"什么",'是否','分别','多少','为','?','是','和',
'的','我','想','元','。','？','，','怎样','谁','以及','了','在','哪','对']
bd_list = [',','.','?','。','，','[',']']

print('C02_Started')
for cyc in range(1000):
    temp_q = q_file[cyc:cyc+1]['问题'][cyc]
    
    str1_list = re.findall(pattern1,temp_q)
    str2_list = re.findall(pattern2,temp_q)
    
 
        
    temp_e = q_file[cyc:cyc+1]['对应实体'][cyc]
    if temp_e == 'N_A':
        csvwriter.writerow([q_file[cyc:cyc+1]['问题id'][cyc],
                            q_file[cyc:cyc+1]['问题'][cyc],
                            'N_A','N_A','N_A','N_A'])
        continue
    else:
        temp_csv_dir = pdf_csv_file_dir +'/' + q_file[cyc:cyc+1]['csv文件名'][cyc]
        company_csv = pd.read_csv(temp_csv_dir,delimiter = ",",header = 0)
        temp_q = temp_q.replace(' ','')
        #去除截至与日期，使得匹配更有针对性
        for word in str1_list:
            temp_q = temp_q.replace(word,'')
        for word in str2_list:
            temp_q = temp_q.replace(word,'')  
            
            
        #停用词？
        temp_q = temp_q.replace(temp_e,' ')
        for word in stopword_list:
            temp_q = temp_q.replace(word,' ')
        temp_q_list = temp_q.split()
        temp_q_tokens = list()
        for word in temp_q_list:
            temp_q_tokens_add = tokenizer(word)
            temp_q_tokens_add = temp_q_tokens_add['input_ids']
            for word_add in temp_q_tokens_add:
                temp_q_tokens.append(word_add)

        C_temp_q_tokens = Counter(temp_q_tokens)
        list_sim = list()
        for cyc2 in range(len(company_csv)):
            temp_sim = 0
            temp_file_piece = ''
            if company_csv[cyc2:cyc2+1]['纯文本'][cyc2] == company_csv[cyc2:cyc2+1]['纯文本'][cyc2]:
                temp_file_piece = company_csv[cyc2:cyc2+1]['纯文本'][cyc2]
            if company_csv[cyc2:cyc2+1]['表格'][cyc2] == company_csv[cyc2:cyc2+1]['表格'][cyc2]:
                temp_file_piece = temp_file_piece + company_csv[cyc2:cyc2+1]['表格'][cyc2].replace('None'," ")
            
            for bd in bd_list:
                temp_file_piece = temp_file_piece.replace(bd,' ')
                
            temp_s_tokens = tokenizer(temp_file_piece)
            temp_s_tokens = temp_s_tokens['input_ids']
            
            C_temp_s_tokens = Counter(temp_s_tokens)
            C_temp_s_tokens['220'] = 0
            
            for token in C_temp_s_tokens:
                if C_temp_s_tokens[token] >= cap:
                    C_temp_s_tokens[token] = cap
            
            
            if temp_q_tokens == '':
                temp_sim = 0
            else:
                temp_sim = counter_cosine_similarity(C_temp_q_tokens,C_temp_s_tokens)
            list_sim.append(temp_sim)
            
        #找到相似度最大的
        t = copy.deepcopy(list_sim) 
        max_number = []
        max_index = []
        
        for _ in range(n):
            number = max(t)
            index = t.index(number)
            t[index] = 0
            max_number.append(number)
            max_index.append(index)
        t = []
        
        #将对应的index片段放入文件
        temp_file_pieces_list = list()
        for index in max_index:
            temp_dict = {}
            if company_csv[index:index+1]['纯文本'][index] == company_csv[index:index+1]['纯文本'][index]:
                temp_dict['text'] = company_csv[index:index+1]['纯文本'][index]
            if company_csv[index:index+1]['表格'][index] == company_csv[index:index+1]['表格'][index]:
                temp_dict['table'] = company_csv[index:index+1]['表格'][index].replace('None'," ")
            
            temp_file_pieces_list.append(temp_dict)
            
            
        csvwriter.writerow([q_file[cyc:cyc+1]['问题id'][cyc],
                    q_file[cyc:cyc+1]['问题'][cyc],
                    temp_e,q_file[cyc:cyc+1]['csv文件名'][cyc],max_index,max_number,temp_file_pieces_list])
g.close()  
                      