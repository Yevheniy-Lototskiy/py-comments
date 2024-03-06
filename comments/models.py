from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=63)
    email = models.EmailField()
    homepage = models.URLField(null=True, blank=True)
    text = models.TextField()
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return f"id: {self.id} {self.username}: {self.text[:50]}..."
