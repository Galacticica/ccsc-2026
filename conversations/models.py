from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Conversation {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        super().save(*args, **kwargs)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=255)  # e.g., "user" or "ai"
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:50]}..."