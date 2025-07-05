from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Test(models.Model):
    TEST_TYPE_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ]

    id = models.AutoField(primary_key=True, help_text="Unique identifier for the test") 
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES, default='private')
    test_limit = models.PositiveIntegerField(default=60, help_text="Time in minutes")
    shuffle_questions = models.BooleanField(default=True, help_text="Shuffle questions in the test")
    is_active = models.BooleanField(default=True, help_text="Is the test currently active")
    expire_at = models.DateTimeField(blank=True, null=True, help_text="Expiration date and time of the test")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests', help_text="User who created the test")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True, help_text="Unique identifier for the question")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', help_text="Test to which the question belongs")
    question_title = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True, help_text="Image associated with the question")
    answer_a = models.CharField(max_length=255)
    answer_b = models.CharField(max_length=255)
    answer_c = models.CharField(max_length=255, blank=True, null=True)
    answer_d = models.CharField(max_length=255, blank=True, null=True)
    correct = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} for Test {self.test.title}"