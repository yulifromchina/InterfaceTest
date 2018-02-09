import time,sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import  unittest
from db_fixture import test_data
import time


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