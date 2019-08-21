from WindPy import *
import pandas as pd
import datetime

w.start()

def get_price(code, price_type, begin_date, end_date, adj_direction='B'):
    adj_param = 'PriceAdj={0}'.format(adj_direction)
    data = w.wsd(code, price_type, begin_date, end_date, adj_param)
    seri = pd.Series(data.Data[0], index=data.Times)
    return seri

def get_close_price(code, begin_date, end_date, adj_direction='B'):
    seri = get_price(code, 'close', begin_date, end_date, adj_direction)
    seri.name = 'spj'
    seri.index.name = 'rq'
    return seri

def get_sector_index(sector):
    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d')
    data = w.wset("sectorconstituent","date={0};sectorid={1};field=wind_code,sec_name".format(today, sector))
    df = pd.DataFrame(data.Data,index=data.Fields)
    df = df.T
    return df

# 所有基金
def get_all_fund():
    return get_sector_index('2001000000000000')

# 所有指数
def get_all_index():
    l =[get_sector_index('1000002477000000'),
        get_sector_index('1000009424000000'),
        get_sector_index('1000009426000000'),
        get_sector_index('1000009416000000'),
        get_sector_index('1000003627000000'),
        get_sector_index('a39901011u000000'),
        get_sector_index('1000011658000000'),
        get_sector_index('1000009424000000'),
        get_sector_index('1000009425000000'),
        get_sector_index('1000009427000000'),
        get_sector_index('a39901010o000000'),
        ]

    df = pd.concat(l, ignore_index=True)
    df.drop_duplicates(['wind_code'], inplace=True)
    return df

# 中证海外指数
def get_zz_hw_index():
    return get_sector_index('a39901010o000000')

# 中证主题指数
def get_zz_zt_index():
    return get_sector_index('1000009427000000')

# 中证策略指数
def get_zz_cl_index():
    return get_sector_index('1000009425000000')

# 中证行业指数
def get_zz_hy_index():
    return get_sector_index('1000009424000000')

# 中证规模指数
def get_zz_size_index():
    return get_sector_index('1000002477000000')

# 沪深300一级行业指数
def get_hs300_first_level_index():
    return get_sector_index('1000011645000000')

# 中证全指一级行业
def get_qz_first_level_index():
    return get_sector_index('1000003895000000')

# 沪深300风格
def get_hs300_style_index():
    return get_sector_index('a39901010e000000')

# 填充证券名称
def pack_sec_name(code_list, df):
    code_df = pd.DataFrame({'wind_code': code_list})
    df = pd.merge(code_df, df, how='left', on='wind_code')
    return list(zip(list(df['wind_code']), list(df['sec_name'])))




