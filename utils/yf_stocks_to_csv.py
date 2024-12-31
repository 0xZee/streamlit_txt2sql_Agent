import yfinance as yf
import pandas as pd


def yf_stocks_to_csv(tickers_list, keys_list, output_file):
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

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    return df


# Example usage:
tickers_list = ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AVGO', 'WMT', 'ORCL', 'COST', 'NFLX', 'CRM', 'KO', 'CSCO', 'NOW', 'IBM', 'BABA', 'DIS', 'AMD', 'ADBE', 'GE', 'PLTR', 'QCOM', 'RTX', 'NEE', 'HON', 'ANET', 'SHOP', 'ARM', 'UBER', 'PANW', 'APP', 'NKE', 'BYDDY', 'MRVL', 'MU', 'SPOT', 'INTC', 'CRWD', 'PYPL', 'MSTR', 'FTNT', 'CEG', 'WDAY', 'COIN', 'TTD', 'JD', 'SQ', 'SNOW', 'DDOG', 'VST', 'NET', 'RDDT', 'ZS', 'IOT', 'ALAB', 'PSTG', 'AFRM', 'GRAB', 'MDB', 'SMCI', 'SOFI', 'NTNX', 'CYBR', 'GME', 'RIVN', 'OKTA', 'RKLB', 'RBRK', 'MNDY', 'XPEV', 'ROKU', 'EXAS', 'PSN', 'IONQ', 'LCID', 'ENPH', 'NIO', 'GTLB', 'AES', 'SOUN', 'S', 'PATH', 'ASTS', 'PONY', 'LYFT', 'BE', 'ACHR', 'BEPC', 'RGTI', 'AI', 'VKTX', 'AVAV', 'BRZE', 'GSAT', 'CRSP', 'OKLO', 'QS', 'KC', 'RXRX', 'RPD', 'QBTS', 'QUBT', 'SMR', 'BEAM', 'TXG', 'LUNR', 'APLD', 'TDOC', 'SDGR', 'FSLY', 'DQ', 'PL', 'OLO', 'BBAI', 'TLRY', 'RDW', 'NTLA', 'RCAT', 'KULR', 'NNE', 'RZLV', 'SERV', 'LAES', 'ARQQ', 'DNA', 'PACB', 'QSI', 'CHPT', 'NNOX', 'CGC', 'SPIR', 'BKSY', 'QMCO', 'RR', 'VLN', 'ACB', 'QNCCF', 'EDIT', 'NKLA', 'SIDU', 'MDAI', 'LLAP', 'INTZ', 'VZ', 'T', 'V']
tickers_list_old = ["AVGO", "LUNR", "TLRY", "PL", "DQ", "OLO", "QBTS", "NTLA", "TSLA", "FSLY", "SDGR", "META", "TXG", "TDOC", "APLD", "ENPH", "PSN", "BYDDY", "MRVL", "EXAS", "XPEV", "NKE", "MU", "RBRK", "RKLB", "NKLA", "EDIT", "PANW", "OKTA", "RIVN", "NEE", "RTX", "ARM", "NTNX", "PLTR", "QCOM", "GE", "KC", "SMR", "GOOGL", "BEAM", "AMZN", "RGTI", "QS", "OKLO", "RXRX", "MDB", "PSTG", "AMD", "BABA", "GRAB", "SMCI", "IBM", "AFRM", "VLN", "NOW", "CSCO", "ADBE", "ACB", "IOT", "KO", "ARQQ", "MSFT", "NVDA", "ACHR", "AAPL", "CRSP", "ZS", "BKSY", "NET", "GSAT", "BRZE", "AVAV", "NNOX", "COST", "CGC", "VST", "ORCL", "AI", "VKTX", "BEPC", "BE", "LLAP", "DDOG", "SNOW", "CHPT", "DNA", "SOUN", "ASTS", "JD", "SERV", "PACB", "IONQ", "S", "PATH", "BBAI", "FTNT", "WMT", "COIN", "QUBT", "BHAT", "RDW", "INTC", "GTLB", "AES", "NIO", "CRWD", "RR", "PYPL", "NNE", "QMCO", "LAES", ]
keys_list = ['symbol', 'shortName', 'country','industry','sector','currentPrice','marketCap', 'trailingPE', 'forwardPE', 'priceToSalesTrailing12Months', 'priceToBook', 'debtToEquity','shortRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', 'beta', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'targetMeanPrice', 'targetHighPrice', 'recommendationKey','returnOnEquity', 'totalRevenue', 'freeCashflow', 'totalDebt', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'profitMargins','trailingPegRatio']
output_file = 'stocks_data.csv'

# Get data
dataset = get_stock_data(tickers_list, keys_list, output_file)
