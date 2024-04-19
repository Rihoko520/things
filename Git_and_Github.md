# 本地部署
## 仓库构建
- 在终端创建一个仓库
打开终端（随便一个都行，例如vim）在终端中定位到自己的仓库所在文件夹 **cd /file**
- 工作区暂存区本地版本区都在这里进行操作
## 进行用户设置
- 使用**git config --global user.name**设置用户名
```
git config --global user.name “Rihoko”
```
- 使用**git config --global user.email**设置邮箱
```
git config --global user.email a1219814581@163.com
```
## 版本控制
- 进仓库行初始化
```
git init
```
- 设置主支路
```
git config --global init.defaultBranch <名称>
```
- 初始化后默认处于主分支里面
此时你的git文件夹里面会新增加一个文件夹为.git
git所有的记录都在这里面
## 在工作区创建文件
```
echo "retard" > sb.md
```
在工作区创建一个md文件名为sb，内容为retard
## 查看自己所处分支
**git status**
- 发现新创建的文件在**untracked files**的列表里，说明是未追踪文件
## 将工作区文件添加到缓存区
- 使用 **git add**来实现添加
```
git add retard.md
```
## 进行缓存区文件的提交操作
- 用**status**查看可以发现文件已经处于**to be committed**的状态
- 用**git commit**进行提交
```
git commit
```
---
- 如果用的是vim，在commit完成后会在vim编辑器显示提交的信息，此时我们只要**esc+:wq**即可回到终端界面
---
- 当再次输入**git status**之后我们可以发现工作区已经没有东西了，即表示所有文件已被提交到本地版本库
##### tips:add 和 commit 一起写(-am)可以一次就把文件放到本地版本库.
```
git status
```
- 在提交同时将缓存区文件进行简短信息编辑的方式
```
git commit -m "you idiot"
```
“”里面的是要往文件里新增加的内容
## 查看前面的版本
```
git log
```
(HEAD -> master)表示目前我所处的版本
按**q**退出出页面

##
- 用**gitignore**文件来实现不让该文件上传到库
```
touch .gitignore
```
创建一个gitignore文件，将不想从工作区上传的文件的名字包括其后缀写进gitignore文件里面
- 做完之后再用**git status**查看就会发现你所想要忽略的文件已经查不到了，已经成功被忽略掉了。
## 创建新的分支
- 分支用来处理一些不确定是否要上传到主分支的文件代码为**git branch + name**
```
git branch (-b) code
```
新分支文件是master复制过来的，因此删除分支文件不影响主支文件
指令不会让我们自动跳转到新的分支(加了 -b 可以直接跳转)
- 用**git branch**查看新的分支
（按q来退出）
- 用**git checkout +分支名**来转到该分支上
```
git checkout code
```
## 分支重命名操作
- 本地分支重命名
```
git branch -m 原始名称 新名称
```
- 远程分支重命名
*先重命名本地分支*
```
git branch -m 旧分支名称  新分支名称
```
**删除远程分支**
```
git push origin -d 旧分支名称
```
***上传新修改名称的本地分支***
```
git push origin 新分支名称
```
****修改后的本地分支关联远程分支****
```
// 关联后push代码就不需要 push origin 分支名，
// 直接git push 就可以了
git push --set-upstream origin test
```
## 去除分支
- **git branch -D + 名字**
```
git branch -D code
```
## 合并分支内容
**git merge + 其他支路名字**
把别的分支内容合并到**当前**所处分支上
- 当合并后内容发生冲突时<br>HEAD表示是当前所处分支的内容<br>别的分支名字表示是别的分支的内容
## 删除库文件并提交更改
- 删除文件
```
git rm file
```
```
git commit -m"change"
```
- 放弃删除的改动
```
git restore --staged file
```
## 云端仓库关联
```
git remote add url
```
## 拷贝远程仓库到本地
```
git clone + URL
```
### 克隆之后要改变仓库所有者才可以进行编辑
- 用指令who or users查看自己的用户名
- 方法1改变文件所有者
```
chown -R root /home/xxx
```
## 方法2 手动禁用安全目录
```
git config --global --add safe.directory '*'
```
## 查看本地库与各个远程库的联系
```
git remote -v
```
远程仓库的url通常用**origin**表示
## 本地库上传到远程仓库
```
git push url
```
https://github.com/Rihoko520/rihoko.git
**用origin(在看联系时url左侧的一串字符）代替url只能用在你先前与本地库有联系的仓库**
- push到远程仓库需要用到个人访问**token**，这个在github上获取
- name:
rihoko
- passwd
（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）
- 从远程仓库获取文件拉到本地版本库
```
git fetch + url
```
## 找本地库与远程库的不同
```
git diff + url/（分支名称）
```
## 将远程仓库文件整合到工作区
```
git pull
```
## 查看仓库版本历史
```
git log
```

