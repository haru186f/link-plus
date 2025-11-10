from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Course, Department

# Create your views here.
class GetDepartmentsView(View):
    """選択された学部に応じて学科リストを返す"""
    def get(self, request, *args, **kwargs):
        college_id = request.GET.get('college_id')
        departments = Department.objects.filter(college_id=college_id).values('id', 'name')
        return JsonResponse(list(departments), safe=False)

class GetCoursesView(View):
    """選択された学科に応じてコースリストを返す"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')
        courses = Course.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse(list(courses), safe=False)


class GetGradesView(View):
    """学科ごとに年制を返す（2年制 / 3年制 / 4年制）"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')

        # 特定の学科で分岐（3年制、4年制度）
        THREE_YEAR_DEPARTMENTS = [
            # デザインカレッジ
            'ゲームクリエイター科（3年制）'
            'デザイン科（3年制）',
            'CG映像科（3年制）',

            # スポーツ・医療カレッジ
            'スポーツトレーナー科（3年制）',
            'スポーツ健康学科（3年制）',
            '鍼灸科（3年制）',
            '柔道整復科（3年制）',
        ]
        FOUR_YEAR_DEPARTMENTS = [
            # クリエイターズカレッジ
            'マンガ・アニメーション科（4年制）',

            # デザインカレッジ
            'ゲームクリエイター科（4年制）',

            # ITカレッジ
            'ITスペシャリスト科（4年制）',

            # テクノロジーカレッジ
            '建築学科（4年制）',
            '一級自動車整備科（4年制）',
            ]

        try:
            department = Department.objects.get(id=department_id)
            if department.name in FOUR_YEAR_DEPARTMENTS:
                max_grade = 4
            elif department.name in THREE_YEAR_DEPARTMENTS:
                max_grade = 3
            else:
                max_grade = 2
        except Department.DoesNotExist:
            max_grade = 2

        return JsonResponse({'max_grade': max_grade})
