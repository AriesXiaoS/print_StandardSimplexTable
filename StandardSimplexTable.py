# -*- coding: utf-8 -*-
"""

%%%%%   解标准单纯形表并打印每一步   %%%%%

！！！请勿使用Python自带IED，请使用第三方编译器，推荐Anaconda-Spider

标准单纯形：
    max z=CX
    AX=b
    b>0
    
输入标准单纯形表的例子：
--------------------------------------------
C=np.array([[2,3,0,0,0]])
A=np.array([[1,2,1,0,0],
            [4,0,0,1,0],
            [0,4,0,0,1]],dtype=np.float)
b=np.array([[8,16,12]],dtype=np.float)
X_B=[3,4,5]
--------------------------------------------
注！
X_B e.g.  x1,x2,x3 表示为 [1,2,3]

#####
#####
此文件只能当库import使用！
此文件只能当库import使用！
此文件只能当库import使用！
#####
#####
具体用法：
将此文件和需要使用此文件的py脚本放在同一文件夹下

import StandardSimplexTable as sst

sst.solve(C,A,b,X_B)

如有数据格式问题请 help(sst)
"""
import numpy as np   
import copy

def solve(input_C,input_A,input_b,input_X_B):
    global C,A,b,X_B
    C=copy.deepcopy(input_C)
    A=copy.deepcopy(input_A)
    b=copy.deepcopy(input_b)
    X_B=copy.deepcopy(input_X_B)
    _main()

def _init_data():
    global n_x_all,n_x_B,C_B,Sigma,Sita
    n_x_all=len(C[0])
    n_x_B=len(b[0])
    C_B=np.zeros((1,len(X_B)))  
    Sigma=[0 for i in range(n_x_all)]
    Sita=[0 for i in range(len(X_B))]
########################################
def _update_C_B():
    global X_B,C_B,C
    for i in range(len(X_B)):
        C_B[0,i]=C[0,X_B[i]-1]   
################################
def _update_Sigma():
    global A,C_B,Sigma
    for i in range(n_x_all):
        Sigma[i]=(C[0,i]-C_B.dot(A[:,i:i+1]))[0,0]
################################
def _update_Sita():
    """
    xi为换入基变量;
    若换入变量为x1，xi=1
    """
    global A,b,Sita
    xi=_get_x_in()
    P=A[:,xi-1]
    for i in range(len(P)):
        if P[i]>0:
            Sita[i]=round(b[0,i]/P[i],3)
        else:
            Sita[i]=False
    #e.g. Sita=[4.0, False, 3.0]
################################
def _get_x_out():
    global Sita,X_B
    """
    若换出变量为x1，xi=1
    xi=0表示无
    """
    #获得第一个数用于比较
    the_i=-1
    for i in range(len(Sita)):
        if Sita[i]:
            minimum=Sita[i]
            the_i=i
            break
    #找出最小者
    for i in range(len(Sita)):
        if Sita[i]:
            if Sita[i]<=minimum:
                minimum=Sita[i]
                the_i=i
    if the_i==-1:
        return False
    return (X_B[the_i])

def _get_x_in():
    global Sigma
    """
    求最大值，找Sigma最小者
    默认检验数有大于0者
    若返回False 表明所有检验数小于0，已达到最优解
    """
    maximum=0
    the_i=-1
    for i in range(len(Sigma)):
        if Sigma[i]>=maximum:
            maximum=Sigma[i]
            the_i=i
    #if the_i==-1:
    #    return False
    return the_i+1
################################
def _get_main_element():
    """
    获得主元素    求出主元素所在位置(x,y)
    得到主元素A[x,y]
    Sigma 和 Sita 默认已经更新过了
    若返回False 表明已经达到最优解
    """
    global Sigma,Sita,X_B
    y=_get_x_in()-1
    if not _get_x_out():
        x=-1
    else:
        x=X_B.index(_get_x_out())
    return (x,y)
################################
def _optimum():
    """
    判断是否达到最优解
    """
    global Sigma
    for s in Sigma:
        if s>0:
            return False
    return True

def _unbounded():
    """
    判断是否是无界解
    """
    if not _get_x_out():
        return True
    return False
################################
def _update_Ab():
    """
    在确认有最优解时，对A进行操作
    （旋转运算
    """
    global A,b,X_B
    (x,y)=_get_main_element()
    main_element=A[x,y]
    #print(main_element)
    b[0,x]=b[0,x]/main_element
    for j in range(n_x_all):
        A[x,j]=A[x,j]/main_element
    ###
    for i in range(n_x_B):
        #i为行
        a=A[i,y]#原主元素所在列 在此行要消去的元素
        if i!=x:
            b[0,i]=b[0,i]-a*b[0,x]
            for j in range(n_x_all):
                #j为列
                A[i,j]=A[i,j]-a*A[x,j]
        #####
        if X_B[i]==_get_x_out():
            X_B[i]=_get_x_in()
##################################################
##################################################
def _print_one_table():
    """
    自定函数打印单纯形表
    \033[显示方式;字体色;背景色m......[\033[0m]
    \033[1;32;43m test \033[0m
    """
    global C_B,X_B,b,A,Sita,Sigma,n_x_all,n_x_B
    """
    len1:C_B,X_B,b
    len2:A,Sita
    Sigma,n_x_all
    """
    #转换Sita
    the_Sita=[]
    for s in Sita:
        if s==False:
            the_Sita.append('-')
        else:
            the_Sita.append(s)
    ###
    len1=7
    len_X_B=5
    len2=8
    print('='*(2*len1+len_X_B+4+(len2+1)*(n_x_all+1)))
    def _print_line():
        #打印横线
        print('+{0}+{1}+{0}+'.format('-'*len1,'-'*len_X_B),end='')
        for i in range(n_x_all+1):
            print('{}+'.format('-'*len2),end='')
        print('')
    ##########
    #打印第一行：
    print('|{:^21}|'.format('cj'),end='')
    for i in range(n_x_all):
        print('{:^8}|'.format(C[0][i]),end='')
    print('{:^8}|'.format(''))
    _print_line()
    ###########
    #打印第二行：
    print('|{:^7}|{:^5}|{:^7}|'.format('C_B','X_B','b'),end='')
    for i in range(n_x_all):
        print('{:^8}|'.format('x{}'.format(i+1)),end='')
    print('{:^8}|'.format('θ_i'))
    _print_line()
    ######################
    #打印中间元素：
    (x,y)=_get_main_element()
    flag=0
    if _optimum():
        #已达最优解 
        flag=1
    if _unbounded():
        #无界解
        flag=2
    for row in range(n_x_B):
        #一行一行地打印
        print('|{:^7.2f}|{:^5}|{:^7.2f}|'.format(C_B[0][row],'x{}'.format(X_B[row]),b[0][row]),end='')
        for i in range(n_x_all):
            if flag==2 and i==y:
                #无界解时 将Pi列标记
                print('\033[1;30;43m{:^8.3f}\033[0m|'.format(A[row][i]),end='')
            elif flag==0 and y!=-1 and x!=-1 and row==x and i==y:
                #未到最优解时 标记主元素             
                print('\033[1;31;43m{:^8.3f}\033[0m|'.format(A[row][i]),end='')
            else:
                print('{:^8.3f}|'.format(A[row][i]),end='')
        #####
        #打印Sita
        if flag==2:
            #无界解时不打印Sita
            print('{}|'.format(' '*len2))
        elif flag==0:
            #还未到最优解 且不是无界解时 才打印Sita
            print('{:^8}|'.format(the_Sita[row]))
        else:
            #最优解时 最后一张表不打印Sita
            print('{}|'.format(' '*len2))
    _print_line()
    ######################
    #打印Sigma
    print('|{:^21}|'.format('σ_j'),end='')
    for i in range(n_x_all):
        print('{:^8.3f}|'.format(Sigma[i]),end='')
    print('{}|'.format(' '*len2))
    
    print('='*(2*len1+len_X_B
               +4+(len2+1)*(n_x_all+1)))
##################################################
##################################################   
def _get_optimum_x():
    global X_B,b
    final_x=[0 for i in range(n_x_all)]
    for i in range(n_x_B):
        final_x[X_B[i]-1]=b[0][i]
    return final_x

def _one_loop():
    _update_C_B()
    _update_Sigma()
    _update_Sita()
    _print_one_table()
    
    if _optimum():
        print("已经找到最优解!\n最优解为：(",end='')
        final_x=_get_optimum_x()
        for i in range(n_x_all):
            print('x{},'.format(i+1),end='')
        print(')=(',end='')
        for i in range(n_x_all):
            print('{:.3f},'.format(final_x[i]),end='')
        print(')\n目标值为：{}'.format(C.dot(final_x)[0])) 
        return(False,"optimum")
    if _unbounded():
        print("无界解")
        return(False,"unbounded")
        
    print('换入变量为：x{}'.format(_get_x_in()),end='  ')
    print('换出变量为：x{}'.format(_get_x_out()),end='  ')
    (x,y)=_get_main_element()
    main_a=A[x][y]
    print('所以主元素为：A{}即{:.3f}'.format((x+1,y+1),main_a))
    _update_Ab()
    
    return (True,"continue")

def _main():
    _init_data()
    while(1):
        (flag,message)=_one_loop()
        if flag==False:
            break
        
if __name__=='__main__':   
    _main()



