
def bubbleSort(l):
    for i in range(0, len(l)-1):
        isChanged = False
        for j in range(0, len(l)-1-i):
            if l[j] > l[j+1]:
                value = l[j]
                l[j]=l[j+1]
                l[j+1]=value
                isChanged = True
        if not isChanged:
            print("已经有序了，不需要交换了",l[i])
            break
    print(l)

bubbleSort([1,2,3,4,6,5,8,0,9,10,100,101,3,4,11,12])

def selectSort(l):
    for i in range(0, len(l)-1):
        min = l[i]
        index = i
        for j in range(i, len(l)):
            if min > l[j]:
                min = l[j]
                index = j
        
        value = l[i]
        l[i]=l[index]
        l[index]=value

    print(l)
    
selectSort([1,2,3,4,6,5,8,0,9,10,100,101,3,4,11,12])

def insertSort(l):
    for i in range(1, len(l)):
        temp = l[i]
        insertIndex = 0
        for j in range(i, -1, -1):
            if temp<=l[j]:
                insertIndex = j    #更新插入位置
                if j>1 and temp>=l[j-1]:   #如果已经比前一位大了那就不需要继续往前走了
                    break
        del l[i]                     #进行插入
        l.insert(insertIndex,temp)
    print(l)
insertSort([1,2,3,4,6,5,8,0,9,10,100,101,3,4,11,12])

def shellSort(l):
    step = int(len(l)/2)
    while step >= 1:
        print("当前增量是：", step)
        for i in range(step, len(l)):
            for j in range(i-step, -step, -step):
                if l[j] > l[j+step]:
                    temp = l[j]
                    l[j] = l[j+step]
                    l[j+step] = temp
        step = int(step/2)
    print(l)

shellSort([1,2,3,4,6,5,8,0,9,10,100,101,3,4,11,12])

def quickSort(a, l, r):
    if l < r:
        i = l
        j = r
        x = a[l]    #选取比较基准
        while i < j:
            while(i<j and a[j]>=x):   #从右向左寻找比基准小的元素
                j -= 1
            if i < j:  #说明上面从右往左的寻找找到了比x小的元素
                a[i] = a[j]    #将位置j的元素移动到i上
                i += 1 
            while(i<j and a[i]<x):     #从左向右寻找比x大的元素来填充位置j，因为位置j的元素被填充到位置i上了。
                i += 1
            if i < j:
                a[j] = a[i]
                j -= 1
        a[i] = x   #将基准元素填充到应该填充的位置
        quickSort(a, l, i-1)
        quickSort(a, i+1, r)

s = [1,2,3,4,6,5,8,0,9,10,100,101,3,4,11,12]
quickSort(s, 0, len(s)-1)
print(s)
                        
