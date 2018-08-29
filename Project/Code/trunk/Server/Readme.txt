需要安装 python3、mysql 社区版、pymysql、protobuf

1. 安装mysql社区版，按照http://www.cnblogs.com/laumians-notes/p/9069498.html
进行配置

2.创建数据库
create database minigame;

3.创建服务器登陆所用用户账号 （ client   password   只能从本地连接，如果要允许从任意主机登陆，要用 client@'%' , 要允许只从指定ip主机登陆，用 dbadmin@192.168.1.100  ）
create user client@localhost  identified by 'password'

4.赋予权限
grant all on minigame.* to client@localhost;

5.查看本机ip       ipconfig /all
找到 ipv4对应栏

6.在 Config/Config 文件修改 host为本机ip

7.运行 GateServer/GateServer

8.可运行TestClient/Client进行测试

