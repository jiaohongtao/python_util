import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender = '1007760854@qq.com'
receivers = ['1007760854@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
password = 'QQ授权码'

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("肺炎最新消息", 'utf-8')
message['To'] = Header("肺炎最新消息", 'utf-8')
subject = 'Python SMTP 肺炎最新消息'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('肺炎最新消息', 'plain', 'utf-8'))

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('update.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="肺炎最新消息.txt"'
message.attach(att1)

smtp_server = 'smtp.qq.com'
server = smtplib.SMTP_SSL(smtp_server)
server.login(sender, password)
# 发送邮件
server.sendmail(sender, receivers, message.as_string())
# 关闭服务器
server.quit()
