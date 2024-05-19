#在Python中，父类和子类之间的关系是通过继承来实现的。父类是一个类，
#子类是从父类继承而来的类，子类可以使用父类中定义的方法和属性。这种继承关系可以帮助我们编写更加模块化和可重用的代码。
#父类通常包含一些通用的方法和属性，而子类可以根据需要添加新的方法或属性，
#也可以覆盖父类中的方法。在Python中，创建子类非常简单，只需在子类的定义中将父类作为参数传递即可。
# 定义父类 Animal
class Animal:
    # 初始化方法，设置物种
    def __init__(self, species):
        self.species = species

    # 吃的方法
    def eat(self):
        print("The animal is eating.")

# 定义子类 Dog，继承自 Animal
class Dog(Animal):
    # 初始化方法，设置物种和品种
    def __init__(self, species, breed):
        super().__init__(species)
        self.breed = breed

    # 汪汪叫的方法
    def bark(self):
        print("The dog is barking.")

# 创建子类对象
my_dog = Dog("Canine", "Labrador")
# 打印物种和品种
print(my_dog.species)
print(my_dog.breed)
# 调用父类方法 eat
my_dog.eat()
# 调用子类方法 bark
my_dog.bark()