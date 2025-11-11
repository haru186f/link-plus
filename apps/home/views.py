from django.views.generic import TemplateView
import logging

# ロガーを追加
logger = logging.getLogger(__name__)

# 🚨 必須: 他のアプリのモデルをインポート 🚨
# 正しいアプリ名とモデル名に修正してください
try:
    from apps.news.models import ReceivedEmail 
    from apps.lecture.models import Lecture 
    from apps.bus.models import BusSchedule  
except ImportError as e:
    logger.critical(f"FATAL: Required models failed to import for MasterHomeView: {e}")
    # 開発環境でモデルが存在しない場合でも実行を継続できるように、ダミーを用意
    class ReceivedEmail: objects = type('M', (object,), {'all': lambda: []}) 
    class Lecture: objects = type('M', (object,), {'all': lambda: []}) 
    class BusSchedule: objects = type('M', (object,), {'all': lambda: []}) 


# ---------------------------------------------------
# ✨ 画面ビュー（データを集約した司令塔）✨
# ---------------------------------------------------
class MasterHomeView(TemplateView):
    """
    ホーム画面用のクラスベースビュー。
    ニュース、レクチャー、バスのデータを集約し、テンプレートに渡す。
    """
    template_name = 'home/home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🚨 データ集約ロジック開始 🚨
        
        # 1. ニュースデータ
        try:
            # 最新のメール5件を取得
            context['news_emails'] = ReceivedEmail.objects.all().order_by('-received_at')[:5]
            logger.info(f"Fetched {len(context['news_emails'])} news emails.")
        except Exception as e:
            logger.error(f"ERROR: Failed to fetch NEWS emails: {e}", exc_info=True)
            context['news_emails'] = [] 
            
        # 2. レクチャーデータ
        try:
            # 例: 最新の公開済みレクチャー3件を取得
            context['latest_lectures'] = Lecture.objects.all().order_by('-created_at')[:3]
            logger.info(f"Fetched {len(context['latest_lectures'])} lectures.")
        except Exception as e:
            logger.error(f"ERROR: Failed to fetch LECTURE data: {e}", exc_info=True)
            context['latest_lectures'] = [] 

        # 3. バスデータ
        try:
            # 例: 今日のバス運行予定を取得
            context['bus_schedules'] = BusSchedule.objects.all().order_by('time')[:4]
            logger.info(f"Fetched {len(context['bus_schedules'])} bus schedules.")
        except Exception as e:
            logger.error(f"ERROR: Failed to fetch BUS data: {e}", exc_info=True)
            context['bus_schedules'] = []
            
        # ------------------------------------
        
        return context