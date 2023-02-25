# 文件读写

```python
**文件的打开和创建**
f = open('/tmp/test.txt')
f.read()
'hello python!\nhello world!\n'

f
open file '/tmp/test.txt', mode 'r' at 0x7fb2255efc00>
 
**文件的读取**
步骤：打开 -- 读取 -- 关闭
f = open('/tmp/test.txt')
f.read()
'hello python!\nhello world!\n'
f.close()
 
**文件写入（慎重，小心别清空原本的文件）**
步骤：打开 -- 写入 -- （保存）关闭
#直接的写入数据是不行的，因为默认打开的是'r' 只读模式
f.write('hello boy')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
IOError: File not open for writing

f
<open file '/tmp/test.txt', mode 'r' at 0x7fe550a49d20>
 
应该先指定可写的模式

f1 = open('/tmp/test.txt','w')
f1.write('hello boy!')

但此时数据只写到了缓存中，并未保存到文件，而且从下面的输出可以看到，原先里面的配置被清空了
[root@node1 ~]# cat /tmp/test.txt
[root@node1 ~]#

关闭这个文件即可将缓存中的数据写入到文件中
f1.close()
[root@node1 ~]# cat /tmp/test.txt
[root@node1 ~]# hello boy!

注意：这一步需要相当慎重，因为如果编辑的文件存在的话，这一步操作会先清空这个文件再重新写入。
那么如果不要清空文件再写入该如何做呢？
使用r+ 模式不会先清空，但是会替换掉原先的文件，如下面的例子：hello boy! 被替换成hello aay!
f2 = open('/tmp/test.txt','r+')
f2.write('\nhello aa!')
f2.close()

[root@node1 python]# cat /tmp/test.txt
hello aay!

如何实现不替换？
f2 = open('/tmp/test.txt','r+')
f2.read()
'hello girl!'

f2.write('\nhello boy!')
f2.close()

[root@node1 python]# cat /tmp/test.txt
hello girl!
hello boy!

可以看到，如果在写之前先读取一下文件，再进行写入，则写入的数据会添加到文件末尾而不会替换掉原先的文件。
这是因为指针引起的，r+ 模式的指针默认是在文件的开头，如果直接写入，则会覆盖源文件，
通过read() 读取文件后，指针会移到文件的末尾，再写入数据就不会有问题了。这里也可以使用a 模式

f = open('/tmp/test.txt','a')
f.write('\nhello man!')
f.close()

[root@node1 python]# cat /tmp/test.txt
hello girl!
hello boy!
hello man!

**关于其他模式的介绍，见下表：**

#模式	                    描述
#r 打开只读文件，该文件必须存在。 
#r+ 打开可读写的文件，该文件必须存在。 
#w 打开只写文件，若文件存在则文件长度清为0，即该文件内容会消失。若文件不存在则建立该文件。 
#w+ 打开可读写文件，若文件存在则文件长度清为零，即该文件内容会消失。若文件不存在则建立该文件。 
#a 以附加的方式打开只写文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾，即文件原先的内容会被保留。 
#a+ 以附加方式打开可读写的文件。若文件不存在，则会建立该文件，如果文件存在，写入的数据会被加到文件尾后，即文件原先的内容会被保留。 
#上述的形态字符串都可以再加一个b字符，如rb、w+b或ab＋等组合，加入b 字符用来告诉函数库打开的文件为二进制文件，而非纯文字文件。不过在POSIX系统，包含Linux都会忽略该字符。

**文件对象的方法：

f.readline()   逐行读取数据**
方法一：
f = open('/tmp/test.txt')
f.readline()
'hello girl!\n'

f.readline()
'hello boy!\n'

f.readline()
'hello man!'
f.readline()
''

方法二：

for i in open('/tmp/test.txt'):
...     print i
...
hello girl!
hello boy!
hello man!

**f.readlines()     将文件内容以列表的形式存放**

f = open('/tmp/test.txt')
f.readlines()
['hello girl!\n', 'hello boy!\n', 'hello man!']
f.close()
f.next()   逐行读取数据，和f.readline() 相似，唯一不同的是，f.readline() 读取到最后如果没有数据会返回空，而f.next() 没读取到数据则会报错
f = open('/tmp/test.txt')
f.readlines()
['hello girl!\n', 'hello boy!\n', 'hello man!']
f.close()

f = open('/tmp/test.txt')
f.next()
'hello girl!\n'
f.next()
'hello boy!\n'
f.next()
'hello man!'
f.next()
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
StopIteration

**f.writelines()   多行写入**
l = ['\nhello dear!','\nhello son!','\nhello baby!\n']
f = open('/tmp/test.txt','a')
f.writelines(l)
f.close()

[root@node1 python]# cat /tmp/test.txt
hello girl!
hello boy!
hello man!
hello dear!
hello son!
hello baby!

**f.seek(偏移量，选项)**

f = open('/tmp/test.txt','r+')
f.readline()
'hello girl!\n'
f.readline()
'hello boy!\n'
f.readline()
'hello man!\n'
f.readline()
' '
f.close()
f = open('/tmp/test.txt','r+')
f.read()
'hello girl!\nhello boy!\nhello man!\n'
>>> f.readline()
''
f.close()
这个例子可以充分的解释前面使用r+这个模式的时候，为什么需要执行f.read()之后才能正常插入
**f.seek(偏移量，选项)**
	选项=0，表示将文件指针指向从文件头部到“偏移量”字节处
	选项=1，表示将文件指针指向从文件的当前位置，向后移动“偏移量”字节
	选项=2，表示将文件指针指向从文件的尾部，向前移动“偏移量”字节
偏移量：正数表示向右偏移，负数表示向左偏移
f = open('/tmp/test.txt','r+')
f.seek(0,2)
f.readline()
''

f.seek(0,0)
f.readline()
'hello girl!\n'
f.readline()
'hello boy!\n'
f.readline()
'hello man!\n'
f.readline()
''

**f.flush()    将修改写入到文件中（无需关闭文件）**
f.write('hello python!')
f.flush()
[root@node1 python]# cat /tmp/test.txt
hello girl!
hello boy!
hello man!
hello python!

**f.tell()   获取指针位置**
f = open('/tmp/test.txt')
f.readline()
'hello girl!\n'
f.tell()
12

f.readline()
'hello boy!\n'
f.tell()
23

**内容查找和替换**
一、内容查找
实例：统计文件中hello个数
思路：打开文件，遍历文件内容，通过正则表达式匹配关键字，统计匹配个数。
1	[root@node1 ~]# cat /tmp/test.txt
2	hello girl!
3	hello boy!
4	hello man!
5	hello python!

脚本如下：
**方法一：**
#!/usr/bin/python
import re
f = open('/tmp/test.txt')
source = f.read()
f.close()

r = r'hello'
s = len(re.findall(r,source))
print s
[root@node1 python]# python count.py
4

**方法二：**
#!/usr/bin/python
import re
fp = file("/tmp/test.txt",'r')
count = 0
for s in fp.readlines():
		li = re.findall("hello",s)
		if len(li)>0:
		count = count + len(li)
		print "Search",count, "hello"
fp.close()
[root@node1 python]# python count1.py
Search 4 hello

**二、替换**
实例：把test.txt 中的hello全部换为"hi"，并把结果保存到myhello.txt中。

#!/usr/bin/python
import re
f1 = open('/tmp/test.txt')
f2 = open('/tmp/myhello.txt','r+')
for s in f1.readlines():
		f2.write(s.replace('hello','hi'))
f1.close()
f2.close()

[root@node1 python]# touch /tmp/myhello.txt
[root@node1 ~]# cat /tmp/myhello.txt
hi girl!
hi boy!
hi man!
hi python!

实例：读取文件test.txt内容，去除空行和注释行后，以行为单位进行排序，并将结果输出为result.txt。test.txt 的内容如下所示：
#some words
Sometimes in life,You find a special friend;Someone who changes your life just by being part of it.Someone who makes you laugh until you can't stop;Someone who makes you believe that there really is good in the world.Someone who convinces you that there really is an unlocked door just waiting for you to open it.This is Forever Friendship.when you're down,and the world seems dark and empty,Your forever friend lifts you up in spirits and makes that dark and empty worldsuddenly seem bright and full.Your forever friend gets you through the hard times,the sad times,and the confused times.If you turn and walk away,Your forever friend follows,If you lose you way,Your forever friend guides you and cheers you on.Your forever friend holds your hand and tells you that everything is going to be okay. 

脚本如下：
f = open('cdays-4-test.txt')
result = list()
for line in f.readlines():                        # 逐行读取数据
		line = line.strip()                           #去掉每行头尾空白
		if not len(line) or line.startswith('#'):     # 判断是否是空行或注释行
		continue                                   #是的话，跳过不处理
result.append(line)                            #保存
result.sort()                                              #排序结果
print result
open('cdays-4-result.txt','w').write('%s' % '\n'.join(result))              
#保存入结果文件
```
