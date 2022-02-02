profit_table = {}
HAVE_STOCK = 1
CLEAR_STOCK = 2

SAVING = 20

def max_profit_by_status(day, status, price_list):
    if day <= 0:
        if status is CLEAR_STOCK: #在第一天如果不购入股票，投资者资金额度不变
            return SAVING
        else:
            return SAVING - price_list[0]  #如果购入股票需要减去股票的价格，如果字节不足就会变成负值

    if (day, status) in profit_table:  #查表看看是否已经有了答案
        return profit_table[(day, status)]

    '''
    计算持有股票状态下的最大收益，分为两种情况，第n-1天没有股票，然后在第n天购入，注意购入股票可能形成负值，
    第二种情况是在第n-1天是持有股票，注意这时收益依然有可能是负值
    '''
    max_profit_have_stock = 0
    max_profit_have_stock = max(max_profit_by_status(day - 1, CLEAR_STOCK, price_list) - price_list[day],
                                max_profit_by_status(day - 1, HAVE_STOCK, price_list))

    '''
    计算第n天不持有股票的最大收益，分为两种情况，在n-1天时持有股票，在第n天卖出，注意我们要确保n-1天持有股票时收益不能为负数，因为
    因为预算不允许投资者购买价格超过其资金的股票，于是当n-1天持有股票是负值时，我们不能进行卖出，因为这不是合法操作。
    第二种情况是n-1天没有股票，然后第n天什么都不做
    '''
    max_profit_clear_stock = 0
    profit1 = 0
    if max_profit_by_status(day - 1, HAVE_STOCK, price_list) >= 0:
        profit1 = max_profit_by_status(day - 1, HAVE_STOCK, price_list) + price_list[day]
    profit2 = max_profit_by_status(day-1, CLEAR_STOCK, price_list)
    max_profit_clear_stock = max(profit1, profit2)

    if status is HAVE_STOCK:
        profit_table[(day, HAVE_STOCK)] = max_profit_have_stock
    else:
        profit_table[(day, CLEAR_STOCK)] = max_profit_clear_stock

    return profit_table[(day, status)]



price_list = [199, 193, 201, 172, 159, 106, 42, 70, 118, 209, 202, 108, 189,
              162, 283, 5, 123, 43, 127, 128, 105, 90, 91, 225, 192, 37, 251, 77, 195, 64, 7, 289,
              24, 59, 84, 110, 48, 88, 248, 174, 131, 258, 244, 58, 50, 169,
              217, 160, 41, 95, 283, 200, 149, 249, 106, 116, 174, 47, 159, 21, 119, 105, 42, 56]


profit = max_profit_by_status(len(price_list) - 1, CLEAR_STOCK, price_list)
print(f"profit by status:{profit - SAVING}")