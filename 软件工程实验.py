#!/usr/bin/env python
# coding: utf-8

# In[1]:


#读取idkp1-10.txt数据集
file = open(r"C:\Users\Administrator\OneDrive\桌面\ruanjian\idkp1-10.txt",mode='r')
content = file.read()
content = content.split("\n")
content 


# In[2]:


content = [i for i in content if(len(str(i))!=0)] #去除content中的空元素
content = content[1:-1] #去除new_content中的首尾元素
content


# In[3]:


#函数fun1将一个长度为n的列表划分 ，每个子列表中包含m个元素
def fun1(one_list,m=6):  
    return [one_list[i:i+m] for i in range(len(one_list)) if i%m==0]
content=fun1(content,m=6)
content


# In[4]:


#将二维列表转换为DataFrame
import pandas as pd
df = pd.DataFrame(content)
df


# In[5]:


IDKP1 = df.loc[1,1] #获取第1行第1列的值,此时是str类型
IDKP1 = IDKP1.split(" ")#以空格为分隔符，分割这句话
print(IDKP1)
#从中准备提取出物品总数
amount = str(IDKP1[3])
amount = amount.split("d=3*")
amount = str(amount[1])
amount = amount.split(",")
amount = [i for i in amount if(len(str(i))!=0)] #去除amount中的空元素
amount = 3*int(amount[0])
print(amount)
#从中准备提取出背包容量
cubage = IDKP1[-1].split(".")
cubage = [i for i in cubage if(len(str(i))!=0)] #去除cubage中的空元素
cubage = int(cubage[0])
print(cubage)

profit = df.loc[1,3] #获取第1行第3列的profit的值,此时是str类型
profit = profit.split(",") #将由逗号分隔的几个值的序列（str类型）转化为列表
profit = profit[0:-1] #去掉最后一个列表项
print(profit)
weight = df.loc[1,5] #获取第1行第5列的weight的值,此时是str类型
weight = weight.split(",") #将由逗号分隔的几个值的序列（str类型）转化为列表
weight = weight[0:-1] #去掉最后一个列表项
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
plt.title('IDKP9 重量与价值')
#显示网格
plt.grid(True)
#显示图形
plt.show()


# In[ ]:





# In[8]:


profit_list=fun1(profit_int,m=3)#调用fun1将列表项三项为一项
profit_list
weight_list=fun1(weight_int,m=3)
weight_list


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


import time

def backpack(number, weight, w, v):
    #初始化二维数组，用于记录背包中个数为i，重量为j时能获得的最大价值
    result = [[0 for i in range(weight+1)] for i in range(number+1)]
    #循环将数组进行填充
    for i in range(1, number+1):
        for j in range(1, weight+1):
            if j < w[i-1]:
                result[i][j] = result[i-1][j]
            else:
                result[i][j] = max(result[i-1][j], result[i-1][j-w[i-1]] + v[i-1])
    return result


def main():
    number = amount
    weight = cubage
    w = weight_int
    v = profit_int
    start = time.time()
    result = backpack(number, weight, w, v)
    end = time.time()
    print("共耗时:\n" + str(end - start) + " s")
    print("最优解为：" + str(result[number][weight]) + "\n")
    print("所选取的物品为：")
    item = [0 for i in range(number+1)]
    j = weight
    for i in range(1, number+1):
        if result[i][j] > result[i-1][j]:
            item[i-1] = 1
            j -= w[i-1]
    for i in range(number):
        if item[i] == 1:
            print("第" + str(i+1) + "件")
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




