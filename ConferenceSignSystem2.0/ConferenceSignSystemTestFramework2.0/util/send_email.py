import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import re


class SendEmail(object):

    global g_send_user
    global g_send_password
    global g_email_host
    g_email_host = 'smtp.sohu.com'
    g_send_user='xxxx@sohu.com'
    g_send_password='xxxxx'
    
    # 连接SMTP服务器
    def __init__(self):
        self.server = smtplib.SMTP()
        self.server.connect(g_email_host)
        self.server.login(g_send_user, g_send_password)
        self.message = MIMEMultipart()
    
    # 填写发件人，收件人，主题，内容后发送
    def send_email(self, user_list,send_user=g_send_user, sub='', content=''):
        pattern = '(.*)@.*'
        send_user = re.match(pattern, send_user).group(1)+'<'+send_user+'>'
        self.message['From'] = Header(send_user,'utf-8').encode()
        self.message['To'] = Header(';'.join(user_list),'utf-8').encode()
        if sub!='':
            self.message['Subject'] = Header(sub,'utf-8').encode()
        if content!='':
            self.message.attach(MIMEText(content,'plain','utf-8'))
    
        try:
            self.server.sendmail(send_user, user_list, self.message.as_string())
            print('发送邮件成功')
        except smtplib.SMTPException:
            print('发送邮件失败')
            self.server.close()
    
    def add_attachment(self, file_path, file_name):
        attachment = MIMEText(open(file_path, 'rb').read(), 'base64','utf-8')
        attachment['Content-Type'] = 'application/octet-stream'
        attachment['Content-Disposition'] = 'attachment;filename="%s"'% file_name
        self.message.attach(attachment)
    
    def close(self):
        self.server.close()


if __name__=='__main__':
    email_obj = SendEmail()
    email_obj.add_attachment(file_path=r'C:\Users\70409\Desktop\test.txt',file_name='test.txt')
    user_list = ['xxxxxx@qq.com']
    email_obj.send_email(user_list)
    email_obj.close()
