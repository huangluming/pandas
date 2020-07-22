import pandas as pd
import numpy as np
import os
import sqlalchemy

# 获取文件内的文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

# 文件存入df
# 根据文件的编码格式修改ISO-8859-1
def get_df(dir_name):
    df = pd.DataFrame()
    files = file_name(dir_name)
    for file in files:
        df_temp = pd.DataFrame()
        df_temp = pd.read_csv(
            dir_name + '/' + file, encoding='ISO-8859-1', sep='\t', error_bad_lines=False)
        df_temp['shop-name'] = file.split('.')[0].split('-')[0]
        df_temp['country'] = file.split('.')[0].split('-')[1]

        df = df.append(df_temp)

    return df

# 文件夹名称
dir_name = 'data/test'

# 获取文件夹下所有的内容
df_asin=pd.read_excel('data/xxx.xlsx')
df = get_df(dir_name)

df_result=pd.merge(df_asin, df, how='left', left_on=['国家', '店铺','公司SKU','FNSKU'], right_on=['country', 'shop-name','sku','fnsku'],
 sort=False, copy=False)

df_result.loc[df_result['received-date'].isna()==False, '开售时间' ] = df_result['received-date']

df_result=df_result.iloc[:,1:16].head()

print(df_result)


#测试文件里AM1-US.txt是可以个xxx.xlsx匹配的一条数据






