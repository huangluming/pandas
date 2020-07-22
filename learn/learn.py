import pandas as pd
import numpy as np

# url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv' #在线文件
url='learn/data.tsv' #下载后的文件
chipo = pd.read_csv(url, sep = '\t')
# print(chipo)

#第四题
#Step 4. See the first 10 entries
# print(chipo.head(10))


#第五题：这个题也很简单，让求这个数据集的数据量，要求给出两种方法
# print (chipo.shape[0])
# print (chipo.info)

#第六题，求数据的列数df.shape可以得出df的行数和列数
# print (chipo.shape[1])

#第七题，打印df的列名
# print(chipo.columns) 

#第八题，df的索引
# print(chipo.index) 

#第九题，求订购最多的iterm
print(chipo.groupby('item_name').max().head(1))
