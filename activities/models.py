from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Activity(models.Model):
    ACTIVITY_CATEGORY_CHOICES = [
        ('Technical Knowledge', 'Technical Knowledge'),
        ('Skill Development', 'Skill Development'),
        ('Workplace Readiness', 'Workplace Readiness'),
        ('Assessment', 'Assessment'),
        ('Problem-Solving', 'Problem-Solving'),
        ('Industry-Specific', 'Industry-Specific'),
        ('Creative and Design', 'Creative and Design'),
        ('Self-Learning', 'Self-Learning'),
        ('Collaborative', 'Collaborative'),
        ('Reflective and Feedback', 'Reflective and Feedback'),
    ]

    """
    Represents a learning or training activity.
    """
    title = models.CharField(max_length=200, verbose_name="Activity Title")
    activity_name = models.CharField(max_length=200)
    activity_code = models.CharField(max_length=10, unique=True, verbose_name="Activity Code")
    description = models.TextField(help_text="Instructions or steps to complete the activity.")
    activity_name = models.CharField(max_length=200)
    activity_code = models.CharField(max_length=10, unique=True, verbose_name="Activity Code")    
    instructions = models.TextField(help_text="Detailed instructions for solving the activity.")
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration_minutes = models.PositiveIntegerField(
        default=30, 
        help_text="Countdown time in minutes.",
        verbose_name="Duration (minutes)"
    )
    no_of_sessions = models.PositiveIntegerField(default=1, verbose_name="Number of Sessions")

    def __str__(self):
        return self.title




class MainActivity(models.Model):
    """
    Base model for all types of main activities.
    """
    ACTIVITY_TYPES = [
        ('Exercise', 'Exercise'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
        ('Demonstration', 'Demonstration'),
        ('Lecture', 'Lecture'),
        ('Group', 'Group'),
    ]

    MODE_TYPES = [
        ('Online', 'Online'),
        ('Video', 'Video'),
        ('Physical', 'Physical'),
    ]

    activity = models.ForeignKey(Activity, related_name='activities', on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    activity_code = models.CharField(max_length=10)
    description = models.TextField()
    mode = models.CharField(max_length=10, choices=MODE_TYPES)
    duration_minutes = models.FloatField(help_text="Duration in minutes")
    deadline = models.DateTimeField(help_text="Submission deadline")
    efficacy_questions = models.ManyToManyField('CommonEfficacyQuestion', blank=True)

    def __str__(self):
        return self.activity_name

class LearningActivity(MainActivity):
    """
    Model for learning-related activities.
    """
    learning_goal = models.TextField(help_text="Learning goal or outcome.")
    is_required = models.BooleanField(default=True, help_text="Whether this activity is mandatory.")

    def __str__(self):
        return f"Learning Activity: {self.activity_name}"

class PracticingActivity(MainActivity):
    """
    Model for practice-related activities.
    """
    practice_type = models.CharField(max_length=100, help_text="Type of practice (e.g., Individual, Group).")
    is_assessment_related = models.BooleanField(default=False, help_text="Linked to assessments.")

    def __str__(self):
        return f"Practicing Activity: {self.activity_name}"

class AssessmentActivity(MainActivity):
    """
    Model for assessment-related activities.
    """
    ASSESSMENT_TYPES = [
        ('MCQ', 'MCQ'),
        ('Presentation', 'Presentation'),
        ('Project', 'Project'),
        ('Demonstration', 'Demonstration'),
        ('Assignment', 'Assignment'),
    ]

    assessment_type = models.CharField(max_length=100, choices=ASSESSMENT_TYPES)
    max_marks = models.FloatField(help_text="Maximum marks for the assessment.")

    def __str__(self):
        return f"Assessment Activity: {self.activity_name}"

class Exercise(models.Model):
    """
    Represents an exercise within an activity.
    """
    title = models.CharField(max_length=200, verbose_name="Exercise Title")
    description = models.TextField()
    objective = models.TextField(verbose_name="Exercise Objective")
    total_weight = models.FloatField(default=0.0, verbose_name="Total Weight")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    is_completed = models.BooleanField(default=False, verbose_name="Completed")

    def __str__(self):
        return self.title

class Instruction(models.Model):
    """
    Represents instructions for completing an exercise.
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="instructions")
    title = models.CharField(max_length=200, verbose_name="Instruction Title")
    text = models.TextField(verbose_name="Instruction Text")
    weight = models.FloatField(verbose_name="Weight (%)")
    is_completed = models.BooleanField(default=False, verbose_name="Completed")

    def __str__(self):
        return f"{self.title} ({self.exercise.title})"

class Quiz(models.Model):
    """
    Represents a quiz related to an activity.
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    total_score = models.IntegerField(default=0, verbose_name="Total Score")
    is_completed = models.BooleanField(default=False, verbose_name="Completed")

    def __str__(self):
        return self.title

class Question(models.Model):
    """
    Represents a question within a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(verbose_name="Question Text")
    weight = models.FloatField(default=1.0, verbose_name="Weight (%)")

    def __str__(self):
        return self.text

class Choice(models.Model):
    """
    Represents a choice for a quiz question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, verbose_name="Choice Text")
    is_correct = models.BooleanField(default=False, verbose_name="Correct Answer")

    def __str__(self):
        return self.text

class Submission(models.Model):
    """
    Represents a submission for an exercise.
    """
    activity = models.ForeignKey(Activity, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    submission_file = models.FileField(upload_to='submissions/', verbose_name="Uploaded File")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Time")
    marks = models.FloatField(null=True, blank=True, help_text="Marks awarded.")
    feedback = models.TextField(null=True, blank=True, help_text="Optional feedback.")
    end_time = models.DateTimeField(null=True, blank=True)
    on_time_completion = models.BooleanField(default=False, verbose_name="Submitted On Time")
    exercise = models.ForeignKey(
    Exercise,
    on_delete=models.CASCADE,
    related_name="submissions",
    null=True,
    blank=True
)
    def duration(self):
        if self.end_time and self.submitted_at:
            return (self.end_time - self.submitted_at).total_seconds() / 3600
        return 0.0

    def is_achieved_on_time(self):
        now = timezone.now()
        if now > self.activity.deadline:
            self.on_time_completion = False
            return 'Late'
        elif now < self.activity.deadline:
            self.on_time_completion = True
            return 'Earlier'
        else:
            self.on_time_completion = True
            return 'On Time'

    def __str__(self):
        return f"Submission by {self.student.username} for {self.activity.title}"

class MarksTracker(models.Model):
    """
    Tracks marks and progress for a student.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks')
    daily_marks = models.FloatField(default=0.0)
    weekly_marks = models.FloatField(default=0.0)
    monthly_marks = models.FloatField(default=0.0)
    course_wise_marks = models.FloatField(default=0.0)
    final_grade = models.CharField(max_length=10, blank=True)
    final_assessment_score = models.FloatField(null=True, blank=True)
    tasks_completed = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    on_time_completion = models.BooleanField(default=False)
    practical_hours = models.FloatField(default=0.0)
    theory_hours = models.FloatField(default=0.0)
    num_of_prev_attempts = models.IntegerField(default=0)
    industry_training_experience = models.FloatField(default=0.0)

    def __str__(self):
        return f"Marks Tracker for {self.student.username}"

class GradingRubric(models.Model):
    """
    Represents a rubric for grading activities.
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="rubrics")
    criteria = models.CharField(max_length=255, verbose_name="Criteria")
    excellent_description = models.TextField(blank=True, null=True, verbose_name="Excellent")
    good_description = models.TextField(blank=True, null=True, verbose_name="Good")
    average_description = models.TextField(blank=True, null=True, verbose_name="Average")
    poor_description = models.TextField(blank=True, null=True, verbose_name="Poor")
    weight = models.FloatField(default=1.0, verbose_name="Weight (%)")

    def __str__(self):
        return self.criteria

class SelfEfficacy(models.Model):
    """
    Represents a self-efficacy score for exercises or quizzes.
    """
    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    confidence_score = models.FloatField(default=0.0, verbose_name="Confidence Score")

    def save(self, *args, **kwargs):
        if not (self.exercise or self.quiz):
            raise ValueError("SelfEfficacy must be linked to either an Exercise or a Quiz.")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.exercise:
            return f"Self-Efficacy for {self.exercise.title}"
        elif self.quiz:
            return f"Self-Efficacy for {self.quiz.title}"

class CommonEfficacyQuestion(models.Model):
    """
    Common efficacy questions related to activities.
    """
    question_text = models.CharField(max_length=255, verbose_name="Question Text")
    is_active = models.BooleanField(default=True, help_text="Is this question active?")

    def __str__(self):
        return self.question_text

class Score(models.Model):
    """
    Represents the score for a submission.
    """
    submission = models.OneToOneField(
        Submission, 
        on_delete=models.CASCADE, 
        related_name='score'
    )
    total_score = models.PositiveIntegerField(default=0, verbose_name="Total Score")
    feedback = models.TextField(blank=True, null=True, verbose_name="Feedback")

    def __str__(self):
        return f"Score: {self.total_score} for {self.submission.student.username}"

class Response(models.Model):
    """
    Represents a user's response to a quiz question.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.question.text[:50]}"
