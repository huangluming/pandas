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

# 计算df，根据fnsku分组，求received-date最小值
def get_latest_time(df):
    return df.groupby(['fnsku'])['received-date'].agg(min)

# df数据插入mysql，若存在则替换
def insert_mysql(engine, df):
    df.to_sql('testpd', con=engine, if_exists='append', index=False)


# 数据库配置信息
# engine = sqlalchemy.create_engine(
#     "mysql+mysqldb://root:AJHJUe7y$1ECR#Pw@192.168.1.110:3306/prod_dw_rzb", encoding='utf8')

engine = sqlalchemy.create_engine(
    "mysql+pymysql://root:Alarm41.#@122.51.96.100:3306/test", encoding='utf8')
# 文件夹名称
dir_name = 'test'


# 获取文件夹下所有的内容
df = get_df(dir_name)

print(df)
# 获取fnsku的最早时间
# print(get_latest_time(df))

# df数据插入musql
insert_mysql(engine, df)
