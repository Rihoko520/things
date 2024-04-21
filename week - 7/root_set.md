# Linux：readonly option is set (add ! to override)错误

## 创建一个root权限

- 设置新root

```bash

sudo passwd root

```

此时会让你设定密码(Enter new UNIX password:)

```bash

your passwd

```

输入完第一次会让你**retype passwd

```bash

your passwd

```

确定之后会显示
passwd: password updated successfully
表示root用户成功创建并设置密码

### 使用管理员权限在终端用vim编写文本

- 先获得管理员权限<br>登陆你的root

```bash

su root

```
**press enter**
```bash

passwd

```

