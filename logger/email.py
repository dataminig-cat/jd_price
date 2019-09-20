import smtplib
from email.mime.text import MIMEText
from utils.settings import sender,password

def get_emailclient(sender,password,smtp_server = 'smtp.qq.com'):
    # 发送纯文本格式的邮件
    # smtp服务器
    server = smtplib.SMTP(smtp_server,25)# SMTP协议默认端口是25
    server.starttls()
    server.ehlo()
    server.login(sender,password)#ogin()方法用来登录SMTP服务器
    # server.set_debuglevel(1)#打印出和SMTP服务器交互的所有信息。
    return server

if __name__ == '__main__':
    # 收件箱地址
    # receiver = '1921749915@qq.com'
    receiver = '664006035@qq.com'
    # mailto_list = ['liqiang22230@163.com', '10116340931@qq.com']  # 收件人

    sender = '3317186060@qq.com'  # 发送邮箱地址
    password = 'liytreahlmmicjgg'  # 邮箱授权码，非登陆密码
    server = get_emailclient(sender,password)

    # # 发送邮箱地址
    msg = MIMEText('hello，send by python_test...', 'plain', 'utf-8')
    msg['From'] = sender
    # # 收件箱地址
    msg['To'] = receiver
    # msg['To'] = ';'.join(mailto_list)  # 发送多人邮件写法
    # # 主题
    msg['Subject'] = 'from IMYalost'
    # # 第一个参数为发送者，第二个参数为接收者，可以添加多个例如：['SunshineWuya@163.com','xxx@qq.com',]# 第三个参数为发送的内容
    # server.sendmail(sender,mailto_list,msg.as_string())#msg.as_string()把MIMEText对象变成str server.quit()