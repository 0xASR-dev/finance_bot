"""
Chatbot for Holdings and Trades Data Analysis
This chatbot answers questions based on holdings.csv and trades.csv files only.
If the answer cannot be found in the data, it responds with "Sorry can not find the answer"
"""

import pandas as pd
import re
from datetime import datetime


class DataChatbot:
    def __init__(self):
        self.holdings_df = None
        self.trades_df = None
        self.load_data()
    
    def load_data(self):
        """Load the CSV files into DataFrames"""
        try:
            self.holdings_df = pd.read_csv('holdings.csv')
            self.trades_df = pd.read_csv('trades.csv')
            
            # Clean column names (strip whitespace)
            self.holdings_df.columns = self.holdings_df.columns.str.strip()
            self.trades_df.columns = self.trades_df.columns.str.strip()
            
            # Convert numeric columns where needed
            numeric_cols_holdings = ['Qty', 'StartQty', 'Price', 'StartPrice', 
                                    'MV_Local', 'MV_Base', 'PL_DTD', 'PL_QTD', 'PL_MTD', 'PL_YTD']
            for col in numeric_cols_holdings:
                if col in self.holdings_df.columns:
                    self.holdings_df[col] = pd.to_numeric(self.holdings_df[col], errors='coerce')
            
            numeric_cols_trades = ['Quantity', 'Price', 'Principal', 'Interest', 
                                  'TotalCash', 'AllocationQTY', 'AllocationPrincipal']
            for col in numeric_cols_trades:
                if col in self.trades_df.columns:
                    self.trades_df[col] = pd.to_numeric(self.trades_df[col], errors='coerce')
                    
            print("Data loaded successfully!")
            print(f"Holdings: {len(self.holdings_df)} records")
            print(f"Trades: {len(self.trades_df)} records")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_all_funds(self):
        """Get list of all unique funds/portfolios"""
        holdings_funds = set(self.holdings_df['ShortName'].dropna().unique())
        holdings_portfolios = set(self.holdings_df['PortfolioName'].dropna().unique())
        trades_portfolios = set(self.trades_df['PortfolioName'].dropna().unique())
        return holdings_funds | holdings_portfolios | trades_portfolios
    
    def get_total_holdings_for_fund(self, fund_name):
        """Get total number of holdings for a specific fund"""
        # Search in both ShortName and PortfolioName
        mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
        count = mask.sum()
        return count if count > 0 else None
    
    def get_total_trades_for_fund(self, fund_name):
        """Get total number of trades for a specific fund"""
        mask = self.trades_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False)
        count = mask.sum()
        return count if count > 0 else None
    
    def get_total_holdings(self):
        """Get total number of holdings"""
        return len(self.holdings_df)
    
    def get_total_trades(self):
        """Get total number of trades"""
        return len(self.trades_df)
    
    def get_fund_pnl_ytd(self, fund_name=None):
        """Get YTD P&L for a fund or all funds"""
        if fund_name:
            mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                    self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
            filtered = self.holdings_df[mask]
            if len(filtered) > 0:
                return filtered['PL_YTD'].sum()
            return None
        else:
            # Return P&L for all funds
            return self.holdings_df.groupby('ShortName')['PL_YTD'].sum().to_dict()
    
    def get_best_performing_funds(self, n=5):
        """Get best performing funds by YTD P&L"""
        fund_pnl = self.holdings_df.groupby('ShortName')['PL_YTD'].sum().sort_values(ascending=False)
        return fund_pnl.head(n)
    
    def get_worst_performing_funds(self, n=5):
        """Get worst performing funds by YTD P&L"""
        fund_pnl = self.holdings_df.groupby('ShortName')['PL_YTD'].sum().sort_values(ascending=True)
        return fund_pnl.head(n)
    
    def get_fund_performance_ranking(self):
        """Get all funds ranked by YTD P&L"""
        fund_pnl = self.holdings_df.groupby('ShortName')['PL_YTD'].sum().sort_values(ascending=False)
        return fund_pnl
    
    def get_securities_for_fund(self, fund_name):
        """Get list of securities held by a fund"""
        mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
        filtered = self.holdings_df[mask]
        if len(filtered) > 0:
            return filtered['SecName'].unique().tolist()
        return None
    
    def get_security_types_for_fund(self, fund_name):
        """Get security types held by a fund"""
        mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
        filtered = self.holdings_df[mask]
        if len(filtered) > 0:
            return filtered['SecurityTypeName'].unique().tolist()
        return None
    
    def get_trade_types_summary(self):
        """Get summary of trade types (Buy/Sell)"""
        return self.trades_df['TradeTypeName'].value_counts().to_dict()
    
    def get_trades_by_type(self, trade_type):
        """Get trades filtered by type (Buy/Sell)"""
        mask = self.trades_df['TradeTypeName'].str.lower() == trade_type.lower()
        return mask.sum()
    
    def get_fund_market_value(self, fund_name):
        """Get total market value for a fund"""
        mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
        filtered = self.holdings_df[mask]
        if len(filtered) > 0:
            return filtered['MV_Base'].sum()
        return None
    
    def get_custodians(self):
        """Get list of all custodians"""
        holdings_custodians = set(self.holdings_df['CustodianName'].dropna().unique())
        trades_custodians = set(self.trades_df['CustodianName'].dropna().unique())
        return holdings_custodians | trades_custodians
    
    def get_counterparties(self):
        """Get list of all counterparties"""
        return self.trades_df['Counterparty'].dropna().unique().tolist()
    
    def get_security_types(self):
        """Get all security types in holdings"""
        return self.holdings_df['SecurityTypeName'].dropna().unique().tolist()
    
    def get_holdings_by_security_type(self, sec_type):
        """Get holdings count by security type"""
        mask = self.holdings_df['SecurityTypeName'].str.lower().str.contains(sec_type.lower(), na=False)
        return mask.sum()
    
    def get_pnl_mtd(self, fund_name=None):
        """Get MTD P&L"""
        if fund_name:
            mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                    self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
            filtered = self.holdings_df[mask]
            if len(filtered) > 0:
                return filtered['PL_MTD'].sum()
            return None
        return self.holdings_df.groupby('ShortName')['PL_MTD'].sum().to_dict()
    
    def get_pnl_qtd(self, fund_name=None):
        """Get QTD P&L"""
        if fund_name:
            mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                    self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
            filtered = self.holdings_df[mask]
            if len(filtered) > 0:
                return filtered['PL_QTD'].sum()
            return None
        return self.holdings_df.groupby('ShortName')['PL_QTD'].sum().to_dict()
    
    def get_total_quantity_for_fund(self, fund_name):
        """Get total quantity of holdings for a fund"""
        mask = (self.holdings_df['ShortName'].str.lower().str.contains(fund_name.lower(), na=False) |
                self.holdings_df['PortfolioName'].str.lower().str.contains(fund_name.lower(), na=False))
        filtered = self.holdings_df[mask]
        if len(filtered) > 0:
            return filtered['Qty'].sum()
        return None

    def extract_fund_name(self, question):
        """Extract fund name from question"""
        all_funds = self.get_all_funds()
        question_lower = question.lower()
        
        for fund in all_funds:
            if fund.lower() in question_lower:
                return fund
        
        # Try partial matching
        for fund in all_funds:
            # Check if any significant word from fund name is in question
            fund_words = fund.lower().split()
            for word in fund_words:
                if len(word) > 3 and word in question_lower:
                    return fund
        
        return None

    def process_question(self, question):
        """Process user question and return appropriate answer"""
        question_lower = question.lower().strip()
        
        # Check for empty question
        if not question_lower:
            return "Please enter a question."
        
        # List all funds
        if any(phrase in question_lower for phrase in ['list all funds', 'all funds', 'what funds', 'which funds are there', 'show funds', 'available funds']):
            funds = self.get_all_funds()
            if funds:
                return f"Available funds/portfolios:\n" + "\n".join(f"  - {fund}" for fund in sorted(funds))
            return "Sorry can not find the answer"
        
        # Total holdings (overall)
        if ('total' in question_lower and 'holdings' in question_lower) or ('how many' in question_lower and 'holdings' in question_lower):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                count = self.get_total_holdings_for_fund(fund_name)
                if count:
                    return f"Total number of holdings for {fund_name}: {count}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                return f"Total number of holdings across all funds: {self.get_total_holdings()}"
        
        # Total trades (overall or for fund)
        if ('total' in question_lower and 'trades' in question_lower) or ('how many' in question_lower and 'trades' in question_lower):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                count = self.get_total_trades_for_fund(fund_name)
                if count:
                    return f"Total number of trades for {fund_name}: {count}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                return f"Total number of trades across all funds: {self.get_total_trades()}"
        
        # Best performing funds
        if any(phrase in question_lower for phrase in ['best performing', 'top performing', 'highest profit', 'best fund', 'top fund', 'performed better', 'which fund performed']):
            top_funds = self.get_best_performing_funds(10)
            if len(top_funds) > 0:
                result = "Best performing funds by YTD P&L:\n"
                for i, (fund, pnl) in enumerate(top_funds.items(), 1):
                    result += f"  {i}. {fund}: ${pnl:,.2f}\n"
                return result
            return "Sorry can not find the answer"
        
        # Worst performing funds
        if any(phrase in question_lower for phrase in ['worst performing', 'lowest profit', 'worst fund', 'poor performing', 'lowest performing']):
            worst_funds = self.get_worst_performing_funds(10)
            if len(worst_funds) > 0:
                result = "Worst performing funds by YTD P&L:\n"
                for i, (fund, pnl) in enumerate(worst_funds.items(), 1):
                    result += f"  {i}. {fund}: ${pnl:,.2f}\n"
                return result
            return "Sorry can not find the answer"
        
        # Fund performance/ranking
        if any(phrase in question_lower for phrase in ['fund performance', 'performance ranking', 'rank funds', 'compare funds']):
            ranking = self.get_fund_performance_ranking()
            if len(ranking) > 0:
                result = "Fund Performance Ranking by YTD P&L:\n"
                for i, (fund, pnl) in enumerate(ranking.items(), 1):
                    result += f"  {i}. {fund}: ${pnl:,.2f}\n"
                return result
            return "Sorry can not find the answer"
        
        # P&L for specific fund (YTD)
        if any(phrase in question_lower for phrase in ['ytd', 'yearly', 'year to date', 'annual', 'profit and loss', 'pnl', 'p&l', 'profit', 'loss']):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                pnl = self.get_fund_pnl_ytd(fund_name)
                if pnl is not None:
                    return f"YTD P&L for {fund_name}: ${pnl:,.2f}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                # Show all funds P&L
                all_pnl = self.get_fund_pnl_ytd()
                if all_pnl:
                    result = "YTD P&L for all funds:\n"
                    sorted_pnl = sorted(all_pnl.items(), key=lambda x: x[1], reverse=True)
                    for fund, pnl in sorted_pnl:
                        result += f"  - {fund}: ${pnl:,.2f}\n"
                    return result
                return "Sorry can not find the answer"
        
        # MTD P&L
        if 'mtd' in question_lower or 'month to date' in question_lower:
            fund_name = self.extract_fund_name(question)
            if fund_name:
                pnl = self.get_pnl_mtd(fund_name)
                if pnl is not None:
                    return f"MTD P&L for {fund_name}: ${pnl:,.2f}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                all_pnl = self.get_pnl_mtd()
                if all_pnl:
                    result = "MTD P&L for all funds:\n"
                    sorted_pnl = sorted(all_pnl.items(), key=lambda x: x[1], reverse=True)
                    for fund, pnl in sorted_pnl:
                        result += f"  - {fund}: ${pnl:,.2f}\n"
                    return result
                return "Sorry can not find the answer"
        
        # QTD P&L
        if 'qtd' in question_lower or 'quarter to date' in question_lower:
            fund_name = self.extract_fund_name(question)
            if fund_name:
                pnl = self.get_pnl_qtd(fund_name)
                if pnl is not None:
                    return f"QTD P&L for {fund_name}: ${pnl:,.2f}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                all_pnl = self.get_pnl_qtd()
                if all_pnl:
                    result = "QTD P&L for all funds:\n"
                    sorted_pnl = sorted(all_pnl.items(), key=lambda x: x[1], reverse=True)
                    for fund, pnl in sorted_pnl:
                        result += f"  - {fund}: ${pnl:,.2f}\n"
                    return result
                return "Sorry can not find the answer"
        
        # Securities for a fund
        if any(phrase in question_lower for phrase in ['securities', 'what securities', 'which securities', 'holdings for']):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                securities = self.get_securities_for_fund(fund_name)
                if securities:
                    return f"Securities held by {fund_name}:\n" + "\n".join(f"  - {sec}" for sec in securities)
                return f"Sorry can not find the answer for fund '{fund_name}'"
            return "Please specify a fund name."
        
        # Security types
        if any(phrase in question_lower for phrase in ['security types', 'asset types', 'type of securities', 'types of assets']):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                types = self.get_security_types_for_fund(fund_name)
                if types:
                    return f"Security types for {fund_name}: {', '.join(types)}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                types = self.get_security_types()
                if types:
                    return f"Available security types: {', '.join(types)}"
                return "Sorry can not find the answer"
        
        # Trade types summary
        if any(phrase in question_lower for phrase in ['trade types', 'buy and sell', 'buys and sells', 'trade summary']):
            summary = self.get_trade_types_summary()
            if summary:
                result = "Trade Types Summary:\n"
                for trade_type, count in summary.items():
                    result += f"  - {trade_type}: {count}\n"
                return result
            return "Sorry can not find the answer"
        
        # Number of buys
        if 'buy' in question_lower and ('how many' in question_lower or 'number of' in question_lower or 'total' in question_lower):
            count = self.get_trades_by_type('buy')
            if count > 0:
                return f"Total number of Buy trades: {count}"
            return "Sorry can not find the answer"
        
        # Number of sells
        if 'sell' in question_lower and ('how many' in question_lower or 'number of' in question_lower or 'total' in question_lower):
            count = self.get_trades_by_type('sell')
            if count > 0:
                return f"Total number of Sell trades: {count}"
            return "Sorry can not find the answer"
        
        # Market value for fund
        if any(phrase in question_lower for phrase in ['market value', 'total value', 'mv', 'aum']):
            fund_name = self.extract_fund_name(question)
            if fund_name:
                mv = self.get_fund_market_value(fund_name)
                if mv is not None:
                    return f"Total market value for {fund_name}: ${mv:,.2f}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            else:
                total_mv = self.holdings_df['MV_Base'].sum()
                return f"Total market value across all funds: ${total_mv:,.2f}"
        
        # Custodians
        if 'custodian' in question_lower:
            custodians = self.get_custodians()
            if custodians:
                return f"Custodians:\n" + "\n".join(f"  - {c}" for c in sorted(custodians))
            return "Sorry can not find the answer"
        
        # Counterparties
        if 'counterpart' in question_lower:
            counterparties = self.get_counterparties()
            if counterparties:
                return f"Counterparties:\n" + "\n".join(f"  - {c}" for c in sorted(counterparties))
            return "Sorry can not find the answer"
        
        # Holdings by security type
        if any(sec_type.lower() in question_lower for sec_type in ['equity', 'bond', 'option', 'assetbacked', 'fx forward']):
            for sec_type in ['Equity', 'Bond', 'Option', 'AssetBacked', 'FX Forward']:
                if sec_type.lower() in question_lower:
                    count = self.get_holdings_by_security_type(sec_type)
                    if count > 0:
                        return f"Number of {sec_type} holdings: {count}"
            return "Sorry can not find the answer"
        
        # Quantity for fund
        if 'quantity' in question_lower or 'qty' in question_lower:
            fund_name = self.extract_fund_name(question)
            if fund_name:
                qty = self.get_total_quantity_for_fund(fund_name)
                if qty is not None:
                    return f"Total quantity for {fund_name}: {qty:,.0f}"
                return f"Sorry can not find the answer for fund '{fund_name}'"
            return "Please specify a fund name for quantity information."
        
        # Help command
        if any(phrase in question_lower for phrase in ['help', 'what can you', 'commands', 'examples']):
            return """I can help you with questions about holdings and trades data. Here are some examples:

📊 Holdings Questions:
  - "Total number of holdings for Garfield"
  - "How many holdings are there?"
  - "What securities does Heather hold?"
  - "What are the security types for MNC Inv?"
  - "Number of equity holdings"

📈 Trades Questions:
  - "Total number of trades for HoldCo 1"
  - "How many trades are there?"
  - "Trade types summary"
  - "How many buy trades?"
  - "How many sell trades?"

💰 Performance Questions:
  - "Which funds performed better?"
  - "Best performing funds"
  - "Worst performing funds"
  - "YTD P&L for Ytum"
  - "MTD P&L for all funds"
  - "Fund performance ranking"

💵 Value Questions:
  - "Market value for Garfield"
  - "Total market value"

🏢 Other Questions:
  - "List all funds"
  - "What are the custodians?"
  - "What are the counterparties?"
"""
        
        return "Sorry can not find the answer"


def main():
    print("=" * 60)
    print("Welcome to the Holdings & Trades Data Chatbot!")
    print("=" * 60)
    print("\nType 'help' for example questions, or 'quit' to exit.\n")
    
    chatbot = DataChatbot()
    print()
    
    while True:
        try:
            question = input("You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\nThank you for using the chatbot. Goodbye!")
                break
            
            if not question:
                continue
            
            answer = chatbot.process_question(question)
            print(f"\nBot: {answer}\n")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the chatbot. Goodbye!")
            break
        except Exception as e:
            print(f"\nBot: Sorry, an error occurred: {e}\n")


if __name__ == "__main__":
    main()
