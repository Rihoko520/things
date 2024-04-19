# Ubuntu不显示共享文件夹解决方案
## 设置共享文件夹之后不显示，解决方法如下：
- 检查共享文件夹是否设置成功
```
vmware-hgfsclient
```
- 进入管理员模式的终端
```
su root
```
```
passwd(200949)
```
- 用vim编辑器打开fstab
```
 vim /etc/fstab
```
在文本最后一行加上这串代码
```
vmhgfs-fuse .host:/ /mnt/hgfs fuse.vmhgfs-fuse -o nonempty allow_other
```
---
### vim 编辑使用方法
按a进入编辑模式
esc退出编辑
：wq离开并保存文件
---
