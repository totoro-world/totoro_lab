import datetime
import security
import webbrowser
import value_stgy

correlation_period = 90
data_period = 360
shape_period = 15
today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
cor_sec_list = ['VIX.GI', 'DJI.GI', 'IXIC.GI', 'SPX.GI', 'USDX.FX', 'B.IPE', 'ABX.N']

stgy = value_stgy.ValueStgy('XAUCNY.IDC', cor_sec_list, end_date, data_period, correlation_period, shape_period, adf_pvalue=0.5)
(value_quant, correlation_quant, cointegration_quant) = stgy.run(False)
print('------quant report------')
print('[value quant]')
value_stgy.print_quant_ret(value_quant)
print('[correlation quant]')
value_stgy.print_quant_ret(correlation_quant)
print('[cointegration quant]')
value_stgy.print_quant_ret(cointegration_quant)

# open wallstreetcn web
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))  
webbrowser.get('chrome').open('https://wallstreetcn.com/')
webbrowser.get('chrome').open('https://www.goldtoutiao.com/news/gold-latest')
