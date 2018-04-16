---
title: LeetCode(Medium)
copyright: true
date: 2018-03-08 18:35:17
tags:
    - LeetCode
category: [LeetCode]
password:
top:
---

## 1. Partition Labels

[LeetCode](https://leetcode.com/problems/partition-labels/description/)

>A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that each letter appears in at most one part, and return a list of integers representing the size of these parts.

>>Example 1:
Input: S = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits S into less parts.

>Note:
S will have length in range [1, 500].
S will consist of lowercase letters ('a' to 'z') only.

切割一个由小写字母组成的字符串S为n个子串，要求每个字符只最多只能出现在一个子串中。例如：
**str = 'abcabdhij'**
我们先从第一个字符'a'开始，要想不重复，肯定需要找到最后一个字符‘a’，其中的字符‘abca’都应该在第一个子串里，我们分析这个子串，发现‘b’的最后一个字符的位置比‘a’更大，所以第一个子串至少是‘abcab’，我们再分析‘c’，发现最后一个‘c’的位置是小于最后一个‘b’的，因此第一个子串应该是‘abcab’，剩下元素同上。

```python
def partitionLabels(S):
    sizes = []
    start = 0     #记录开始位置
    end = 0       #记录已遍历的字符出现的最远位置。
    for i, l in enumerate(S):
        last = S.rfind(l, i+1, len(S))   #找到字符l在S里的最远位置
        if last > end:   #当出现一个更远的字符的时候，更新end
            end = last
        if i == end:     #在S[end:]已无重复，切割字符串
            sizes.append(end-start+1)
            start = end+1
            end = end+1
    return sizes

print(partitionLabels("ababcbacadefegdehijhklij"))   # [9, 7, 8]
```

## 2. Single Element in a Sorted Array

[LeetCode](https://leetcode.com/problems/single-element-in-a-sorted-array/description/)

>Given a sorted array consisting of only integers where every element appears twice except for one element which appears once. Find this single element that appears only once.

>>Example 1:
Input: [1,1,2,3,3,4,4,8,8]
Output: 2

>Note: Your solution should run in O(log n) time and O(1) space.

给定一个有序数组，只有一个元素只出现了一次，其余所有元素会出现两次，要求时间复杂度为log n，因为有序，我们通过二分查找的方法来找到单独的元素。

```python
def singleNonDuplicate(nums):
    if len(nums) == 1: return nums[0]
    mid = int(len(nums)/2)
    i = nums[mid]
    if i!=nums[mid-1] and i!=nums[mid+1]:      #如果中间的元素与左右两个元素都不相等，那么就是要找的那个元素
        return i
    if nums[mid-1]==i:         #如果中间的元素与左边元素相等
        left = nums[0:mid+1]
        if len(left)%2==0:    #如果算上中间元素，一共有2的倍数个元素，说明单独的元素肯定不在左边，递归的在右边剩余的元素里查找。
            return singleNonDuplicate(nums[mid+1:len(nums)])
        else:
            return singleNonDuplicate(left)
    else:
        right = nums[mid:len(nums)]
        if len(right)%2==0:
            return singleNonDuplicate(nums[0:mid])
        else:
            return singleNonDuplicate(right)
number = singleNonDuplicate([3,3,7,7,10,11,11])
```