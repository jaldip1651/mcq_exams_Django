from django.urls import path
from .views import login_view, UserRegisterAPIView, CreateExamAPIView, TakeExamAPIView, ExamResultAPIView, login_page, register_page, take_exam_page, exam_result_page, GetExamQuestionsAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login_page/', login_page, name='login-page'),
    path('register_page/', register_page, name='user-register'),
    path('take_exam_page/', take_exam_page, name='take-exam'),
    path('exam_result_page/<int:exam_id>/', exam_result_page, name='exam-result'),

    # ---------------above for design------------------------

    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', login_view.as_view(), name='user-login'),
    path('create_exam/', CreateExamAPIView.as_view(), name='create-exam'),
    path('exam_questions/<int:exam_id>/', GetExamQuestionsAPIView.as_view(), name='exam_questions'),

    path('take_exam/', TakeExamAPIView.as_view(), name='take-exam'),
    path('exam_result/<int:exam_id>/', ExamResultAPIView.as_view(), name='exam-result'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
