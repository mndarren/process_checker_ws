"""
.. currentmodule:: process_checker.notifiers

"""
import smtplib
import yaml


class EmailConfig:

    def __init__(self, yml_config='notifier_config.yml'):
        """
        Read values from config yaml file
        :param yml_config:
        """
        with open(yml_config, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)['email']
            self.host = cfg['host']
            self.port = cfg['port']
            self.username = cfg['username']
            self.password = cfg['password']
            self.recipients = cfg['recipients']


class Email:
    """
    Notification Email server.
    """
    def __init__(self, config: EmailConfig = EmailConfig()):
        """
        Initial Email for notification.
        :param config: Email Authentication info
        """
        self._config = config

    def send(self, subject: str, body: str):
        """
        Send message to recipients.
        :param subject: message subject
        :param body: message body
        :return:
        """
        try:
            smtp_server = smtplib.SMTP(host=self._config.host, port=self._config.port)
            smtp_server.starttls()
            smtp_server.login(self._config.username, self._config.password)

            msg = f'Subject: {subject}\nFrom: {self._config.username}\nTo: {self._config.recipients}\n\n{body}'
            smtp_server.sendmail(self._config.username, self._config.recipients, msg)
        except Exception as e:
            print(str(e))
