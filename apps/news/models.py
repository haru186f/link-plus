from django.db import models

class ReceivedEmail(models.Model):
    subject = models.CharField("件名", max_length=255)
    sender = models.EmailField("送信元メールアドレス")
    body = models.TextField("本文")
    message_uid = models.CharField("IMAP UID", max_length=100, unique=True, null=True, blank=True)
    received_at = models.DateTimeField("受信日時", auto_now_add=True)
    is_read = models.BooleanField("既読", default=False)
    # 必要に応じて、HTML本文、添付ファイルのフィールドなどを追加

    def __str__(self):
        return self.subject