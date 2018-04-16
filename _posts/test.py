def selfDividingNumbers(left, right):
    """
    :type left: int
    :type right: int
    :rtype: List[int]
    """
    # resultList = []
    # for i in range(left, right+1):
    #     valid = True
    #     for n in str(i):
    #         if int(n) == 0:
    #             valid = False
    #             break
    #         if i%int(n) != 0 and int(n)!=0:
    #             valid = False
    #             break
    #     if valid:
    #         resultList.append(i)

    # return resultList
    isDividing = lambda num: '0' not in str(num) and all([num % int(digit)==0 for digit in str(num)])
    return filter(isDividing, range(left, right))

print(list(selfDividingNumbers(1,22)))

def testlambdaFunc():
    la = lambda x : x+1
    print(la(100))

testlambdaFunc()

def partitionLabels(S):
    sizes = []
    start = 0
    end = 0
    for i, l in enumerate(S):
        last = S.rfind(l, i+1, len(S))
        if last > 0 and last > end:
            end = last
        if i == end:
            sizes.append(end-start+1)
            start = end+1
            end = end+1
    return sizes

# print(partitionLabels("ababcbacadefegdehijhklij"))

def singleNonDuplicate(nums): 
    if len(nums) == 1: return nums[0]
    mid = int(len(nums)/2)
    i = nums[mid]
    if i!=nums[mid-1] and i!=nums[mid+1]:
        return i
    if nums[mid-1]==i:
        left = nums[0:mid+1]
        if len(left)%2==0:
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
print(number)