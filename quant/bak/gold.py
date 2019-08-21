import datetime
import security
import webbrowser
import value_stgy

correlation_period = 90
data_period = 360
shape_period = 15
today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
cor_sec_list = ['VIX.GI', 'DJI.GI', 'IXIC.GI', 'SPX.GI', 'USDX.FX', 'B.IPE']

stgy = value_stgy.ValueStgy('SPTAUUSDOZ.IDC', cor_sec_list, end_date, data_period, correlation_period, shape_period)
stgy.run(False)

# open wallstreetcn web
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))  
webbrowser.get('chrome').open('https://wallstreetcn.com/')
