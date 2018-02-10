import time,sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import  unittest
from db_fixture import test_data
import time
from util import send_email

global user_list
user_list = ['xxxxx@qq.com']


def send_result(filepath, filename):
    email_obj = send_email.SendEmail()
    email_obj.add_attachment(file_path=filepath, file_name=filename)
    subject = '自动化测试报告'
    content='测试结果见附件'
    email_obj.send_email(user_list,sub=subject,content=content)
    email_obj.close()


test_dir='./interface'
#discover = unittest.defaultTestLoader.discover(test_dir,pattern='*.py')

if __name__=='__main__':
    test_data.init_data()
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/'+now+'_result.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner(stream=fp,title='ConferenceSignSystem Interface Test Report',
                            description="Implementation Example with:")
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='md5_*.py')
    runner.run(discover)
    
    fp.close()
    
    # 发送带附件的邮件
    send_result(filename,now+'_result.html')