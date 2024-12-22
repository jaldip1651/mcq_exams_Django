from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Exam, Question, StudentAnswer
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def take_exam_page(request):
    return render(request, 'take_exam.html')


def exam_result_page(request):
    return render(request, 'exam_result.html')


class login_view(APIView):
    def post(self, request, *args, **kwargs):
        print("login__ api called")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful', 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                is_student=True if data['role'] == 'student' else False,
                is_admin=True if data['role'] == 'admin' else False
            )
            print("user--->>", user)
            return Response({'message': 'User register successfully'}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)


class CreateExamAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        exam = Exam.objects.create(
            title=data['title'],
            created_by=request.user
        )
        for question_data in data['questions']:
            Question.objects.create(
                exam=exam,
                text=question_data['text'],
                options=question_data['options'],
                correct_answer=question_data['correct_answer']
            )
        return Response({'message': 'Exam created successfully'}, status=status.HTTP_201_CREATED)


class GetExamQuestionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        exam_id = kwargs['exam_id']
        try:
            exam = Exam.objects.get(id=exam_id)
            questions = exam.questions.all()
            question_list = []
            for question in questions:
                question_list.append({
                    'id': question.id,
                    'text': question.text,
                    'options': question.options
                })
            return Response({
                'exam_id': exam.id,
                'title': exam.title,
                'questions': question_list
            }, status=status.HTTP_200_OK)
        except Exam.DoesNotExist:
            return Response({'error': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)


class TakeExamAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        exam_id = request.data['exam_id']
        exam = Exam.objects.get(id=exam_id)
        answers = request.data['answers']

        if StudentAnswer.objects.filter(student=request.user, exam=exam).exists():
            return Response({'error': 'You have already taken this exam.'}, status=status.HTTP_400_BAD_REQUEST)

        score = 0
        correct_answers = 0
        total_questions = len(exam.questions.all())

        for question in exam.questions.all():
            if answers.get(str(question.id)) == question.correct_answer:
                score += 1
                correct_answers += 1

        passed = correct_answers >= total_questions * 0.5

        student_answer = StudentAnswer.objects.create(
            student=request.user,
            exam=exam,
            answers=answers,
            score=score,
            passed=passed
        )
        print("student_answer--->>", student_answer)

        return Response({'score': score, 'passed': passed,
                         'total_questions': total_questions
                         })


class ExamResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        exam_id = kwargs['exam_id']
        student_answer = StudentAnswer.objects.filter(student=request.user, exam_id=exam_id).first()
        print(request.user)
        print(exam_id)

        if student_answer:
            return Response({
                'score': student_answer.score,
                'passed': student_answer.passed,
            })
        else:
            return Response({'error': 'No exam results found for this student'}, status=status.HTTP_404_NOT_FOUND)
