祝愿各位同学在新一年里身体健康，阖家欢乐。根据过往几十年的观察和经验发现，单单恭喜无法令人发财，我们只有成功找到好的工作，赢得一份称心的事业，发财才有机会，能够进入好的企业自然是实现自身财富提升的合理方式，前不久听闻腾讯除了年终至少三个月外，”阳光普照“奖都能是100股，折合人民币有三万多，所以解决大厂面试题，某得一个大厂正式职位应该是普通人实现财富较快积累的好方式吧。

对大厂技术岗而言，面试考算法往往避不开，而动态规划问题是一道较难跨越的门槛，因此为了美好的钱程，我们有必要下功夫搞定。上一节我们讲了一道我遇到的动态规划算法题，我以为是个例，后来经过调查发现相应题目经常出现，同时上次描述比较粗糙，同时解法有问题，这次我打算通过慢慢拆解来进一步阐述动态规划问题的处理方法。

当算法题要求你给出”最优“，”最佳“，”最多“，”最少“等字眼时，十有八九就是动态规划，它的处理通常有固定的步骤如下：
1，如果问题的规模为n, 那么把问题拆解成n-1 和最后一个元素，分析前n-1个元素在各个不同状态下对应的最优解，然后再结合最后一个元素寻求整体最优解。
2，解决动态规划问题肯定要考虑列表来记录信息，要不然时间复杂度会变成指数级。
3，在第一部将问题拆解成n-1后，往往需要递归的将问题同样拆解成n-2，在递归求解时需要先查表看看问题是否已经有了答案。
4，注意在递归过程中处理边界问题。

我们还是拿上次的股票买卖问题进行解析。给定一只股票在未来一段时期内价格变化，如果投资者预算上没有限制，也就是无论股票价格多高他都买得起，但要求每次他最多只能持有一股，他只能在没有持有股票的情况下购买，请设计最优投资策略使得股票买卖利润最大化，，例如[2,5,1]是三天内的变化，那么最优策略是第一天2块钱买，第二天5块钱卖，例如最大为3块。如果股票价格变化为[2,5,1,3]，那就是第一天买，第二天卖，然后第3天买，第4天卖，于是利润为5 = 3 + 2 。

我们看看前面提到的结题步骤如何应用，我们就以[2,5,1,3]为例，首先将其拆解成n-1和最后一个元素，那就是[2,5,1] 和 3，于是我们先看当股票变化为[2,5,1]时，它在不同状态下的最优解。所谓”不同状态“就是最后一天到底是持有股票，还是没有股票，于是我们先找到股票价格为[2,5,1]时最后一天持有股票时的最佳利润和不持有股票时的最佳利润。

如果[2,51]时最后一天持有股票，那么[2,5,1,3]时对应的最优收入就是在最后一天以3块卖掉股票。如果[2,5,1]时最后一天没有股票，那么[2,5,1,3]时最后一天就什么都不要做，然后我们比较两种情况，哪一种收益最大。

于是在计算[2,5,1]情况时，我们又能将其分解为[2,5]和1，依然以同样的逻辑去处理。接下来我们要看第二步，也就是用表来记录信息，这里我们要记录的是在n天结束后，最后一天状态分别为持有股票和没有股票的最佳收益。例如前面我们需要解决[2,5,1]时，最后一天持有股票和没有股票的最大收益，如果此时表里面记录了这些信息，我们直接查表就能获取，这样就省掉了后续继续求解的时间。同理问题规模为[2,5,1]时，如果我们能通过查表获得两天后持有股票和没有股票的最大收益，那么我们就能很快的解决问题，因此这里对应的是第3步。

由于问题不断递归，因此我们必然要让递归有个停止的地方，当问题规模足够小能够直接给出答案时就是问题应该停止的地方，在本例中当只有一天时，有就是问题规模为[2]时我们可以直接给出答案因此在这里要停止递归，接下来我们看看实现代码:
```
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
```
同学们可以结合代码来体会一下前面说道的处理步骤。通常在面试过程中，面试官一般会准备多个后手，也就是你解决了第一个问题后，他很可能会把条件变换一下，增加难度后让你继续求解，假设我们在原问题上增加一个约束条件，那就是投资者有预算，当股票价格高于其手中资金时他就不能购买。增加了这个条件后，上面在购买股票的步骤就必须要进行相应判断，如果条件不满足就不能执行。

同时我们在步骤1分解问题时，有些情况可能达不到，例如考虑n-1天后持有股票的情况，投资者肯定要在n-1天内购买股票，如果资金不足时购买股票后收益就是负值，这种情形我们要排除掉，于是综合起来考虑，代码实现如下：
```
profit_table = {}
HAVE_STOCK = 1
CLEAR_STOCK = 2

SAVING = 100

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
```
最后一种变种也是最复杂的一种情况，那就是限制卖出的次数，例如限制投资者卖出次数不超过10次。在这种情形下，问题的状态多出了一个变量，原来问题状态在于最后一天是持有股票还是不持有，现在多出一个变量就是卖出次数，于是我们要考虑最后一天持有股票，然后卖出池为1次，2次。。。10次，同时还要考虑最后一天没有股票，然后卖出次数分别为1次，2次。。。10次等这些情况，于是要考虑的状态从2中变成了20种，相应代码实现如下：
```
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
```
上面给定代码的运行结果如下：
```
[0, 284, 543, 787, 1028, 1245, 1433, 1600, 1718, 1835, 1947, 2048, 2148, 2246, 2326, 2394, 2456, 2494, 2521, 2535, 2543]
```
代码运行结果值得我们分析一下，当允许卖出的次数为0次时，最好的收益当然就是0，因为只买不买就必然亏本。当只运行卖出一次时，算法在股价最低处也就是5块钱是买入，在最高处也就是289时卖出，于是收益就是284，这一点比较容易检验。根据这两个结果，我们可以有信心的认为算法逻辑应该是正确的。

最后我们分析一下算法时间复杂度。前面两种情况，由于每天状态只有2种，给定n天，那么我们需要计算2n种情况，于是复杂度为O(n)，最后一种由于每天有20种状态，因此我们需要计算20n种情况，因此算法复杂度依然为O(n)，同理空间复杂度也可以同样计算。

