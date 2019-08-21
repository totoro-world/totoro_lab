p = 0.6 # 盈利概率
rW = 0.2 # 盈利率
q = 0.2 # 亏损概率
rL = 0.1 # 亏损率
f = (p * rW - q * rL) / rW * rL
print(f)
