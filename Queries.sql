-- To get all transactions
select * from Transactions
-- To get all transactions which are successful
select * from Transactions where transaction_result='tesSUCCESS'
-- Get Transactions for a specific currency on a specific day
select account, destination, amount_value, delivered_amount from Transactions where amount_currency='BTC' and transaction_time LIKE '2020-08-01T%'
-- From String to Datetime ( If needed , especially for grouping )
select datetime(transaction_time) from Transactions
-- Get transactions by grouping the hours and for a specific currency ( Change the currency field for the currency you want )
select strftime('%dT%H', transaction_time) as DateHour, SUM(amount_value) as EUR_SUM, COUNT(*) as Tx_count_EUR from Transactions where amount_currency='EUR' group by strftime('%dT%H', transaction_time)
-- Same Grouping , but average transaction value
select strftime('%H', transaction_time) as Hour, AVG(amount_value) as AVG_TX_BTC, COUNT(*) as Tx_count_BTC from Transactions where amount_currency='BTC' group by strftime('%H', transaction_time)
