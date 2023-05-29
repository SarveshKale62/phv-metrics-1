from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
import yfinance as yf
from yfinance import Ticker
from datetime import datetime,timedelta
import random

# x = datetime(2023,5,17)
asset_symbols = ["AAPL","AMZN","GOOGL"]

app = Flask(__name__)
 

def calculate_sp500_weight(asset_symbol, date):
    try:
        asset_ticker = Ticker(asset_symbol)
        asset_data = asset_ticker.history(start=date)
        asset_shares = asset_ticker.info['sharesOutstanding']
        with open('marketcap.txt','r') as f:
          market_cap = f.read()
        
        if not asset_data.empty:
            asset_market_cap = asset_data["Close"].iloc[0]*asset_shares
            sp500_weight = (asset_market_cap / float(market_cap)) * 100
            return round(sp500_weight,ndigits=6)
        else:
            return None

    except Exception as e:
        print("Error calculating S&P 500 weight %:", str(e))
        return None


def calculate_ytd_performance(asset_symbol, date):
    try:
        asset_ticker = Ticker(asset_symbol)
        year_start_date = datetime(datetime.now().year, 1, 1)
        asset_data = asset_ticker.history(start=year_start_date,end=date)
        
        if not asset_data.empty:
            first_price = asset_data['Close'].iloc[0]
            last_price = asset_data['Close'].iloc[-1]
            ytd_performance = (last_price - first_price) / first_price * 100
            return round(ytd_performance,ndigits=6)
        else:
            return None

    except Exception as e:
        print("Error calculating YTD performance:", str(e))
        return None


def calculate_short_interest(asset_symbol, date):
    try:
        asset_ticker = Ticker(asset_symbol)
        history = asset_ticker.history(start=date)

        if not history.empty:
            volume = history['Volume'].iloc[0]
            outstanding_shares = asset_ticker.info.get("sharesOutstanding")

            if volume and outstanding_shares:
                short_interest = (volume / outstanding_shares) * 100
                return round(short_interest,ndigits=7)
            else:
                return None
        else:
            return None

    except Exception as e:
        print("Error calculating short interest:", str(e))
        return None


def calculate_operating_margin():
    try:
        operating_incomes=[]
        total_revenues=[]

        for i in range(0,4):
            operating_incomes.append(random.randint(10000000,50000000))
            total_revenues.append(random.randint(50000000,100000000))

        operating_margins=[]
        for i in range(len(operating_incomes)):  
            operating_margins.append(operating_incomes[i]/total_revenues[i])
        
        avg_operating_margins = np.mean(operating_margins)*100
        return avg_operating_margins
    
    except Exception as e:
        print("Error calculating operating margin:", str(e))
        return None


def calculate_revenue_growth():
    try:
        current_year_revenue = random.randint(200000000,400000000)
        previous_year_revenue = random.randint(100000000,300000000)

        annual_revenue_growth = ((current_year_revenue - previous_year_revenue) / previous_year_revenue) * 100
        return annual_revenue_growth
        

    except Exception as e:
        print("Error calculating revenue growth:", str(e))
        return None


def calculate_net_income_growth():
    try:
        current_year_net_income = random.randint(200000000,400000000)
        previous_year_net_income = random.randint(100000000,300000000)

        annual_revenue_growth = ((current_year_net_income - previous_year_net_income) / previous_year_net_income) * 100
        return annual_revenue_growth

    except Exception as e:
        print("Error calculating net income growth:", str(e))
        return None


def calculate_ev_to_ebitda_capex(asset_symbol):
    try:
        asset_ticker = Ticker(asset_symbol)
        ebitda = random.randint(80000000,130000000)
        capex = random.randint(6000000,12000000)
        enterprise_value = asset_ticker.info['enterpriseValue']
        
        if enterprise_value and ebitda and capex != 0:
            ev_to_ebitda_capex = enterprise_value / (ebitda - capex)
            return ev_to_ebitda_capex
        else:
            return None
        
    except Exception as e:
        print("Error calculating EV / (EBITDA - Capex):", str(e))
        return None

        
def get_last_close_price(asset_symbol, date):
    try:
        asset_ticker = Ticker(asset_symbol)
        asset_data = asset_ticker.history(start=date, end=date+timedelta(days=1))

        if not asset_data.empty:
            last_close_price = asset_data["Close"].iloc[0]
            return round(last_close_price,ndigits=2)
        else:
            return None

    except Exception as e:
        print("Error retrieving last close price:", str(e))
        return None
    
def calculate_metrics(asset_symbol, date):
    metrics = {
        "sp500_weight": calculate_sp500_weight(asset_symbol,date),
        "last_close_price": get_last_close_price(asset_symbol,date),
        "operating_margin": calculate_operating_margin(),
        "ev_to_ebitda_capex": calculate_ev_to_ebitda_capex(asset_symbol),
        "ytd_performance": calculate_ytd_performance(asset_symbol,date),
        "revenue_growth": calculate_revenue_growth(),
        "net_income_growth": calculate_net_income_growth(),
        "short_interest": calculate_short_interest(asset_symbol, date),
    }

    return metrics

def calculate_multiple_metrics(asset_symbols, date):
    results = []
    for asset_symbol in asset_symbols:
        metrics = calculate_metrics(asset_symbol, date)
        result = {
            "asset_symbol": asset_symbol,
            "metrics": metrics
        }
        results.append(result)
    return results


@app.route('/metrics', methods=['GET','POST'])
# @app.route('/metrics')
# def get_time():
#     date = x
#     results = calculate_multiple_metrics(asset_symbols,date)
#     return jsonify(results)

def get_metrics():
    try:
        data = request.get_json()
        date_str = data.get('date')

        if not date_str:
            return jsonify({"error": "No date provided."}), 400

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        results = calculate_multiple_metrics(asset_symbols, date_obj)
        return jsonify(results)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)