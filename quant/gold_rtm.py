import datetime
import rtm_stgy
import wind_util

today = datetime.datetime.today()
end_date = today - datetime.timedelta(days=1)
stgy = rtm_stgy.RtmStgy(('XAUCNY.IDC', 'gold'), end_date, 360, change_percent=0.01, regime_percent=0.05)
(max_row, min_row) = stgy.run()










