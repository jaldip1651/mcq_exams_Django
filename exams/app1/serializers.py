from rest_framework import serializers
from .models import Exam, Question, StudentAnswer


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'created_by', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'options', 'correct_answer']


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['student', 'exam', 'answers', 'score', 'passed']
