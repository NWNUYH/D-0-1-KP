#!/usr/bin/env python
# coding: utf-8

# In[1]:


#读取idkp1-10.txt数据集
file = open(r"C:\Users\Administrator\OneDrive\桌面\ruanjian\idkp1-10.txt",mode='r')
content = file.read()
content = content.split("\n")#去除content中的换行符
content 


# In[2]:


#函数fun1去除列表one_list中的空项
def fun1(one_list): 
    return [i for i in one_list if(len(str(i))!=0)]

#调用fun1去除列表content中的空项
content = fun1(content)

#去除new_content中的首尾元素
content = content[1:-1]
content


# In[3]:


#函数fun2将一个长度为n的一维列表划分 ，每个子列表中包含m个元素
def fun2(one_list,m=6):  
    return [one_list[i:i+m] for i in range(len(one_list)) if i%m==0]

#调用fun2将数据分块
content=fun2(content,m=6)
content


# In[4]:


#将二维列表转换为DataFrame
import pandas as pd
df = pd.DataFrame(content)
df


# In[5]:


#获取第2行第1列的值,此时是str类型
IDKP = df.loc[0,1]

#将遇到的所有符号替换为空格
IDKP = IDKP.replace(","," ")
IDKP = IDKP.replace("."," ")
IDKP = IDKP.replace("="," ")
IDKP = IDKP.replace("*"," ")

#用空格分隔这句话
IDKP = IDKP.split(" ")

#调用fun1去除列表IDKP中的空项
IDKP = fun1(IDKP)
print(IDKP)

#从中准备提取出物品总数
amount = int(IDKP[4])*int(IDKP[5])
print("物品总数:" + str(amount))

#从中准备提取出背包容量
cubage = int(IDKP[-1])
print("背包容量:" + str(cubage))

#提取出profit值
#获取第2行第3列的profit的值,此时是str类型
profit = df.loc[0,3]

#将遇到的所有符号替换为空格
profit = profit.replace(","," ")
profit = profit.replace("."," ")

#将由空格分隔的几个值的序列（str类型）转化为列表
profit = profit.split(" ") 

#调用fun1去除列表profit中的空项
profit = fun1(profit)
print(profit)

#提取出weight值
#获取第2行第5列的weight的值,此时是str类型
weight = df.loc[0,5]

#将遇到的所有符号替换为空格
weight = weight.replace(","," ")
weight = weight.replace("."," ")

#将由空格分隔的几个值的序列（str类型）转化为列表
weight = weight.split(" ") 

#调用fun1去除列表weight中的空项
weight = fun1(weight)
print(weight)


# In[6]:


#将列表元素profit,weight类型由object转换为int64
profit_int = list(map(int, profit)) #profit = [int(i) for i in profit]同
print(profit_int)
weight_int = list(map(int, weight)) #weight = [int(i) for i in weight]同
print(weight_int)


# In[7]:


#将两个列表合并为dataframe类型，便于绘制散点图
profit_weight = pd.DataFrame(profit_int, columns=['profit']) #List转DataFrame
profit_weight = pd.concat([profit_weight, pd.DataFrame(weight_int,columns=['weight'])],axis=1)#多个List合并成一个DataFrame
#导入可视化包,绘制散点图
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False  
profit_weight.plot(x='weight',y='profit',kind='scatter')
#x坐标轴文本
plt.xlabel('重量')
#y坐标轴文本
plt.ylabel('价值')
#图片标题
plt.title('重量与价值散点图')
#显示网格
plt.grid(True)
#显示图形
plt.show()


# In[8]:


#调用fun2将列表项三项为一项子列表项
profit_list=fun2(profit_int,m=3)
print(profit_list)
weight_list=fun2(weight_int,m=3)
print(weight_list)


# In[9]:


#将二维列表profit_list转换为DataFrame
profit_df = pd.DataFrame(profit_list)

#将二维列表weight_list转换为DataFrame
weight_df = pd.DataFrame(weight_list)

#将两个dataframe合并为一个dataframe
profit_weight_df = pd.concat([profit_df,weight_df],axis=1)
profit_weight_df.columns=['first_profit','scecond_profit','third_profit','first_weight','scecond_weight','third_weight']
profit_weight_df


# In[10]:


#计算项集第三项的价值:重量比
third_profit_weight = profit_weight_df["third_profit"]/profit_weight_df["third_weight"]

#将第三项的价值:重量比插入dataframe
profit_weight_df.insert(6,"third_profit_weight",third_profit_weight)

#非递增排序
profit_weight_df.sort_values(by = ['third_profit_weight'],ascending = False)


# In[11]:


#动态规划法
import time
def backpack(n, c, w, v):
    #初始化二维数组，用于记录背包中个数为i，重量为j时能获得的最大价值
    result = [[0 for i in range(c+1)] for i in range(n+1)]
    #循环将数组进行填充
    for i in range(1, n+1):
        for j in range(1, c+1):
            if j < w[i-1]:
                result[i][j] = result[i-1][j]
            else:
                result[i][j] = max(result[i-1][j], result[i-1][j-w[i-1]] + v[i-1])
    return result

if __name__ == '__main__':
    start = time.time()
    result = backpack(amount, cubage, weight_int, profit_int)
    end = time.time()
    print("最优解为：" + str(result[amount][cubage]) + "\n")
    print("共耗时:" + str(end - start) + " s")
    file = open(r"C:\Users\Administrator\OneDrive\桌面\ruanjian\Dynamic_KnapSack_output.txt",mode='w')
    file = file.write("最优解为：" + str(result[amount][cubage]) + "\n" + "共耗时:" + str(end - start) + " s")


# In[12]:


#回溯法
import time
bestV=0
curW=0
curV=0
def backtrack(i):
    global bestV,curW,curV
    if i>=n:
        if bestV<curV:
            bestV=curV
    else:
        if curW+w[i]<=c:
            curW+=w[i]
            curV+=v[i]
            backtrack(i+1)
            curW-=w[i]
            curV-=v[i]
        backtrack(i+1)
        
if __name__ == '__main__':
    start = time.time()
    n = amount
    c = cubage
    w = weight_int
    v = profit_int
    start = time.time()
    backtrack(0)
    end = time.time()
    print("最优解为：" + str(bestV)+ "\n")
    print("共耗时:" + str(end - start) + " s")
    file = open(r"C:\Users\Administrator\OneDrive\桌面\ruanjian\Back_KnapSack_output.txt",mode='w')
    file = file.write("最优解为：" + str(bestV) + "\n" + "共耗时:" + str(end - start) + " s")

