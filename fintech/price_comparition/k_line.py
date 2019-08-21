import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import wind_util
import plotly.graph_objs as go

app = dash.Dash()

def get_all_stock():
    df = wind_util.get_all_a_stock()
    return [ {'label': '{0} {1}'.format(x['wind_code'], x['sec_name']),
              'value':x['wind_code']} for index, x in df.iterrows() ]

end_date = datetime.datetime.today()
end_date = end_date - datetime.timedelta(days=1)
begin_date = end_date - datetime.timedelta(days=30)

app.layout = html.Div([
    html.H1('股价对比工具'),
	dcc.DatePickerRange(
        id='date-picker-range',
        display_format='YYYY-MM-DD',
        start_date=begin_date,
        end_date_placeholder_text='Select a date!',
	    end_date=end_date
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options= get_all_stock(),
        multi=True,
    ),
    dcc.Graph(id='my-graph')
])


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'), Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')])
def update_graph(selected_dropdown_value, begin_date, end_date):
    if selected_dropdown_value is None or len(selected_dropdown_value) < 2:
        return None

    stock1 = selected_dropdown_value[0]
    stock2 = selected_dropdown_value[1]
    seri = wind_util.get_close_price(stock1, begin_date, end_date)
    seri2 = wind_util.get_close_price(stock2, begin_date, end_date)

    trace1 = go.Scatter(
        x=list(seri.index),
        y=list(seri.values),
        name=stock1
    )
    trace2 = go.Scatter(
        x=list(seri2.index),
        y=list(seri2.values),
        name=stock2,
        yaxis='y2'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title='价格曲线',
        yaxis=dict(
            title=stock1
        ),
        yaxis2=dict(
            title=stock2,
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )

    #return go.Figure(data=data, layout=layout)
    return {
        'data': data,
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True)
