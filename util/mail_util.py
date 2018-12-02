from os.path import basename
from email.utils import COMMASPACE
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from util.util import parse_config
import smtplib
from util.util import init_logging


class MailUtil(object):

    def __init__(self):
        self.__logging = init_logging()
        self.__mail_cfg = parse_config()

    def send_email(self, receivers, subject, body, files=None):
        try:

            self.__logging.debug("Yaml Config: %s", self.__mail_cfg)
            sender = self.__mail_cfg['mail']['email']

            msg = MIMEMultipart()

            msg['From'] = sender
            msg['To'] = COMMASPACE.join(receivers)
            msg['Subject'] = subject

            msg.attach(MIMEText(body))

            for f in files or []:
                with open(f, "rb") as temp_file:
                    part = MIMEApplication(
                        temp_file.read(),
                        Name=basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

            server = smtplib.SMTP_SSL(self.__mail_cfg['server']['server_address'], self.__mail_cfg['server']['port'])
            server.login(sender, self.__mail_cfg['mail']['password'])
            server.sendmail(sender, receivers, msg.as_string())
            server.quit()
        except Exception as e:
            msg = 'Error while sending email in Mail Service: {}!'.format(e)
            self.__logging.error(msg)
