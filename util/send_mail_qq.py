# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.header import Header
from email.mime.text import MIMEText

# 用于构建邮件头
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = 'account@qq.com'
password = '邮箱授权码'

# 收信方邮箱
to_addr = 'toaccount@qq.com'

# 发信服务器
smtp_server = 'smtp.qq.com'

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
msg = MIMEText('发送内容', 'plain', 'utf-8')

# 邮件头信息
msg['From'] = Header(from_addr)
msg['To'] = Header(to_addr)
msg['Subject'] = Header('python test')

# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP_SSL(smtp_server)
server.connect(smtp_server, 465)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()
