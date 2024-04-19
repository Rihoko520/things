# 标题
# 在行首使用 1-6 个 # 字符，对应于标题级别 1-6。例如:
# 这是 H1        # typora 快捷键 Ctrl-1
## 这是 H2       # typora 快捷键 Ctrl-2（常用）
### 这是 H3      # typora 快捷键 Ctrl-3（常用）
#### 这是 H4     # typora 快捷键 Ctrl-4

# 段落和换行符
段落由一个或更多的空行分隔。

段落内换行使用换行符 <br>，或者 两个空格 + shift-Enter。不推荐使用 \ + shift-Enter。

Typora 段落快捷键：ctrl-0

# 段首缩进
使用 Markdown 写文章不需要段首缩进。但如果确实有需要的话，可以在段落前面使用两个全角空格（space）。因为一个全角空格的宽度是整整一个汉字，输入两个全角空格正好是两个汉字的宽度。

一般的中文输入法都是按 shift-Space 切换到全角模式，输完两个空格后，再次按 shift-Space 回到正常输入状态。

# 引用
使用标记符 > 对内容进行引用。

> This is a blockquote with two paragraphs. This is first paragraph.
>
> This is second pragraph. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.



> This is another blockquote with one paragraph. There is three empty line to seperate two blockquote.
（这是另一个只有一个段落的引用。用三个空行来分隔两个引用。）
Typora 引用快捷键：ctrl-shift-Q。牢记：重按快捷键取消。

# 列表
使用 * 创建一个无序列表，标记符号 * 可以替换为 + 或 -。

使用 1. list item 1 创建一个有序列表。

## un-ordered list
*   Red
*   Green
*   Blue

## ordered list
1.  Red
2. 	Green
3.	Blue
Typora 快捷键

有序列表快捷键：ctrl-shift-[
无序列表快捷键：ctrl-shift-]。在 偏好设置 > Markdown 中可设置偏好为符号 *。

# 任务列表
任务列表是将项目标记为 [] 或 [x]（未完成或已完成）的列表。

- [ ] a task list item
  - [x] list syntax required
  - [ ] normal **formatting**, @mentions, #1234 refs
- [ ] incomplete
- [x] completed
 a task list item
 list syntax required
 normal formatting, @mentions, #1234 refs
 incomplete
 completed

# 代码块
在多行代码的前一行及后一行使用三个反引号（~ 键）将其标记为代码块。同时第一行反引号后面，输入所属语言实现代码高亮。

Here's an example:

​```
function test() {
  console.log("notice the blank line before this function?");
}
​```

syntax highlighting:
​```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
​```
Typora 代码块快捷键：ctrl-shift-K

# 数学公式
当你需要在编辑器中插入数学公式时，可以使用两个美元符 $$ 包裹 TeX 或 LaTeX 格式的数学公式来实现。

如：一个简单的数学公式，求圆的面积。

$$
S=\pi r^2
$$

Typora 公式块快捷键：ctrl-shift-M

# 表格
|学号|姓名|分数|
|---|---|---|
|小明|男|75|
|小红|女|79|
|小陆|男|92|
通过在标题行中包含冒号（：），可以将该列中的文本定义为左对齐，右对齐或居中对齐：

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
最左侧的冒号表示左对齐的列（默认即为左对齐）；最右边的冒号表示右对齐的列；两侧的冒号表示中心对齐的列。

Typora 表格快捷键：ctrl-T

# 流程图
横向流程图：

graph LR;
A[Hard edge] -->|Label| B(Round edge)
B --> C{Decision}
C -->|One| D[Result one]
C -->|Two| E[Result two]

纵向流程图：

graph TD;
A[christmas] -->B(Go shopping)
B --> C{Let me think}
C -->|One| D[Laptop]
C -->|Two| E[iPhone]
C -->|Three|F[Car]

# 脚注
在这段文字后添加一个脚注[^footnote]。

[^footnote]: 这里是脚注的内容.
footnote 可以是任意英文字符； 脚注的内容可以放在文章的任意位置（一般放最后）。

# 水平分隔线
可用三个以上的减号、星号、底线在一空行中建立一条分隔线，中间可以插入空格，但行内不能有其他东西。

---
***
___

# YAML Front Matter
Typora 现在支持 YAML Front Matter。在文章顶部输入 ---，然后按 Return 引入元数据块。

# 目录
输入 [toc]，然后按 Return 键。这将创建一个“目录”部分。TOC 从文档中提取所有标题，其内容会随文档自动更新。

# 区段元素
# 链接
Markdown 支持两种链接样式：行内链接和参考链接。在这两种样式中，链接文本都由 [方括号] 分隔。

# 行内链接：

要创建行内链接，请在链接文本的右方括号后立即使用一组常规括号 ()。在括号内，将您想要链接指向的 URL 以及链接的可选标题放在引号中。例如：

This is [an example](http://example.com/ "Title") inline link.

[This link](http://example.net/) has no title attribute.
This is an example inline link.

This link has no title attribute.

Typora 超链接快捷键：ctrl-K。通常先复制链接，然后选中文字按 ctrl-K 插入链接。

单击链接将展开它进行编辑，ctrl-Click 将在 web 浏览器中打开超链接。

参考链接：

参考链接使用第二组方括号，在方括号内放置一个您选择的标签来标识（identify）链接：

This is [an example][id] reference-style link.

Then, anywhere in the document, you define your link label on a line by itself like this:

[id]: http://example.com/  "Optional Title Here"
id name 可以用字母、数字和空格，且不分大小写。

另外，隐式参考链接允许您省略链接的名称，在这种情况下，链接文本本身将用作名称。只需使用一组空的方括号——例如，将“ Google”一词链接到 google.com 网站，您可以简单地编写：

[Google][]
And then define the link:

[Google]: http://google.com/
自动链接：

Markdown 支持以比较简短的自动链接形式来处理网址和电子邮件信箱，只需用 < > 包起来，Markdown 就会自动把它转成链接。例如：

<http://example.com/>
<address@example.com>
# 图片
图片的语法与链接相似，但需要一个额外的 ! 字符，放在链接开始之前。插入图像的语法如下：

![Alt text](/path/to/img.jpg)

![Alt text](/path/to/img.jpg "Optional title")
Typora 图片快捷键：ctrl-shift-I

您可以使用拖放功能从图像文件或 Web 浏览器中插入图片。您可以通过单击图片来修改 markdown 源代码。如果通过拖放添加的图像与您当前正在编辑的文档位于同一目录或子目录中，则将使用相对路径。

# 强调
Markdown 把星号（*）和下划线（_）作为强调标示符。用一个 * 或 _ 包裹的文本将被一个 HTML <em> 标签包裹。例如：

*斜体*
_斜体_
推荐使用星号（*）。

Typora 斜体快捷键：ctrl-I

GFM (Github Flavored Markdown) 将忽略单词中的下划线，这通常在代码和名称中使用，如下所示：

wow_great_stuff

do_this_and_do_that_and_another_thing.

要在原本会用作强调定界符的位置产生文字星号，您可以将其反斜杠转义：

\*this text is surrounded by literal asterisks\*
粗体
用两个 * 将使其包裹的内容被 HTML <strong> 标签包裹。例如：

**double asterisks**
Typora 粗体快捷键：ctrl-B

加粗斜体
***加粗斜体***
代码
要表明行内代码，请用反引号引起来（`）。与预格式化的代码块不同，行内代码指示正常段落中的代码。例如：

Use the `printf()` function.
Use the printf() function.

Typora 代码快捷键：ctrl-shift-`

# 删除线
~~删除线~~
~~Mistaken text.~~ becomes Mistaken text.

Typora 删除线快捷键：alt-shift-5

下划线
下划线由原始 HTML 驱动。

<u>Underline</u> becomes Underline.

Typora 下划线快捷键：ctrl-U

# Emoji 😄
使用语法 :smile: 输入表情符号。

下标
下标：H<sub>2</sub>O
下标：H2O

上标
上标：O<sup>2</sup>
上标：O2

# HTML
您可以使用 HTML 样式化纯 Markdown 不支持的内容。例如，使用 <span style="color:red">this text is red</span> 来添加红色文本。

折叠内容
使用 HTML 5 <details> 标签，指定用户可以按需打开和关闭的其他详细信息。

<details> <summary>Title</summary>

Contents ...

</details>
Title
内容里面可以嵌套使用 Markdown 语法和 HTML 语法。

折叠的用途：

可用于折叠大段代码
或者不重要的内容
嵌入内容
某些网站提供了基于 iframe 的嵌入代码，您也可以将其粘贴到 Typora 中。例如：

<iframe height='265'scrolling='no'
title='Fancy Animated SVG Menu'
src='http://codepen.io/jeangontijo/embed/OxVywj/?height=265&theme-id=0&default-tab=css,result&embed-version=2'
frameborder='no'allowtransparency='true'allowfullscreen='true'
style='width: 100%;'></iframe>

Audio
您可以使用 HTML <audio> 标签来嵌入音频。例如：

<audio src="xxx.mp3" />
src 属性可以设置为一个音频文件的 URL 或者本地文件的路径。

Video
您可以使用 HTML <video> 标签来嵌入视频。例如：

<video src="xxx.mp4" />