import yfinance as yf
import pandas as pd

class TradingApp:
    def __init__(self):
        self.portfolio = {}
        self.bank_balance = 0
        self.wallet_balance = 0
        self.balance = 0
        self.initial_investment = 0
        self.menu_options = {
            '1': self.buy_stock,
            '2': self.sell_stock,
            '3': self.display_portfolio,
            '4': self.calculate_portfolio_performance,
            '5': self.add_money_to_wallet,
            '6': self.view_wallet_balance,
            '7': self.check_stock_price,
            '8': self.show_ticker_list,
            '9': self.stock_analyzer,
            '10': exit
        }

    def run(self):
        while True:
            print("\nTrading Menu:")
            print("1. Buy Stock")
            print("2. Sell Stock")
            print("3. Display Portfolio")
            print("4. Calculate Portfolio Performance")
            print("5. Add money to Wallet")
            print("6. View Wallet Balance")
            print("7. Check Stock Price")
            print("8. Show Ticker List")
            print("9. Stock Analyzer")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice in self.menu_options:
                self.menu_options[choice]()
            else:
                print("Invalid choice. Please try again.")

    def buy_stock(self):
        try:
            ticker = input("Enter the ticker symbol of the stock you want to buy: ").upper()
            quantity = int(input("Enter the quantity of shares you want to buy: "))
            
            stock = yf.Ticker(ticker)
            history = stock.history(period='1d')
            current_price = history['Close'].iloc[-1]
            total_cost = current_price * quantity

            if self.check_balance(total_cost):
                if ticker in self.portfolio:
                    self.portfolio[ticker]['quantity'] += quantity
                else:
                    self.portfolio[ticker] = {'quantity': quantity, 'price': current_price}

                self.update_balance(-total_cost)
                self.update_wallet_balance(-total_cost)
                print(f"Bought {quantity} shares of {ticker} at ${current_price} each.")
            else:
                print("Insufficient balance.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print("Error:", e)

    def sell_stock(self):
        try:
            ticker = input("Enter the ticker symbol of the stock you want to sell: ").upper()
            quantity = int(input("Enter the quantity of shares you want to sell: "))

            if ticker in self.portfolio and self.portfolio[ticker]['quantity'] >= quantity:
                stock = yf.Ticker(ticker)
                history = stock.history(period='1d')
                current_price = history['Close'].iloc[-1]
                total_sell_amount = current_price * quantity

                self.update_balance(total_sell_amount)
                self.update_wallet_balance(total_sell_amount)
                self.portfolio[ticker]['quantity'] -= quantity
                if self.portfolio[ticker]['quantity'] == 0:
                    del self.portfolio[ticker]

                print(f"Sold {quantity} shares of {ticker} at ${current_price} each.")
            else:
                print("Insufficient shares to sell.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print("Error:", e)

    def display_portfolio(self):
        if not self.portfolio:
            print("Portfolio is empty.")
        else:
            print("Portfolio:")
            for ticker, data in self.portfolio.items():
                quantity = data['quantity']
                current_price = data['price']
                print(f"{ticker}: {quantity} shares (Current Price: ${current_price})")

    def add_money_to_wallet(self):
        try:
            amount = float(input("Enter the amount you want to add to the wallet: "))
            if amount > 0:
                self.bank_balance -= amount
                self.wallet_balance += amount
                self.update_balance(amount)
                print(f"Added ${amount} to the wallet.")
            else:
                print("Invalid amount. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print("Error:", e)

    def view_wallet_balance(self):
        print(f"Wallet Balance: ${self.wallet_balance}")

    def check_balance(self, amount):
        return self.balance >= amount

    def update_balance(self, amount):
        self.balance += amount

    def update_wallet_balance(self, amount):
        self.wallet_balance += amount

    def calculate_portfolio_performance(self):
        total_value = self.balance
        for ticker, data in self.portfolio.items():
            try:
                stock = yf.Ticker(ticker)
                history = stock.history(period='1d')
                current_price = history['Close'].iloc[-1]
                total_value += current_price * data['quantity']
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

        overall_change = total_value - self.initial_investment
        percentage_change = (overall_change / self.initial_investment) * 100 if self.initial_investment != 0 else 0

        if overall_change > 0:
            print(f"Overall portfolio is in profit by ${overall_change:.2f} ({percentage_change:.2f}%).")
        elif overall_change < 0:
            print(f"Overall portfolio is in loss by ${abs(overall_change):.2f} ({percentage_change:.2f}%).")
        else:
            print("Overall portfolio neither in profit nor in loss.")

    def check_stock_price(self):
        try:
            ticker = input("Enter the ticker symbol of the stock you want to check: ").upper()
            stock = yf.Ticker(ticker)
            current_price = stock.history(period='1d')['Close'].iloc[-1]
            print(f"Current price of {ticker}: ${current_price}")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    def show_ticker_list(self):
        try:
            tickers_df = pd.read_csv("D:\\Projects\stock Project\\nasdaq_tickers.csv")
            print("\nAvailable Tickers:")
            print(tickers_df.to_string(index=False))
        except Exception as e:
            print("Error:", e)
    
    def stock_analyzer(self):
        try:
            ticker = input("Enter the ticker symbol of the stock you want to analyze: ").upper()
            stock = yf.Ticker(ticker)
            history = stock.history(period='1y')
            prices = history['Close']
            current_price = prices.iloc[-1]
            avg_price_last_month = prices.iloc[-30:].mean()
            avg_price_last_year = prices.mean()

            projected_price = (current_price / avg_price_last_month) * avg_price_last_year
            percentage_increase = ((projected_price - current_price) / current_price) * 100 if current_price != 0 else 0

            print(f"Projected price of {ticker} in one year: ${projected_price:.2f}")
            print(f"Approximate percentage increase: {percentage_increase:.2f}%")
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")

if __name__ == "__main__":
    app = TradingApp()
    app.run()
