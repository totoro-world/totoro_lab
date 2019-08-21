import three_line_stgy
import datetime
import wind_util

def test():
    sec_list = ['000849.SH']
    today = datetime.datetime.today()
    end_date = today - datetime.timedelta(days=1)
    df = wind_util.get_all_index()
    sec_list = wind_util.pack_sec_name(sec_list, df)
    stgy = three_line_stgy.ThreeLineStgy(sec_list[0], end_date)
    return stgy.run()
