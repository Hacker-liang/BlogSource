---
title: Java Tips
copyright: true
date: 2018-06-22 19:55:39
tags: 
    - Java
category: 
    - Java
password:
top:
---

### 1.Java会确保每个字符串常量只有一个，不会产生多个副本。意思就是只要字符串长得一样，那么所有的变量都引用一块内存，如：
```java
String s0 = “helloworld”
String s1 = “helloworld”
String s2 = “hello” + “world”
s0=s1=s2
```

### 2. break不仅可以跳出本层循环，也可以跳出指定循环，通过java的标识符来实现,如：
```java
public static void main(String[] args) {
    outer:
    for(int i=0; i<5; i++)
    {
        for(int j=5; j>0; j--)
        {
                System.out.println("i=" + i + "j=" + j);
                if (i==j) {
                      break outer;
                 }
        }
    }
}
```

### 3.java实例可以调用static修饰的静态方法/变量。但是不鼓励这么调用

### 4.java，方法中的参数传递都是值传递，也就是方法内部会将传进来的参数copy一份，基础类型没有什么疑问，对于引用类型，是将指针copy一份，但是与外部的指针指向的是同一份内存。

### 5.如果一个子类声明了一个和父类相同名字的实例变量。java会开辟两份存储空间分别存储父类的变量和子类的变量。例如

```java
public class Parent {
    public String name = "hello";
}
public class SubClass extends Parent {
    public String name = "hello world";
}

{
    SubClass c = SubClass()
    System.out.println(c.name); //hello world
    System.out.println(((Parent)c).name); //hello
}
```

### 6.引用变量再编译阶段只能调用其编译时类型所具有的方方法，但运行时却执行运行时类型所具有的方法。所以引用变量只能调用编译时确定的方法。这种情况多放生在多态的时候。但是实例变量和方法并不一样，系统访问编译时所定义的变量。

### 7.final修饰的成员变量必须由程序显示的指定初始值，系统不会进行隐式初始化。指定初始值的地方只能有如下几个：
>1.类变量：必须在静态初始化块中指定或者在声明该变量的时候指定，并且只能在其中一处指定。
>2.实例变量：必须在静态初始化块中指定或者在声明该变量的时候指定，或者在构造方法里指定。三处只能选其一。

```java
public static void main(String[] args)
{
    final int a = 5;
    System.out.println(a);
}
```
>你知道吗，上面程序的a，其实压根不存在。final一个重要用途就是“宏变量”，当final变量在定义的时候就指定了值，那么这个final变量就是一个“宏变量”，编译器会把程序中所有用到该变量的地方直接替换成该变量的值。很聪明不是么

### 8. 接口和抽象类
>共性：
>1. 接口和抽象类都不能被实例化，都位于继承树的顶端，用于被其他类实现和继承
>2. 接口和抽象类都可以包含抽象方法，实现接口和子类都必须实现这些抽象方法

>异性：
>1. 接口提现的是一种规范，接口规定了实现者必须向外提供哪些服务。接口更像一个通信协议。
>2. 抽象类更像是一个模板，告诉子类你该按照爸爸的样子来长，别长歪了。

>具体细节方面的不同：
>1. 接口只能包含抽象方法和默认方法，抽象类可以包含普通方法（带有花括号实现体）。
>2. 接口只能定义静态常量，抽象类可以定义普通变量
>3. 接口不能包含构造器，抽象类可以包含构造器，但是其并不用于创建对象，而是让其子类调用这些构造器来完成抽象类的初始化工作。
>4. 一个类可以实现多个接口，但是只能继承一个抽象类 

### 9. GC内存回收

>对象在内存中分为以下三种状态：
>1. 可达状态：一个对象被初始化并被一个或一个以上变量引用的时候，称为可达状态。
>2. 可恢复状态：一个对象不再有变量引用的时候称为可恢复状态，当GC回收该对象并调用该对象finalize()的时候，该对象可通过添加引用来变成可达状态，反之则变为不可达状态。
>3. 不可达状态：当GC已经调用了该对象的finalize()方法，该对象仍然没有变为可达状态，此对象会被回收。

>finalize() 方法调用有如下4个特点
>1. 永远不要主动调用对象的finalize()方法，该方法由GC来调用
>2. finalize()何时被调用具有很强的不确定性，所以不要在此方法里做一些必须的清理工作
>3. finalize()调用时可以通过重新设置引用变量来使该对象重新变为可达状态
>4. finalize()调用时抛出异常，GC并不会报告异常，程序继续执行

### 10. java引用

>1. 强引用
>>java中最常见的引用方式，程序创建一个对象，并把这个对象赋给一个引用变量，通过变量来访问操作实际的对象，当对象被一个或多个变量强引用的时候，对象处于可达状态。
>2. 软引用
>>软引用通过SoftReference类来实现，当一个对象只有软引用时候，它有可能被GC回收，但只有在系统内存空间不足的时候才会回收。软引用常用于内存敏感的程序中。
>3. 弱引用
>>弱引用通过WeakReference类来实现，当一个对象只有弱引用是，无论内存是否充足，都有可能被GC回收。
>4. 虚引用
>>虚引用通过PhantomReference类来实现，虚引用完全类似于没有引用，虚引用对对象没有太大影响，虚引用不能单独使用，必须和引用队列联合使用。

```java
#虚引用使用
public class TestPhantomReference {
    public static void main(String[] args) {
        String str = "Hello PhantomReference";
        ReferenceQueue queue = ReferenceQueue();
        PhantomReference pr = new PhantomReference<T>(str, queue);
        str = null;
        System.out.print(pr.get());      // 输出null
        System.gc();
        System.runFinalization();
        System.out.print(queue.poll() == pr);   // 输出 true
    }
}

```