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

```java
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
    范围分为非为范围来看；fejwf
}
```
