��Ҫ��װ python3��mysql �����桢pymysql��protobuf

1. ��װmysql�����棬����http://www.cnblogs.com/laumians-notes/p/9069498.html
��������

2.�������ݿ�
create database minigame;

3.������������½�����û��˺� �� client   password   ֻ�ܴӱ������ӣ����Ҫ���������������½��Ҫ�� client@'%' , Ҫ����ֻ��ָ��ip������½���� dbadmin@192.168.1.100  ��
create user client@localhost  identified by 'password'

4.����Ȩ��
grant all on minigame.* to client@localhost;

5.�鿴����ip       ipconfig /all
�ҵ� ipv4��Ӧ��

6.�� Config/Config �ļ��޸� hostΪ����ip

7.���� GateServer/GateServer

8.������TestClient/Client���в���

