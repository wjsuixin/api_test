# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2021/12/3 15:12
import os,sys,time
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from util.handle_ini import handle_ini
from util.handle_log import Logger
logger=Logger(logger="SendEmail").getlog()

class SendEmail:
    #自动发送邮件
    def send_email(self,new_report):
        #读取测试报告中的内容作为邮件的内容
        with open(new_report,'rb') as f:
            mail_body = f.read().decode("utf-8")
        #发件人地址
        from_addr = handle_ini.get_value("from_addr","email")
        #收件人地址
        to_addr =handle_ini.get_value("to_addr","email")
        #发送邮箱的服务器地址
        mail_server = handle_ini.get_value("mail_server","email")
        #邮件的标题
        subject = handle_ini.get_value("subject","email")
        #邮箱的内容和标题
        body = MIMEText(mail_body, 'html', 'utf-8')
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, charset='utf8')
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr )
        msg['Date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")
        msg.attach((body))
        file_name = new_report.split("/")[-1]
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = f'attachment; filename={file_name}'
        msg.attach(att)
        smtp= smtplib.SMTP()
        smtp.connect(mail_server)  # 连接 qq 邮箱
        smtp.login(from_addr, handle_ini.get_value("authorization_code","email"))  # 账号和授权码
        #发送邮件
        smtp.sendmail(from_addr,to_addr.split(','),msg.as_string())
        logger.info("邮件发送成功，请查收！")
        smtp.quit()

    #获取最新报告的地址
    def acquire_report_address(self,reports_address):
        #测试报告文件夹中的所有文件加入到列表
        test_reports_list = os.listdir(reports_address)
        #按照升序排序生成新的列表
        new_test_reports_list = sorted(test_reports_list)
        #获取最新的测试报告
        the_last_report = new_test_reports_list[-1]
        #最新的测试报告的地址
        the_last_report_address = os.path.join(reports_address,the_last_report)
        return the_last_report_address

send_email=SendEmail()
if __name__ == '__main__':
    send=SendEmail()
    reports_address=base_path+"\\report"
    send.send_email(send.acquire_report_address(reports_address))
