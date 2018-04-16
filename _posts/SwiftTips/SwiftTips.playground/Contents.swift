//: Playground - noun: a place where people can play

import UIKit

//var str = "Hello, playground", str1 = "hello world"
//print(str+str1)
//
//var age, height: Int
//age = 10
//height = 11
//var s123ddsf = 10
//
//var i = 10
//var j = 10 + 0.01
//
//var d: Float = 0.01
//var m = Double(d) + j
//
//var i_2 = 0b0101010
//var i_10 = 12314
//var i_8 = 0o12345
//var i_16 = 0x123456
//i = Int(i_16)
//
//var f_8 = 0o123141
//typealias someType = Int
//
//var s: someType = 100
//print(someType.max)
//
//let dd = Int("test")
//let dddd: Int? = 12312312
//
//let ddd = Int(12312)
//
//if var ttt = dddd {
//    print(ttt)
//    ttt = 234234
//    print(ttt)
//}
//
//func throwErrorFunc() throws {
//    print("test throwErrorFunc")
//
//}
//
//do {
//    try throwErrorFunc()
//} catch {
//
//}

let list = [1,2,3,2,3,1,12]
var result = 0
for i in list{
    result ^= i
}
print(result)
print(list[...2])
print(list[2...])

let mutilines = """
                a
                 b
                """
print(mutilines.count)
let str = "한"
for c in str.utf8 {
    print(c)
}

let regionalIndicatorForUS: Character = "\u{1F1F8}"
var hello = "hello world"
hello.insert("t", at: hello.endIndex)
hello.endIndex

hello



