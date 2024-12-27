from django.contrib import admin
from .models import (
    Activity, MainActivity, LearningActivity, PracticingActivity, AssessmentActivity,
    Exercise, Instruction, Quiz, Question, Choice, Submission, MarksTracker,
    GradingRubric, SelfEfficacy, CommonEfficacyQuestion, Score, Response
)

# Inline models
class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class GradingRubricInline(admin.TabularInline):
    model = GradingRubric
    extra = 1


# Admin for models
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes')
    search_fields = ('title', 'description')
    list_filter = ('duration_minutes',)
    inlines = [GradingRubricInline]


@admin.register(MainActivity)
class MainActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'activity_code', 'mode', 'duration_minutes', 'deadline')
    search_fields = ('activity_name', 'activity_code')
    list_filter = ('mode', 'deadline')


@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'learning_goal', 'is_required')
    search_fields = ('activity_name', 'learning_goal')


@admin.register(PracticingActivity)
class PracticingActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'practice_type', 'is_assessment_related')
    search_fields = ('activity_name', 'practice_type')


@admin.register(AssessmentActivity)
class AssessmentActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'assessment_type', 'max_marks')
    search_fields = ('activity_name', 'assessment_type')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'total_weight', 'is_completed')
    search_fields = ('title', 'description', 'objective')
    list_filter = ('is_completed',)
    inlines = [InstructionInline]


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'exercise', 'weight', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('title',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'total_score', 'is_completed')
    search_fields = ('title', 'description')
    list_filter = ('is_completed',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('activity', 'student', 'submission_file', 'on_time_completion', 'submitted_at')
    search_fields = ('activity__title', 'student__username')
    list_filter = ('on_time_completion',)


@admin.register(MarksTracker)
class MarksTrackerAdmin(admin.ModelAdmin):
    list_display = ('student', 'daily_marks', 'weekly_marks', 'monthly_marks', 'course_wise_marks', 'final_grade')
    search_fields = ('student__username',)


@admin.register(GradingRubric)
class GradingRubricAdmin(admin.ModelAdmin):
    list_display = ('criteria', 'activity', 'weight')
    search_fields = ('criteria', 'activity__title')
    list_filter = ('weight',)


@admin.register(SelfEfficacy)
class SelfEfficacyAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'quiz', 'confidence_score')
    search_fields = ('exercise__title', 'quiz__title')


@admin.register(CommonEfficacyQuestion)
class CommonEfficacyQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_active')
    search_fields = ('question_text',)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('submission', 'total_score', 'feedback')
    search_fields = ('submission__activity__title', 'submission__student__username')


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'selected_choice')
    search_fields = ('user__username', 'quiz__title', 'question__text')
