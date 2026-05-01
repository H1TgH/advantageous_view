import logging
import smtplib
from email.mime.text import MIMEText

from settings import settings


logger = logging.getLogger(__name__)


class EmailService:
    def send(self, to_email: str, subject: str, body: str) -> None:
        """Отправляет plain text письмо. Вызывается синхронно из Celery-воркера."""
        cfg = settings.smtp

        if not cfg.user or not cfg.from_email:
            logger.warning("SMTP не настроен, пропускаем отправку на %s", to_email)
            return

        message = MIMEText(body, "plain", "utf-8")
        message["Subject"] = subject
        message["From"] = cfg.from_email
        message["To"] = to_email

        try:
            with smtplib.SMTP_SSL(cfg.host, cfg.port) as server:
                server.login(cfg.user, cfg.password.get_secret_value())
                server.sendmail(cfg.from_email, to_email, message.as_string())

            logger.info("Письмо отправлено на %s, тема: %s", to_email, subject)

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP: ошибка авторизации. Проверь SMTP_USER и SMTP_PASSWORD")
        except smtplib.SMTPException as e:
            logger.error("SMTP: ошибка отправки на %s: %s", to_email, e)
        except OSError as e:
            logger.error("SMTP: не удалось подключиться к %s:%d — %s", cfg.host, cfg.port, e)
