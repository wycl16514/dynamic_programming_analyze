profit_table = {}
HAVE_STOCK = 1  # 持有股票
CLEAR_STOCK = 2 # 没有股票

#计算在给定天数后，在两种状态下的最佳收益
def max_profit_by_status(day, status, price_list):
    if day <= 0:  #首先要确认递归停止的条件
        #当只有一天时，不持有股票所得收益就是0，如果持有股票那么所得收益就是负数，也就是你要花钱买股票
        if status is CLEAR_STOCK:
            return 0
        else:
            return -price_list[0]

    if (day, status) in profit_table:
        #在解决问题前，先查表看看问题是否有了答案
        return profit_table[(day, status)]


    if status == HAVE_STOCK:
        '''
        在第n天持有股票的最大收益取决于第n-1天没有持有股票，然后再第n天买入股票，或者第n-1天持有股票,第n天继续持有，
        然后判断两中情况那种收益更大
        '''
        max_profit_have_stock = max(max_profit_by_status(day - 1, CLEAR_STOCK, price_list) - price_list[day],
                                    max_profit_by_status(day - 1, HAVE_STOCK, price_list))
        #记录最优情况记录
        profit_table[(day, HAVE_STOCK)] = max_profit_have_stock
    else:
        '''
        第n天没有股票的最大收益取决于两种情况，分别是第n-1天持有股票，然后第n天卖出。或者是第n-1天没有股票，然后
        第n天不要买入，看看两种情况那种收益更大
        '''
        max_profit_by_clear_stock = max(max_profit_by_status(day - 1, HAVE_STOCK, price_list) + price_list[day],
                                        max_profit_by_status(day-1, CLEAR_STOCK, price_list))
        # 记录最优情况记录
        profit_table[(day, CLEAR_STOCK)] = max_profit_by_clear_stock
    # 返回给定天数后，在给定状态下的最优回报
    return profit_table[(day, status)]


price_list = [199, 193, 201, 172, 159, 106, 42, 70, 118, 209, 202, 108, 189,
              162, 283, 5, 123, 43, 127, 128, 105, 90, 91, 225, 192, 37, 251, 77, 195, 64, 7, 289,
              24, 59, 84, 110, 48, 88, 248, 174, 131, 258, 244, 58, 50, 169,
              217, 160, 41, 95, 283, 200, 149, 249, 106, 116, 174, 47, 159, 21, 119, 105, 42, 56]

#最后一天能获得最大收益必然是不持有股票的情况
max_profit = max_profit_by_status(len(price_list) - 1, CLEAR_STOCK, price_list)
print(f"max profit is:{max_profit}")


