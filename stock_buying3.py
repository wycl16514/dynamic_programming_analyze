profit_table = {}
HAVE_STOCK = 1
CLEAR_STOCK = 2

TX_LIMIT = 20 #卖出最多不能超过20次

def  max_profit_by_status(day, status, count ,price_list): #我们需要多考虑一个变量就是卖出次数，对应count
    if count < 0:
        return -float('inf')

    if day == 0:
        if status is CLEAR_STOCK:
            profit_table[(0, CLEAR_STOCK, 0)] = 0
        else:
            profit_table[(0, HAVE_STOCK, 0)] = -price_list[0]
        for i in range(1, count+1):  #在只有一天时，只能买入不能卖出，所以对应卖出次数的收益都是无穷小
            profit_table[(0, HAVE_STOCK, i)] = -float('inf')
            profit_table[(0, CLEAR_STOCK, i)] = -float('inf')
        return profit_table[(0, status, count)]

    if (day, status, count) in profit_table: #查找给定天数，给定状态和给定卖出次数下的最大收益
        return profit_table[(day, status, count)]

    '''
    第n天买入股票对应收益
    '''
    profit1 = max_profit_by_status(day - 1, CLEAR_STOCK, count, price_list)
    profit1 -= price_list[day]
    profit2 = max_profit_by_status(day - 1, HAVE_STOCK, count, price_list)
    max_profit_buying = max(profit2, profit1)
    profit_table[(day, status, count)] = max_profit_buying #记录给定情况的最大收益

    '''
    第n天不持有股票对应收益，注意如果我们在第n天卖出，那么前n-1天就只能少卖出一次
    '''
    profit1 = max_profit_by_status(day - 1, HAVE_STOCK, count - 1, price_list)
    profit1 += price_list[day]
    profit2 = max_profit_by_status(day - 1, CLEAR_STOCK, count, price_list)
    max_profit_clear = max(profit1, profit2)
    profit_table[(day, CLEAR_STOCK, count)] = max_profit_clear

    return profit_table[(day, status, count)] #记录给定情况的最大收益

price_list = [199, 193, 201, 172, 159, 106, 42, 70, 118, 209, 202, 108, 189,
              162, 283, 5, 123, 43, 127, 128, 105, 90, 91, 225, 192, 37, 251, 77, 195, 64, 7, 289,
              24, 59, 84, 110, 48, 88, 248, 174, 131, 258, 244, 58, 50, 169,
              217, 160, 41, 95, 283, 200, 149, 249, 106, 116, 174, 47, 159, 21, 119, 105, 42, 56]


profits = []
for i in range(TX_LIMIT + 1):  #计算给定卖出次数下最佳收益
    profit = max_profit_by_status(len(price_list) - 1, CLEAR_STOCK, i, price_list)
    profits.append(profit)


print(profits)





