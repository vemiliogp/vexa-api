"""Email service module."""

from dataclasses import dataclass
from os import getenv

from emails import html


@dataclass
class Attachment:
    """Attachment class for email attachments."""

    filename: str
    path: str


@dataclass
class SendMailOptions:
    """Options for sending an email."""

    to: str
    subject: str
    html_body: str
    attachments: list[Attachment] = None


@dataclass
class EmailService:
    """Service to handle email sending."""

    smtp_config = {
        "host": getenv("MAILER_HOST"),
        "port": int(getenv("MAILER_PORT", "465")),
        "ssl": getenv("MAILER_SSL", "True") == "True",
        "user": getenv("MAILER_USER"),
        "password": getenv("MAILER_PASSWORD"),
    }

    def send_email(self, options: SendMailOptions) -> bool:
        """
        Send an email with the given options.
        """
        message = html(
            html=options.html_body,
            subject=options.subject,
            mail_from=self.smtp_config["user"],
        )

        for att in options.attachments or []:
            with open(att.path, "rb") as f:
                message.attach(
                    filename=att.filename,
                    content=f.read(),
                    maintype="application",
                    subtype="octet-stream",
                )

        try:
            message.send(
                to=options.to,
                smtp=self.smtp_config,
            )
            return True
        except Exception as e:
            raise e
