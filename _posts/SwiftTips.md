---
title: SwiftTips
copyright: true
date: 2018-02-09 10:56:30
tags:
    - Swift
    - iOS
category: [Swift]
password:
top: 100
---

**本篇文章记录Swift学习使用中的一些知识点**

## 1. String.count vs NSString.length

```swift
let str = "Dog‼🐶"
let nstr: NSString = "Dog‼🐶"
print("count in String: \(str.count), count in NSString: \(nstr.length)")
//"count in String: 5, count in NSString: 6"
```

刚接触Swift的String的时候肯定会对上面的输出结果产生疑问：为啥一个是5，一个是6？这肯定是Swift和Objective-c的字符编码不同的原因。我们先复习一下字符编码。

>- **ASCII码**：这个是上个世纪60年代老美定的一套字符编码，只需要一个字节，可以从00000000表示到11111111，一共可以表示2^8=256个字符。

>- **Unicode**：ASCII码最多只能表示256个字符，英文是够了，但是对于中文以及别的语言是完全不够用的，因此中国创造了GB231编码,用2个字节表示。其他国家也可能会创造别的编码，这样新的问题又出现了:同样的编码值可能对应的是不同的文字，因此需要一种统一的编码来包含世界上所有的文字：Unicode.Unicode是世界上所有符号的集合，目前已经很大很大了。

>- **UTF-8**: Unicode编码有一个很大的弊端，因为他所有的字符占有的位数是一样的，比如汉字严的 Unicode 是十六进制数4E25，转换成二进制数足足有15位（100111000100101），也就是说，这个符号的表示至少需要2个字节。表示其他更大的符号，可能需要3个字节或者4个字节，甚至更多，而英文字母其实只需要一个字节就可以表示，因此会造成极大的浪费。变长的字符编码UTF-8就是这么实现的，UTF-8是Unicode的一种实现方式。    
UTF-8实现方式很简单，遵守两条规则：
1）对于单字节的符号，字节的第一位设为0，后面7位为这个符号的 Unicode 码。因此对于英语字母，UTF-8 编码和 ASCII 码是相同的。
2）对于n字节的符号（n > 1），第一个字节的前n位都设为1，第n + 1位设为0，后面字节的前两位一律设为10。剩下的没有提及的二进制位，全部为这个符号的 Unicode 码。

NSString是基于UTF-16的，也就是说NSString每个字符最大的位数是16位，称为一个**码元**,当我们执行[NSString length]的时候返回的是码元的个数而不是字符的个数。而Swift里的String，他是Unicode-21位的。对于一个emoji来说它的Unicode的位数是大于16位而小于21位的，因此一个emoji在String里的长度是1，而在NSString里是2。

*关于Unicode与NSString的关系推荐一篇[文章](https://objccn.io/issue-9-1/) (需要翻墙)*

## 2. Closures

Clouser用法大致思路上和的Block相似，但是细节上有很多不同的地方，Clouser有一些黑魔法，会让代码变得更简单更易读。
首先用内置函数 *sorted(by:)* 来介绍一下Closure的多种写法：

- 最复杂的写法

```swift
var array = [1, 2, 3, 4, 5]
ar result = array.sorted { (a1, a2) -> Bool in
    return a1 > a2
```

- 如果参数以及返回值类型是可以推断出来的，可以省略掉参数的括号和返回值

```swift
result = array.sorted(by: { a1, a2 in
    return a1 > a2
})
```

- 如果一个closure里只有一行代码，那连关键字**return**都可以省略

```swift
result = array.sorted(by: { a1, a2 in a1 > a2 })
```

- 我们再来简化一下参数名字，swift可以使用 $0,$1,$2... 来代替相应位置的参数的

```swift
result = array.sorted(by: { $0 > $1 })
```

- Trailing Closures，顾名思义就是函数的最后一个参数是closure，成为**尾部闭包**，可省略参数名来简略写法

```swift
func trailingClosure(arg: String, closure:(_ name: String) -> Void) {
    closure(arg)
}

trailingClosure(arg: "lps") { (name) in    //省略了参数 closure
    print("hello \(name)")
}
```

如果只有一个参数且参数是closure，括号也可省略

```swift
reversedNames = names.sorted { $0 > $1 }
```

closure这么多写法我们要敢于多用多尝试，一开始肯定看得有点别扭，但是用多了不知不觉就会写出漂亮的语法。
我们继续来看几个Closure的关键词

- **Escaping Closure**

```swift
func trailingClosure(arg: String, closure:(_ name: String) -> Void) {
    closure(arg)
}

trailingClosure(arg: "lps") { (name) in    //省略了参数 closure
    print("hello \(name)")
}
```

上述例子上我们发现闭包：closure会在函数里立即被调用。但是有些情况闭包在函数return之前都不会调用的，这叫做**闭包逃逸**，必须加入关键词 @escaping 来修饰。比如下面这个例子

```swift
var closureList = [(String) -> Void]()
func trailingClosure(arg: String, closure: @escaping  (_ name: String) -> Void) {    //如果不加关键词 @escaping 编译器会报错
    closureList.append(closure)
}

trailingClosure(arg: "lps") { (name) in    //省略了参数 closure
    print("hello \(name)")
}

closureList.first?("lps")
```

- **Autoclosure** 通过下面的例子很容易理解

```swift

//not autoclosure
func autoClosure(closure: () -> Bool) {
    if closure() {
        print("true")
    } else {
        print("false")
    }
}

autoClosure(closure: ({return true}))

//autoclosure
func autoClosure(closure: @autoclosure () -> Bool) {
    if closure() {
        print("true")
    } else {
        print("false")
    }
}

autoClosure(closure: true))   //因为添加了autoclosure，所以会编译器会自动将该段代码变成 autoClosure(closure: ({return true}))
```

注意Autoclosure只适合无参数的closure () -> T，而且closure的实现只有一行。

*深入了解Block的原理，推荐一本书[Objective-C高级编程](https://book.douban.com/subject/24720270/)*
