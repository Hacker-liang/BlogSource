### 直播机包大小优化

#### 前言
* * *
随着项目的发展，我负责的直播机项目包大小越来越大，虽然只是一个主播用的直播工具，但是功能很多，第三方库也集成了很多，推流库就有两套：RTMP、WebRTC、还集成了播放器，AI... 因为是独立APP，用户相对可控，就没太在意包大小的问题，直到有一天上传iTunes connect的时候，苹果爸爸提醒我们universal包已经超过150M了，作为有点追求的码农，优化也迫在眉睫了。经过努力最终将App包大小控制在了较为合理的范围。下面将优化的心路历程做个记录，首先感谢一下给我提供过帮助的两篇技术文章，感谢！
> [干货|今日头条iOS端安装包大小优化—思路与实践](https://techblog.toutiao.com/2018/06/04/gan-huo-jin-ri-tou-tiao-iosduan-an-zhuang-bao-da-xiao-you-hua-si-lu-yu-shi-jian/)
> [iOS 瘦包常见方式梳理](https://juejin.im/entry/5be3de19f265da6110368954)


#### 基本知识

1. **如何查看我们的包大小**

我们这里说的iOS包主要是 **APP** 文件，每次Archive之后点击Window->Orgnizer会看到我们将要上传的archive文件，右键show in finder然后进入某个archive的Contents里，在Products->Applications里可以找到我们的 **APP** 文件，这个就是我们的优化对象，右键进入Contents就可以看到我们他的内部结构了，下面我们会针对这里面的内容划分出不同的维度进行优化。

2. **APP文件的组成**
将APP包里的文件按大小排序，让我们来分析一下这些文件:

* **QYLiveTool可执行文件** ，这个文件是最核心的执行文件，包含了你APP里所有的代码以及引用的静态库，但是不包含动态库。后面会针对这个文件做代码层次的优化。
* **Asserts.car** 这个文件包含了所有通过Assets Catalog管理的图片，通过[特定软件](https://github.com/pcjbird/AssetsExtractor)可以将其解压。
* **其他的静态资源** 如果没有使用Assets Catalog管理的图片以及一些其他的资源，如字体，文本等都会散列在这里。
* **PlugIns** 如果你的APP试用了Extension，例如我们APP用了ReplayKit（录屏），所以PlugIns里会有两个文件，这个如果不注意也可能增加很多包大小，如何避免以及如何优化后面也会讲到。
* **Frameworks** 我们的项目是**Swift**写的，在Xcode9之前，通过pods管理的包只能以动态库的形式加载，所以这个文件夹里存放了用到的Swift标准库，以及我们自己引入的依赖库，Xcode9开始，这个限制解除了，我们可以把通过pods以静态库的形式引入，静态库相比动态库体积上会缩小很多，而且APP的启动速度也会变快。
还有一个问题是：这个文件夹里除了我们自己的库为啥还有很多swift标准库？这是因为Swift4以及之前版本的ABI是不稳定的，同样的二进制代码在不同的系统中跑的结果是不一样的，所以开发者将对应的swift标准库打入APP包里，但是好消息是Swift5，[ABI终于稳定了](https://onevcat.com/2019/02/swift-abi/),也就意味着不用在我们包里引入Swift的标准库了。
![7e2864d825df77367898dbbbff797e6a.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p187)

3. **APP Thinning**
APP Thining是在iOS9之后，我们上传包到iTunes connect之后，苹果会针对不同的设备，根据屏幕分辨率，cpu架构（32位，64位）等把我们的APP分为不同的安装包(variant)，不同的设备下载的variant也是不一样的。APP Thining分为**Slicing**、**Bitcode**、**On-Demand Resources**。
> The App Store and operating system optimize the installation of iOS, tvOS, and watchOS apps by tailoring app delivery to the capabilities of the user’s particular device, with minimal footprint. This optimization, called app thinning, lets you create apps that use the most device features, occupy minimum disk space, and accommodate future updates that can be applied by Apple. Faster downloads and more space for other apps and content provides a better user experience.

![356392e83af65369a37ff32e57d01fda.jpeg](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p190)

* **Slicing** 
> Slicing is the process of creating and delivering variants of the app bundle for different target devices.

![15112e33eea427b6a53f9d82dd502987.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p192)
看完上图可以发现，Slicing根据设备不同的屏幕分辨率，不同的CPU指令集等划分不同的Variant，从而达到专机专用，优化性能的同时也降低了包的体积。

* **Bitcode** 
> Bitcode is an intermediate representation of a compiled program. Apps you upload to iTunes Connect that contain bitcode will be compiled and linked on the App Store. Including bitcode will allow Apple to re-optimize your app binary in the future without the need to submit a new version of your app to the App Store.

如果你开启了Bitcode也就意味着你提交到iTunes connect的代码是一个中间层的代码，如果苹果以后除了别的cpu架构（例如最新的arm64e）或者LLVM推出了其他的优化，Apple会自动帮你做优化，而不需要你上传新的包了。开启Bitcode可能会影响crash定位，需要从iTunes connect下载新的dSYM文件来进行符号化。
由于我们的APP最低系统版本要求是10.0，在这个基础上开启bitcode包大小没有降低太多，并且由于引入的一些第三方库没有开启bitcode，所以就没办法享受开启bitcode带来的好处了。

* **On-Demand Resources** 

这个是将一部分文件放在苹果服务器上，不会在安装APP的时候下载，等到用户需要这些资源的时候才会下载。
![356392e83af65369a37ff32e57d01fda.jpeg](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p190)

* * *

**目标清晰之后，就可以着手具体的优化工作了，主要分三个方面来说一下，第一个是相对比较简单，也是成果比较显著的，就是资源文件的优化，包括删除不再使用的文件，删除重复文件，文件上云等等，第二个是代码层次的优化，包括代码段大小分析，静态库动态库的使用等等，第三个是Xcode编译，打包选项的一些调优。**

#### 资源文件层次优化
这部分相对比较简单，在这里主要介绍一些工具的使用。

1. **搜索不再使用的资源资源文件**
我们使用的是GitHub上一个开源的Mac app，叫[LSUnusedResources](https://github.com/tinymind/LSUnusedResources)。安装后，点击Browse选择你的工程目录，点击search后即可看到扫描的结果，然后可以按需删除掉不再使用的文件，删除之前一定要二次确认，因为这个搜索结果不是100%准确，如果你的文件名字是动态拼接的话，可能会有误删的风险，所以删除一定要谨慎！在这里简单说一下这个软件的原理:
> 对某一文件目录下所有的源代码文件进行扫描，用正则表达式匹配出所有的@"xxx"字符串（会根据不同类型的源代码文件使用不同的匹配规则），形成“使用到的图片的集合”，然后扫描所有的图片文件名，查看哪些图片文件名不在“使用到的图片的集合”中，然后将这些图片文件呈现在结果中。你可以修改正则匹配规则，以符合你们自己的需求。
![7745b8e58008c926564cb5d8a47002d0.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p193)

2. **删除重复文件**
这个主要使用Linux系统的一个命令行工具[fdupes](https://github.com/adrianlopezroche/fdupes)，可以通过homebrew安装 **brew install fdupes** 安装完之后可以cd到指定目录，输入命令 **fdupes -Sr ./** 即可搜索当前根目录所有文件，最终会输出所有重复的文件，以及文件的大小。fdupes会按照:文件大小->部分MD5签名对比->完整MD5签名对比->逐个字节对比，来高效率的查找重复文件。

![700f559591774a10eb0f7ecc5827bf6a.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p195)

3. **大文件压缩**
这里我们说一下如何对图片进行压缩，这里介绍一个很好用的无损压缩工具[ImageOptim](https://imageoptim.com/mac)。
如果你用Imageoptim对png图片进行过压缩，比如100kb的图片压缩成70kb，当经过Xcode打包之后发现大小可能变成了80kb，经过查阅相关资料得知：XCode 在编译的时候会对 png 图片进行 recompress，生成CgBI 格式，会重新添加删除掉的元数据，为了优化图片解码，减少不必要的 GPU 和 CPU 的开销，通俗来说，Xcode会将你压缩的图片反压缩，然后压缩成自己想要的内容。我们将两张同样的图片，一张通过ImageOptim进行压缩，一张不进行压缩，发现最后得到的尺寸是一样的。对于其他格式，例如jpg，Xcode不会进行这种处理。说到jpg，要提另外一个特别重要的点，不要讲jpg放到Image catalog里管理，因为Xcode会将jpg转成png格式，图片大小也会增加很多。

![9b3fecffd5e9259b60f6264cea891f74.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p200)

4. **图片资源管理**
建议图片资源统一通Image Catalog管理（xcassets），因为通过Image Catalog管理的图片会统一压缩到car文件里，而且会根据不同的设备下发@2x图或者@3x图，而通过bundle管理的图片不会有这个优待。当然bundle管理也有一些其他的优势，例如可通过imageWithContentsOfFile方式加载等。

5. **资源文件上云**
一些体积较大的，或者经常变换的可以将资源文件放在云端，APP打开的时候再按需下载解压。例如我们的APP聊天室的表情包，还有为AI识别提供服务的模型文件等都是放在云端，动态下载的。
如果不用自己的服务器也可以使用苹果自己的**On-Demand Resorces**，由于公司一些规章要求我们没有使用这种方式，所以在这里也不班门弄斧了。
    
#### 代码层次优化       
这部分主要从代码结构，源代码冗余，有效性排查，静态库，动态库，App Extension等方面进行优化。

1. **源代码大小，冗余，有效排查**
* 通过使用工具[LinkMap](https://github.com/huanxsd/LinkMap)来分析我们的Link Map文件，得到每个类或者每个库所占用的空间(这里的空间包含代码段和数据段)，然后再有目标的进行代码优化。
> **如何获取Link Map文件？**
> * 在XCode中开启编译选项Write Link Map File 
XCode -> Project -> Build Settings -> 把Write Link Map File选项设为yes，并指定好linkMap的存储位置
> * 工程编译完成后，在编译目录里找到Link Map文件（txt类型) 默认的文件地址：~/Library/Developer/Xcode/DerivedData/XXX-xxxxxxxxxxxxx/Build/Intermediates/XXX.build/Debug-iphoneos/XXX.build/
> * 注意Link Map文件分为Debug版和Release版本，上面说的路径是Debug版本的路径。

![9738a0a7163366276d5e4bc947ca23fc.png](evernotecid://12842C8D-EB6C-4DA4-A53F-91F751F0F3C4/appyinxiangcom/1083386/ENResource/p202)
    
* 删除重复的或者不再使用的类和方法，目前扫描思路大致分为：基于Clang扫描、基于可执行文件扫描、基于源码扫描。如果你用字符串的形式来调用类和方法的话，删除一定要谨慎，除非你100%确定，否则不要轻易删除。

2. **静态库，动态库的选择**
> 静态库：链接时完整地拷贝至可执行文件中，被多次使用就有多份冗余拷贝静态库有两种存在形式: .a和.framework。
动态库：动态库则不会复制, 只有一份. 程序运行时动态加载到内存; 系统只加载一次, 多个程序共用, 节省内存。动态库有两种存在形式: .dylib和.framework。

我们试过把相同代码分别打成动态库和静态库，动态库体积会比静态库大很多，大量使用动态库也会拖延APP启动速度。
如果你的项目是swift项目，并且包是通过cocoapod管理的话，在Xcode9之前Podfile必须加一条**use_frameworks!** 这个会将所有的pod已动态库的形式加载，在Xcode9之后，通过cocoapod管理的库可以以静态库的形式导入到工程里了，改变后同样的库体积降低了30%左右。

3. **App Extension注意事项**
App Extension的文件存放在Plugin文件夹，如果在你的代码里引入了静态库，主APP里也引入了同样的静态库，那么这个静态库会导入两份，所以尽量将这种库改成动态库，Extension和主APP就可以share了。

#### 编译层次优化

根据自身APP的特点修改Xcode的一些选项，同样有不错的瘦身效果。
1. **Generate Debug Symbols**
> Enables or disables generation of debug symbols. When debug symbols are enabled, the level of detail can be controlled by the build ‘Level of Debug Symbols’ setting.

如果设置成no，ipa中不会生成symbol文件，会减少ipa的大小，但是会影响crash定位。

2. **Optimization Level**
这个给我们提供了三个选项，分别为：
>* No optimization[-Onone]：不进行优化，能保证较快的编译速度。
>* Optimize for Speed[-O]：编译器将会对代码的执行效率进行优化，一定程度上会增加包大小。*
>* Optimize for Size[-Osize]：编译器会尽可能减少包的大小并且最小限度影响代码的执行效率。

三种选项的官方解释如下：
>We have seen that using -Osize reduces code size from 5% to even 30% for some projects.
>But what about performance? This completely depends on the project. For most applications the performance hit with -Osize will be negligible, i.e. below 5%. But for performance sensitive code -O might still be the better choice.

设置成 **-Osize** 会减少5%-30%的代码占用空间，但是相比-O会有5%的性能损耗，我们自己的项目当中，开启 **-Osize** 并没有很明显的变化，并且我们的APP对运行时的性能要求较高，因此就没有修改。

3. **Strip Linked Product 设置为YES** 
引入今日头条的解释
>需要注意的是Strip Linked Product也受到Deployment Postprocessing设置选项的影响。在Build Settings中，我们可以看到， Strip Linked Product是在Deployment这栏中的，而Deployment Postprocessing相当于是Deployment的总开关。记得把Deployment Postprocessing也设置为YES， 该选项对安装包大小的影响非常大。 PS：Deployment Postprocessing这个配置项如果使用xcode打包，xcode会默认把这个变量置为YES， 如果使用脚本打包，记得设置。

* * *