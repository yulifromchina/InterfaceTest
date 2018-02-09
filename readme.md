# ConferenceSignSystem

### 发布会签到系统及对应的测试框架1.0

|——ConferenceSignSystem1.0发布会签到系统

|——ConferenceSignSystemTestFramwork1.0对应的测试框架以及接口测试用例

介绍：**<u>1.0版本</u>**是学习了测试专家虫师的《Web接口开发与自动化测试--基于Python语言》，并模仿完成的项目，功能包括：

- 完整的发布会签到系统（登录、发布会管理、嘉宾管理、签到功能）
- 项目Web接口
- 接口测试用例

### 发布会签到系统及对应的测试框架2.0

|——ConferenceSignSystem2.0发布会签到系统

|——ConferenceSignSystemTestFramwork2.0对应的测试框架以及接口测试用例

介绍：**<u>2.0版本</u>**对以下进行了完善

1.优化项目接口，所有接口增加HTTP BASIC认证；测试框架中的接口测试用例增加相应测试

HTTP BASIC认证：使用"username:password"进行base64编码

2.优化项目接口，所有接口增加超时验证和md5摘要认证(去掉HTTP BASIC 认证)；测试框架中的接口测试用例增加相应测试

超时验证：服务端接受请求的时间server_time > 客户端发送的时间client_time+60s,则超时拒绝请求

md5摘要认证：”client_time+约定的密钥“计算md5

### Python版本与依赖库：

python3.6

django 2.0.1

requests 2.18.4

django-bootstrap3-9.1.0

