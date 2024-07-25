# bs_challenge
博金LLM+Agent金融问答系统

# Readme

## 硬件配置

显存16G+

## 下载模型和数据

需要git lfs
'''shell
git lfs install
'''

### 下载数据集
在tcdata目录下

'''shell
git clone https://www.modelscope.cn/datasets/BJQW14B/bs_challenge_financial_14b_dataset.git
'''

### 下载模型
在tcdata目录下


如果显存大于32G，下载千问14Bchat

'''shell
git clone https://www.modelscope.cn/TongyiFinance/Tongyi-Finance-14B-Chat.git
'''

或者千问14Bchat-int4（显存大于16G）

'''shell
git clone https://www.modelscope.cn/TongyiFinance/Tongyi-Finance-14B-Chat-Int4.git
'''


## 运行程序
在app目录下执行run.sh
建议分步执行

## 方案来源

本方案思路来源于阿里云博金挑战赛 第四名
代码略作修改