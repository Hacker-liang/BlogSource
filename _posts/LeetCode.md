---
title: LeetCode(Easy)
copyright: true
date: 2018-02-05 20:23:09
tags:
    - LeetCode
category: [LeetCode]
password:
top: 100
---
## 1.Hamming Distance

[LeetCode](https://leetcode.com/problems/hamming-distance/description/)

>两个字符串的 **[汉明距离](https://zh.wikipedia.org/wiki/%E6%B1%89%E6%98%8E%E8%B7%9D%E7%A6%BB)** 是指对应位置不同字符的个数，如 "abc" "cbd",第一位和第三位字符不一样，因此汉明距离为2。

```python
def hammingDistance(x, y):
    return bin(x ^ y).count('1')

hammingDistance(x:1, y:4) => (001 ^ 100) = '101'.count('1') = 2
```

## 2.Jewels and Stones

[LeetCode](https://leetcode.com/problems/jewels-and-stones/description/)

>You're given strings J representing the types of stones that are jewels, and S representing the stones you have.  Each character in S is a type of stone you have.  You want to know how many of the stones you have are also jewels.
The letters in J are guaranteed distinct, and all characters in J and S are letters. Letters are case sensitive, so "a" is considered a different type of stone from "A".
>J字符串里的每个字符是宝石，S字符串里的每个字符是石头，在S里找到J包含的字符。J字符是唯一的，S是可重复的。

```python
def findJewelsInStones(J, S):
    return sum(map(S.count, J))
```

## 3.Single Number

[LeetCode](https://leetcode.com/problems/single-number/description/)

>Given an array of integers, every element appears twice except for one. Find that single one.
Note:
Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

>一个数组里只有一个数字只出现过一次，其它都出现了两次，找到这个单身狗。要求:***空间复杂度0，时间复杂度O(n)**

先贴一个我写的，有个问题，调用 ***sort()*** 函数本来就不是O(n)了。
 ```python
def singleNumber(nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        count = 0
        nums.sort()
        for i, value in enumerate(nums):
            if i%2 == 0:
                count += value
            else:
                count -= value
        return count
 ```

通过利用逻辑运算符***XOR（异或）***的可交换性，可以得到最优的方法。

``` python
def singleNumber(nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result = 0
        for value in nums:
            result ^= value
        return result

singleNumber([1,2,3,3,2]) = (1^2^3^3^2) = (2^2^3^3^1) = (0^0^1) = 1
```

## 4.Rerverse String

[LeetCode](https://leetcode.com/problems/reverse-string/description/)

>Write a function that takes a string as input and returns the string reversed.
Example:
Given s = "hello", return "olleh".

翻转字符串，有很多很简单的实现方式，因为str也可以看做一个list，可利用python list的**切片**特性来实现。

```python
def reverseString(s):
    retrun s[::-1]
```

说到切片，在这里回顾一下python list的切片知识

```python
numbers = [0,1,2,3,4,5,6,7,8,9]
# 取倒数第一个元素
numbers[:-1] = [9]
# index从0到2
numbers[:3] = [0,1,2]
# index从1到2
numbers[1:3] = [1,2]
# 每两个元素取一个
numbers[::2] = [0, 2, 4, 6, 8]
# 倒序
numbers[::-1] = [9,8,7,6,5,4,3,2,1,0]
```

## 5.Judge Route Circle

[LeetCode](https://leetcode.com/problems/judge-route-circle/description/)

>Initially, there is a Robot at position (0, 0). Given a sequence of its moves, judge if this robot makes a circle, which means it moves back to the original place.
The move sequence is represented by a string. And each move is represent by a character. The valid robot moves are R (Right), L (Left), U (Up) and D (down). The output should be true or false representing whether the robot makes a circle.

这个问题很简单，遇到"L"横坐标-1，遇到"R"横坐标+1，遇到"D"纵坐标+1，遇到"U"纵坐标-1，遍历string，一顿操作后x=0，y=0既可。python一句话实现

```python
def judgeCircle(self, moves):
     return moves.count("D")==moves.count("U") and moves.count("L")==moves.count("R")
```

## 6.Self Dividing Numbers

[LeetCode](https://leetcode.com/problems/self-dividing-numbers/description/)

>A self-dividing number is a number that is divisible by every digit it contains.
For example, 128 is a self-dividing number because 128 % 1 == 0, 128 % 2 == 0, and 128 % 8 == 0.
Also, a self-dividing number is not allowed to contain the digit zero.
Given a lower and upper number bound, output a list of every possible self dividing number, including the bounds if possible.
>>Example 1:
Input: 
left = 1, right = 22
Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]
Note:
The boundaries of each input argument are 1 <= left <= right <= 10000.


判断一个数字能不能被自身所有位数整除（0算不能），最简单的办法就是for循环，利用python的函数式编程可简化实现方式。

```python
def selfDividingNumbers(self, left, right):
    isDividing = lambda num: '0' not in str(num) and all([num % int(digit)==0 for digit in str(num)])
    return filter(isDividing, range(left, right))
```
