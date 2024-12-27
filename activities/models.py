from django.db import models

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Instructions or steps to do the activity.")
    instructions = models.TextField(help_text="Detailed instructions for solving the activity.")
    duration_minutes = models.PositiveIntegerField(default=30, help_text="Countdown time in minutes.")

    def __str__(self):
        return self.title


class GradingRubric(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="rubrics")
    criteria = models.CharField(max_length=255)
    excellent_description = models.TextField()
    good_description = models.TextField()
    average_description = models.TextField()
    poor_description = models.TextField()
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.criteria





class Submission(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='submissions')
    student_name = models.CharField(max_length=100)
    uploaded_file = models.FileField(upload_to='submissions/')
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.activity.title}"



