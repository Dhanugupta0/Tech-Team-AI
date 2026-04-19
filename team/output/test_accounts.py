import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account("test_user", 1000.0)

    def test_initialization(self):
        self.assertEqual(self.account.username, "test_user")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['action'], 'deposit')

        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw(self):
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['action'], 'withdraw')

        with self.assertRaises(ValueError):
            self.account.withdraw(800)

        with self.assertRaises(ValueError):
            self.account.withdraw(-100)

    def test_buy_shares(self):
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.balance, 700.0 - 300.0)  # 150 * 2 = 300
        self.assertEqual(self.account.holdings["AAPL"], 2)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['action'], 'buy')

        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -1)

        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 10)  # Insufficient funds

    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 2)
        self.account.sell_shares("AAPL", 1)
        self.assertEqual(self.account.balance, 700.0 - 150.0)  # 150 * 1 = 150
        self.assertEqual(self.account.holdings["AAPL"], 1)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['action'], 'sell')

        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 2)  # Insufficient shares

        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", -1)

    def test_get_portfolio_value(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 2)
        self.account.buy_shares("TSLA", 1)
        expected_value = (1000.0 - 300.0 - 700.0) + 300.0 + 700.0  # Deposits and share values
        self.assertEqual(self.account.get_portfolio_value(), expected_value)

    def test_get_profit_or_loss(self):
        self.account.deposit(1000.0)
        self.account.buy_shares("AAPL", 2)
        self.assertAlmostEqual(self.account.get_profit_or_loss(), 0.0)

        self.account.buy_shares("TSLA", 1)
        self.assertNotEqual(self.account.get_profit_or_loss(), 0.0)

    def test_get_holdings(self):
        self.account.buy_shares("AAPL", 3)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings["AAPL"], 3)
        self.assertEqual(len(holdings), 1)

    def test_get_transaction_history(self):
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 2)

if __name__ == '__main__':
    unittest.main()