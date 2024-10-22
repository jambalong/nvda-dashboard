from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd

top_sp500 = [
    'SPY', 'QQQ', 'DIA', 'IWM', 'VTI', 'AAPL', 'GOOGL', 'AMZN', 'META', 'MSFT',
    'NVDA', 'AMD', 'INTC', 'WM', 'RSG', 'TSLA', 'SHOP', 'NFLX', 'PG', 'KO', 'MCD'
]

def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='6mo', interval='1d')

    data['MA21'] = data['Close'].rolling(window=21).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    return data

app = Dash(__name__, external_stylesheets=['/assets/styles.css'])

app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': symbol, 'value': symbol} for symbol in top_sp500],
        value='NVDA'
    ),
    dcc.Graph(id='candlestick-chart')
])

@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('stock-dropdown', 'value')]
)

def create_candlestick_chart(selected_symbol):
    data = get_stock_data(selected_symbol)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlesticks',
                increasing=dict(line=dict(color='#a6e3a1')),
                decreasing=dict(line=dict(color='#f38ba8'))
            )
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MA21'],
            mode='lines',
            name='21-day MA',
            line=dict(color='#89b4fa', width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index, y=data['MA50'],
            mode='lines', name='50-day MA',
            line=dict(color='#fab387', width=2)
        )
    )

    fig.update_layout(
        title=f'{selected_symbol} Stock Price with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        plot_bgcolor='#181825',
        paper_bgcolor='#1e1e2e',
        font=dict(
            family='sans-serif',
            color='#b4befe'
        )
    )

    return fig

if __name__=='__main__':
    app.run_server()
