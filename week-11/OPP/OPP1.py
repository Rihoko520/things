class ATMAccount:
    def __init__(self, balance=0):
        self.balance = balance  # 初始化账户余额

    def deposit(self, amount):
        self.balance += amount  # 存款操作
        return self.balance  # 返回更新后的余额

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount  # 取款操作
            return amount  # 返回取款金额
        else:
            return "余额不足"  # 余额不足时返回提示信息

    def check_balance(self):
        return self.balance  # 返回当前余额

# 初始化一个ATM账户

account = ATMAccount(100)

print(account.check_balance())

# 交互式操作
while True:
    print("\n1 - 存款 \t 2 - 取款 \t 3 - 查看余额 \t 4 - 退出")
    choice = int(input("请选择操作: "))

    if choice == 1:
        deposit_amount = float(input("请输入存款金额: "))
        new_balance = account.deposit(deposit_amount)
        print(f"存款成功，当前余额为: {new_balance}")

    elif choice == 2:
        withdraw_amount = float(input("请输入取款金额: "))
        result = account.withdraw(withdraw_amount)
        if type(result) == str:
            print(result)  # 打印错误信息
        else:
            print(f"取款成功，取款金额为: {result}, 当前余额为: {account.check_balance()}")

    elif choice == 3:
        print(f"当前余额为: {account.check_balance()}")  # 打印当前余额

    elif choice == 4:
        print("退出ATM操作，谢谢使用！")
        break

    else:
        print("请输入有效选项")  # 打印无效选项提示