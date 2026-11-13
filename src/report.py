import duckdb

result = duckdb.query("""
    SELECT transaction_type, COUNT(*) AS total
    FROM 'outputs/transactions.parquet'
    GROUP BY transaction_type
""").df()

print(result)

total_amount = duckdb.query("""
    SELECT SUM(amount) AS total_amount
    FROM 'outputs/transactions.parquet'
""").df()

print("\nTotal transaction amount:")
print(total_amount)

highest = duckdb.query("""
    SELECT MAX(amount) AS highest_amount
    FROM 'outputs/transactions.parquet'
""").df()

print("\nHighest transaction amount:")
print(highest)

lowest = duckdb.query("""
    SELECT MIN(amount) AS lowest_amount
    FROM 'outputs/transactions.parquet'
""").df()

print("\nLowest transaction amount:")
print(lowest)

average = duckdb.query("""
    SELECT AVG(amount) AS average_amount
    FROM 'outputs/transactions.parquet'
""").df()

print("\nAverage transaction amount:")
print(average)