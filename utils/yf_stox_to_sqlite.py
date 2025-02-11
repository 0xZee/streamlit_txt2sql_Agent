import yfinance as yf
import pandas as pd
import sqlite3

def yf_stocks_to_sqlite():
    tickers_list = ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO', 'WMT', 'LLY', 'ORCL', 'COST', 'NFLX', 'NVO', 'CRM', 'KO', 'CSCO', 'NOW', 'IBM', 'BABA', 'GE', 'AMD', 'DIS', 'ADBE', 'QCOM', 'PLTR', 'RTX', 'ARM', 'ANET', 'NEE', 'HON', 'UBER', 'SHOP', 'MU', 'PANW', 'APP', 'MRVL', 'BYDDY', 'NKE', 'CEG', 'SPOT', 'MSTR', 'PYPL', 'INTC', 'CRWD', 'COIN', 'FTNT', 'WDAY', 'JD', 'TTD', 'VST', 'SNOW', 'SQ', 'DDOG', 'HOOD', 'NET', 'RDDT', 'ZS', 'IOT', 'TER', 'PSTG', 'ALAB', 'MDB', 'GRAB', 'SMCI', 'AFRM', 'SOFI', 'NTNX', 'CYBR', 'OKTA', 'RIVN', 'XPEV', 'RBRK', 'MNDY', 'AUR', 'ROKU', 'RKLB', 'ONTO', 'GTLB', 'PSN', 'EXAS', 'LCID', 'NIO', 'ENPH', 'IONQ', 'AES', 'PATH', 'S', 'ASTS', 'LYFT', 'TEM', 'BE', 'SOUN', 'KTOS', 'AVAV', 'PONY', 'BEPC', 'BRZE', 'ACHR', 'AI', 'VKTX', 'OKLO', 'GSAT', 'CRSP', 'RGTI', 'SMR', 'QS', 'RXRX', 'RPD', 'KC', 'PLUG', 'APLD', 'BEAM', 'TXG', 'LUNR', 'TDOC', 'QBTS', 'SDGR', 'FSLY', 'OLO', 'DQ', 'QUBT', 'PL', 'TLRY', 'BBAI', 'RDW', 'SERV', 'NTLA', 'NNE', 'RCAT', 'DNA', 'RZLV', 'KULR', 'NNOX', 'CHPT', 'PACB', 'SPIR', 'LAES', 'QSI', 'VLN', 'RR', 'BKSY', 'ARQQ', 'CGC', 'ARBE', 'ACB', 'NUKK', 'QMCO', 'REKR', 'OPTT', 'NKLA', 'EDIT', 'INTZ', 'MDAI', 'SIDU', 'EKSO']
    keys_list = ['symbol', 'shortName', 'country','industry','sector','currentPrice','marketCap', 'trailingPE', 'forwardPE', 'priceToSalesTrailing12Months', 'priceToBook', 'debtToEquity','shortRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', 'beta', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'targetMeanPrice', 'targetHighPrice', 'recommendationKey','returnOnEquity', 'totalRevenue', 'freeCashflow', 'totalDebt', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'profitMargins','trailingPegRatio']
    output_file = 'stocks_data.csv'

    data_list = []
    # Fetch data for each ticker
    for ticker in tickers_list:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            stock_dict = {}
            for key in keys_list:
                stock_dict[key] = info.get(key, None)

            data_list.append(stock_dict)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")

    # Convert to DataFrame
    df = pd.DataFrame(data_list)
    #df.to_csv('stocks_data.csv', index=False)
    #print(f"Stock Data saved to stocks_data.csv}")
    print('# Stock Data saved to Dataframe df')
    print(f'Stocks : {len(df)}')

    # Connect to SQLite
    conn = sqlite3.connect('stox_db')
    
    # Save to SQLite
    df.to_sql('stox_table', conn, if_exists='replace', index=False)
    print('# Stock Data saved in sqlite3 database : stox_db / table : stox_table')
    conn.close()

    return df
