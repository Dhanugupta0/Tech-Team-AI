from accounts import Account
import gradio as gr

# Initialize the account for demonstration
account = Account(username="DemoUser", initial_deposit=1000.0)

def deposit_funds(amount):
    account.deposit(amount)
    return f"Deposited ${amount}. Current balance: ${account.balance}"

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount}. Current balance: ${account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. Current holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. Current holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def portfolio_value():
    return f"Total portfolio value: ${account.get_portfolio_value()}"

def profit_or_loss():
    return f"Profit or Loss: ${account.get_profit_or_loss()}"

def transaction_history():
    return account.get_transaction_history()

with gr.Blocks() as demo:
    gr.Markdown("### Trading Account Management")
    
    with gr.Tab("Account Operations"):
        with gr.Row():
            deposit_amount = gr.Number(label="Deposit Amount")
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Result", interactive=False)

        deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)

        with gr.Row():
            withdraw_amount = gr.Number(label="Withdraw Amount")
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Result", interactive=False)

        withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)

        with gr.Row():
            buy_symbol = gr.Textbox(label="Symbol to Buy")
            buy_quantity = gr.Number(label="Quantity")
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Result", interactive=False)

        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)

        with gr.Row():
            sell_symbol = gr.Textbox(label="Symbol to Sell")
            sell_quantity = gr.Number(label="Quantity")
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Result", interactive=False)

        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)

    with gr.Tab("Portfolio Information"):
        value_btn = gr.Button("Get Portfolio Value")
        value_output = gr.Textbox(label="Result", interactive=False)
        value_btn.click(portfolio_value, outputs=value_output)
        
        profit_btn = gr.Button("Get Profit or Loss")
        profit_output = gr.Textbox(label="Result", interactive=False)
        profit_btn.click(profit_or_loss, outputs=profit_output)

        history_btn = gr.Button("Get Transaction History")
        history_output = gr.Textbox(label="Result", interactive=False)
        history_btn.click(transaction_history, outputs=history_output)

# Launch the Gradio interface
demo.launch()