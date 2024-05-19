### C++

-----------------------

- 头

```c++

#include<iostream>
using namespace std;
// using namespace std 为了解决多个模块间命名冲突的问题
```
- C++库提供的对象都存放在std这个标准名字空中，比如cin、cout、endl

```c++

#include<iostream>
using namespace std;
//这里直接制定了下面的语法
int main()
{
    cout<<"Nice to meet you!"<<endl;
    return 0;
}

```

- 也可以用域限定符::来逐个制定

```c++
#include<iostream>
int main()
{
    std::cout<<"Nice to meet you!"<<std::endl;
    return 0;
}
//这样写很麻烦，但是就不用开头写using namespace std了。
```
- 用using和域限定符一起制定用哪些名字
```c++
#include<iostream>
using std::cout;
using std::endl;
int main()
{
    cout<<"Nice to meet you!"<<endl;
    return 0;
}
```
-----------------------

#### C++中的输入输出

-  cout输出流的使用
本质上，是将字符串"Hello"插入到cout对象里，并以cout对象作为返回值返回，因此你还可以用<<在后面连续输出多个内容,最常用到的还有endl操纵符，可以直接将它插入到cout里，起输出换行(类似于c的/n)的效果，

```c++
cout<<"Hello"<<endl<<"www.dotcpp.com"<<endl;

```

- cin输入流的使用：
     - cin也可以连续接收多个变量
    
    ```c++
    int a,b;
    cin>>a>>b;
    ```
-------------------

### C++表达式和控制语句

#### C++中的数据类型

- int、char、float、double分别表示整形、字符型、单精度和双精度类型

```c++
#include<iostream>
using namespace std;
int main()
{
    int num;//学生学号
    char sex;//性别
    double score1;//科目一成绩
    double score2;//科目二成绩
    double score3;//科目三成绩
    cout<<"Please input student's ID、‘M’ or ‘W’、score1、score2 and score3"<<endl;
    cin>>num>>sex>>score1>>score2>>score3;
    cout<<"ID:"<<num<<" "<<sex<<" Total score is:"<<score1+score2+score3<<endl;//输出该学生信息及总成绩
    return 0;
}
```

- 布尔类型是一种逻辑值，关键字类型为bool，定义出来的变量只有true和false两个，分别表示真和假两个值，在内存上一般只占一个字节。
```c++
#include<iostream>
using namespace std;
int main()
{
    int a=9;
    int b=10;
    bool r;//定义布尔类型变量r,true 的话 r 为 1 ，false 就为 0
    r = a>b;
    cout<<r<<endl;
    cout<<"bool size is:"<<sizeof(r)<<endl;
    return 0;
}

```
正常会得到如下结果：
![bool](pho/image.png)


```c++
#include<iostream>
using namespace std;
int main()
{
    bool a=true;
    bool b=false;
    cout<<a<<endl<<b<<endl;
    return 0;
}
```
输出结果依然是**1**和**0**并非true和false


---

#### C++算数运算符实例讲解

- 算数运算符（+、-、*、/、%）

```c++
#include<iostream>
using namespace std;
int main()
{
    int a;//待判断的这个三位数
    int ge;//三位数中的个位
    int shi;//三位数中的十位
    int bai;//三位数中的百位
    cin>>a;
    ge = a%10;//取余
    shi = a%100/10;//取余之后取整
    bai = a/100;//取整
    cout<<ge<<" "<<shi<<" "<<bai<<endl;
    return 0;
}
```
运行：
input:485
output:5 8 9

-----
```c++
#include<iostream>
using namespace std;
int main()
{
   int x,y;
   cin>>x;
   if(x<1)
   {
      y=x;
   }
   else if(1<=x && x<10)
   {
      y=2*x-1;
   }
   else
   {
      y=3*x-11;
   }
   cout<<y<<endl;
   return 0;
}
```
运行：
input:14
output:31

-----------

#### C++自增++和自减--运算符实例讲解

- 自增运算符（++）和自减运算符（--）都是单目运算符，即一个变量的使用

```c++

#include<iostream>
using namespace std;
int main()
{
    int a=10;
    cout<<a++<<endl;//++在后，就是先用再加，即先输出在自加1
    cout<<a++<<endl;  
    cout<<a<<endl;
    return 0;
}

```
output:
```
10
11
12
```

#### C++赋值运算符=实例讲解

```c++
#include<iostream>
using namespace std;
int main()
{
    int a=10;//定义变量a，并且将10作为初始化值赋给a
    int b;
    b=a;//将a的值赋值给b
    return 0;
}
```

#### C++关系运算符实例讲解

- *>、< 、>=、<=、!=、==六种*
```c++
 10>5;    // 10大于5，很明显成立，是真
 2>=2;    // 2大于或者等于2，也成立，是真
 3!=1;    // 3不等于1，的确成立，是真
 5==5;    // 5确实等于5，成立，为真
```

- 关系运算符表达式的结果就是非0即1的结果(true or false)

```c++
#include<iostream>
using namespace std;
int main()
{
    cout<<(10>5)<<endl;
    cout<<(2>=2)<<endl;
    cout<<(3!=1)<<endl;
    cout<<(5==5)<<endl;
    return 0;
}
```
output:
```
1
1
1
1
```

#### C++逻辑运算符实例讲解

- &&、||、!
分别表示逻辑与、逻辑或、逻辑非

- &&的两边各一个表达式，如果运算符的左右两边的表达式都为真，表达式整体才为真，否则即为假

- 要求两边各一个表达式，如果运算符左右两边的表达式只要有一个为真，那么逻辑或表达式的整体就为真，否则都为假

- 逻辑非是一个单目运算符，它表示取反的意思，放在表达式的左边，如!a ，即原先为真的表达式取反之后变为假，原先为假的表达式取反之后变为真

```c++

#include<iostream>
using namespace std;
int main()
{
    int a=10;
    int b=20;
    int c=30;
    int d,e;
    d=!c>(b-a)&&(c-b)>(b-a);//如果c不是大于(b-a)而且(c-b)大于(b-a)的话整体为真，d=1；反之为假，d=0
    e=(b-a)||(c-b)&&!(c-b-a);//(b-a)或者(c-b)不等于(c-b-a)的话整体为真，e=1；反之为假，e=0
    cout<<d<<endl;
    cout<<e<<endl;
    return 0;
}
```
output:
```
0
1

```

#### C++if选择结构实例讲解

- 用if选择结构、if-else选择结构、else-if多选择结构以及switch多选择结构
```c++
#include<iostream>
using namespace std;
int main()
{
    int a;//待判断的这个三位数
    int ge;//三位数中的个位
    int shi;//三位数中的十位
    int bai;//三位数中的百位
    cin>>a;
    ge = a%10;
    shi = a%100/10;
    bai = a/100;
    if(ge*ge*ge+shi*shi*shi+bai*bai*bai == a)
        cout<<"1"<<endl;
    else
        cout<<"0"<<endl;
    return 0;
}
```
![output](pho/image-1.png)

- 分段函数

```c++

#include<iostream>
#include<iomanip>
using namespace std;
int main()
{
   double x;
   double y;
   cin>>x;
  
   if(x<1)
    {
      y=x;
   }
   else if(x>=1 && x<10)
    {
      y=2*x-1;
   }
   else
    {
      y=3*x-11;
   }
   cout<<fixed<<setprecision(2)<<y<<endl;
   return 0;
}
```
![out](pho/image-2.png)

#### C++中switch选择结构实例讲解
- switch结构同样也可以实现多种分支结构，类似else if结构，即对于多种情况时候可以根据条件让程序判断选择走哪个分支，丰富了程序的可能性
```c++
#include<iostream>
using namespace std;
int main()
{
    int n;
    cin>>n;
    switch( n )
    {
        case 0: cout<<"Sunday"; break;
        case 1: cout<<"Monday"; break;
        case 2: cout<<"Tuesday"; break;
        case 3: cout<<"Wednesday"; break;
        case 4: cout<<"Thursday"; break;
        case 5: cout<<"Friday"; break;
        case 6: cout<<"Saturday"; break;
        default :cout<<"input error!";
    }
    return 0;
}
```

#### C++中while循环结构实例讲解
- while循环、do-while循环以及for循环三种，包括配合使用很多的break和continue
##### while循环
- C++中循环相关的题，求A+B的和的简单问题，但为多组测试数据，循环不停的接受，C++的写法如下：
```c++
#include<iostream>
using namespace std;
int main()
{
    int a,b;
    while(cin>>a>>b)
    {
        cout<<a+b<<endl;
    }
    return 0;
}//cin返回的是一个istream的流对象，如果遇到问题接收失败，则返回false，进而结束循环。
```
- 判断素数的题
```c++
#include<iostream>
using namespace std;
int main()
{
    int n,i;
    cin>>n;
    for(i=2;i<n;i++)
    {
        if(n%i==0)
            break;
    }
    if(i>=n)
        cout<<1<<endl;
    else
        cout<<0<<endl;
  
    return 0;
}

```
##### do while循环
- 遇到do先进入循环执行一次循环体里的语句，然后再判断while里的表达式是否成立，
来决定是否进入循环执行第二次
- N以内累加求和
```c++

#include <iostream>
using namespace std;
int main() {
    int N,sum = 0,i;
    cin >> N;
    do
    {
        sum += i;
        i++;
    }while(i<=N);//**
    cout << sum << endl;
    return 0;
}

```

##### for循环
- 求N以内的奇数和
```c++

#include<iostream>
using namespace std;
int main()
{
    int n,i;
    int sum = 0;
    cin >> n;
    for(i = 1; i <= n; i ++)
    {
        if(i % 2 != 0)   //替换为if(i % 2)的效果是一样的
            sum += i;
    }
    cout << sum;
    return 0;
}
```

### C++函数调用与重载、内联
#### C++中函数调用的用法
- 函数调用及传参
```c++
#include<iostream>
#include<cstring>
using namespace std;
int Reverse(char a[],char b[])//字符串逆序
{
    int i=0,n;
    n=strlen(a);
    while(a[i]!='\0')
    {
        b[n-i-1]=a[i];
        i++;
    }
    b[n]='\0';
    return 0;
}
int main()
{
    char str1[100];
    char str2[100];
    cin>>str1;
    Reverse(str1,str2);
    cout<<str2<<endl;
    return 0;
}
```
in
```
44fgh
```
out
```
hgf44
```

#### 带默认形参值的函数
- 允许在自定义函数的形参列表中，给形参一个默认的值，这样在调用的时候如果有实参，那么按照实参传递给形参的方法使用；若调用的时候没有指定对应的实参，则形参将使用默认值。
```c++
#include<iostream>
using namespace std;
int add(int a=3,int b=5)//初始化了参量值
{
    return a+b;
}
int main()
{
    cout<<add(10,20)<<endl;//将10和20分别给a和b
    cout<<add(30)<<endl;//将30给a，b为默认的5
    cout<<add()<<endl;//使用a、b的默认值3和5
    return 0;
}

```
out
```
30
35
8
```

#### C++中的函数重载
- 对于同一个功能函数，可能处理的对象类型不同，则需要重新实现一遍这个函数，这样下去就显得代码更加繁多，C++为了解决这一问题，而支持函数重载来解决这个问题。
```c++
#include<iostream>
using namespace std;
int add(int a,int b)
{
    cout<<"(int ,int)\t";
    return a+b;
}
double add(double a,double b)
{
    cout<<"(doble ,double)\t";
    return a+b;
}
double add(double a,int b)
{
    cout<<"(double ,int)\t";
    return a+b;
}
double add(int a,double b)
{
    cout<<"(int ,double)\t";
    return a+b;
}
int main()
{
    cout<<add(2,3)<<endl;
    cout<<add(2.9,15.3)<<endl;
    cout<<add(10,9.9)<<endl;
    cout<<add(11.5,5)<<endl;
    return 0;
}
//函数重载即两个或以上的函数，函数名相同，但形参类型或个数不同，
///编译器根据调用方传入的参数的类型和个数，自动选择最适合的一个函数来进行绑定调用，自动实现选择。
```

#### C++函数模板
- 函数模板，是可以创建一个通用的函数，可以支持多种形参。用关键字template来定义，形式如下：


- 说明一下，这个一般形式中，第一行的template<class 类型名1，class 类型名2…>是一句声明语句，template是定义模板函数的关键字，尖括号里可以有多个类型，前面都要用class(或者typename来定义)。然后后面跟定义的函数模板，切记中间不可以加其他的语句，不然会报错！

```c++
template<class 类型名1,class 类型名2…>
返回值 函数名（形参表列） 模板参数表
{
   函数体
}

```

```c++

#include<iostream>
using namespace std;
template<class T1,class T2>
T1 add(T1 x,T2 y)//T1 和 T2 是类型参数，T1 的意义是指定了方法 add 的返回类型,T2 则表示方法的第二个参数的数据类型。
{
    cout<<sizeof(T1)<<","<<sizeof(T2)<<"\t";
    return x+y;
}
int main()
{
    cout<<add(10,20)<<endl;;
    cout<<add(3.14,5.98)<<endl;
    cout<<add('A',2)<<endl;
    return 0;
}
//在主函数中，实际调用时，我们调用了三次，分别三种不用的类型传入，模板函数中的T1和T2类型将根据实际传入的类型变成具体类型，这个化成就叫做模板的实例化。
```
out:
```c++
4,4	30
8,8	9.12
1,4	C
```

#### inline内联函数
- 为我们提供了内联的机制，即仍然使用自定义函数，但在编译的时候，把函数代码插入到函数调用处，从而免去函数调用的一系列过程，像普通顺序执行的代码一样，来解决这个问题！
```c++
//只需要在函数定义的前面加上关键字inline声明就可以了
#include<iostream>
using namespace std;
  
inline int Max(int a,int b)
{
    return a>b?a:b;
}
int main()
{
    cout<<Max(3,5)<<endl;
    cout<<Max(7,9)<<endl;
    return 0;
}

```
- 内联函数与**register**变量类似，仅仅是我们提给编译器的一个请求，最终是否真正会实现内联，由编译器根据情况自行选择。

### 类和对象(面向对象)
#### C++类的定义
- 类其实就是一个模子，是一个变量类型，对象就是这个类型定义出来的具体的变量，就像int a;这句话，int对应类，a就对应对象。
但需要注意的是int是C++的内置类型，并不是真正的类。
    - 类是对象的抽象和概括，而对象是类的具体和实例。
- 关键字用class类定义，比如下面定义一个C++的类，学生类：
```c++
class Student
{
public:
    int num;
    char name[100];
    int score;
    int print()
    {
        cout<<num<<" "<<name<<" "<<score;
        return 0;
    }
};
```
- 类里还有一个public的东西，它是控制成员访问权限的一个存取控制属性，除了public以外，还有private、protected一共三种。
  - private表示私有，被它声明的成员，仅仅能被该类里的成员访问，外界不能访问，是最封闭的一种权限
  - protected比private稍微公开一些，除了类内自己的成员可以访问外，它的子类也可以访问
  - 而public声明的成员，则可以被该类的任何对象访问，是完全公开的数据

- C++还支持另外一种写法，就是成员函数仅在类内声明函数原型，在**类外定义函数体**，这样在类里可以看到所有成员函数的列表，像目录一样**一目了然**，规范很多。
```c++

class Student
{
public:
    int num;//学号
    char name[100];//名字
    int score;//成绩
    int print();//类内声明print函数
};
int Student::print()//在类外定义完整的print函数(python写法是student.print())
{
    cout<<num<<" "<<name<<" "<<score;
    return 0;
}
```

#### 对象的建立和使用
1. **对象的创建**
- 定义了一个这个类的对象，也可以说实例化了一个对象
- 而对象的使用，和结构体的使用也一样，都是主要访问里面的成员，也都是用过.的方式来访问，如：
```c++
    Student A;
    A.num = 101;
    strcpy(A.name,"dotcpp");
    A.score = 100;
    A.print();

//需要注意的是，这里类中的成员变量都是声明为public类型的，如果声明为private类型，
//则在主函数中主要通过对象.变量的方式直接访问的话就会被禁止报错，
//原因private类型的变量是私有类型，
//不允许外部访问。
```
- 对于想保护但又想控制的私有变量，我们通常将其声明为private类型，然后同时定义一个public类型的专门赋值的方法，由于内部成员可以访问**private**声明的变量，我们就可以在外部通过这个public的方法来间接控制这些私有的成员，来起到封装、保护的效果，而这个public类型的方法，也称之为这个类的一个外部接口。
- 以下是一个简单的C++示例，展示了如何使用私有变量和公共成员函数来实现**封装和保护**：
```c++
#include <iostream>

class MyClass {
private:
    int myPrivateVariable;

public:
    // 公共成员函数用于设置私有变量的值
    void setPrivateVariable(int value);
    // 公共成员函数用于获取私有变量的值
    int getPrivateVariable(); 
};
void MyClass::setPrivateVariable(int value){

    myPrivateVariable = value;

}

int MyClass::getPrivateVariable() {
    return myPrivateVariable;
}

int main() {
    MyClass myObject;

    // 通过公共成员函数设置私有变量的值
    myObject.setPrivateVariable(10);

    // 通过公共成员函数获取私有变量的值并输出
    std::cout << myObject.getPrivateVariable() << std::endl;

    return 0;
}
```

2. **对象的指针**
- 与普通变量一样，对象也是一片连续的内存空间，因此也可以创建一个指向对象的指针，即对象指针，存储这个对象的地址。
```c++
类名 *指针名;
```
- Student *p;定义一个Clock类型的指针p，需要清楚的是，这里并没有建立对象，当然也不会调用构造函数。接下来就可以将一个同类型的类对象地址赋值给这个指针，然后通过->来访问对象中的成员。
```c++
Student *p;
Student A;
p = &A;
p->print();
```
- 用指针来传递，其传递的为地址，不会进行对象之间的副本赋值。

3. **对象的引用**
- 对象引用就是一个类对象起个别名，本质上也是把这个类对象的地址赋给了这个引用类型，两者是**指向一块内存空间**的。

```c++
Student A;
Student &Aq=A;
```
- 定义一个Student类型的对象，然后用&来定义一个该类类型的引用类型，并把A对象赋给Aq作为初始化。

**需要注意的是：**

- 与指针一样，两者必须是同类型才可以引用。
- 除非做函数的返回值或形参时，其余定义引用类型的同时就要初始化！
- 引用类型并非是新建立一个对象，因此也不会调用构造函数。

- 因此使用方法也和类对象一样，用别名.成员的方法进行访问
```c++
Student A;
Student &Aq=A;
Aq.print();
```
- 用引用类型时，本质还是存的地址，使用起来和类对象本身使用一样，再做函数实参时，**直接传入引用对象**就可以，不用加地址符，因此看起来更直观、方便。

- 以下是较为全面的引用例子
```c++
#include <iostream>
using namespace std;

class Car {
public:
    int speed;// 声明一个整型成员变量speed
    Car(int s) : speed(s) {}//定义了一个接受整型参数s的Car类构造函数，该构造函数将参数s的值赋给类的成员变量speed进行初始化。
    // 成员函数SpeedUp，用于增加速度
    void SpeedUp() {
        speed += 10; // 将速度增加10
    }
};

int main() {
    Car c(50);// 创建一个Car对象c，速度初始化为50
    
    // 使用指针引用对象
    Car* ptr = &c; // 创建一个指向Car对象c的指针ptr
    ptr->SpeedUp(); // 通过指针调用SpeedUp函数
    cout << "Speed using pointer: " << ptr->speed << endl;// 输出通过指针访问的速度
    
    // 使用引用引用对象
    Car& ref = c;// 创建一个引用ref，引用Car对象c
    ref.SpeedUp();// 通过引用调用SpeedUp函数
    cout << "Speed using reference: " << ref.speed << endl;//用别名.成员的方法进行访问
    
    return 0;
}
```

#### C++中的构造函数(Constructor)
- 例如还是Student类的例子，我们添加一个带有默认参数的构造函数，代码如下
```c++

#include<iostream>
#include<Cstring>
using namespace std;
class Student
{
    private:
    int num;//学号
    char name[100];//名字
    int score;//成绩
    public:
    Student(int n,char *str,int s);
    int print();
    int Set(int n,char *str,int s);
};
Student::Student(int n,char *str,int s)//给隐藏的构造函数设定内容（这个函数是在你定义这个类的时候系统给你配的）
{
     num = n;
     strcpy(name,str);
     score = s;
    cout<<"Constructor"<<endl;
}
int Student::print()
{
    cout<<num<<" "<<name<<" "<<score;
    return 0;
}
int Student::Set(int n,char *str,int s)
{
     num = n;
     strcpy(name,str);
     score = s;
}
int main()
{
    Student A(100,"dotcpp",11);//即可以在定义的同时调用构造函数，实现初始化的作用，
    A.print();
    return 0;
}

```

#### C++中的析构函数(Destructor)

- 名字前有一个波浪线~，它的作用主要是用做对象释放后的清理善后工作。















