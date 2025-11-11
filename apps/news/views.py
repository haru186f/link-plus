from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from apps.news.models import ReceivedEmail # models.pyからのインポートを想定

import logging
logger = logging.getLogger(__name__) # ロガーを追加

# WebhookのURLにアクセスがあったときに実行される
def receive_email_webhook(request):
    if request.method == 'POST':
        # 外部からのリクエストデータから情報を取得（例：Webhookペイロード）
        email_data = request.POST 

        try:
            # 💡 ここでデータ保存ロジックを実行しています 💡
            ReceivedEmail.objects.create(
                # request.POSTから抽出した値を使ってDBに保存
                subject=email_data.get('subject', 'No Subject'), 
                sender=email_data.get('sender', 'noreply@webhook.com'),
                body=email_data.get('text_body', 'Empty Body') 
            )
            return JsonResponse({'status': 'success'}, status=200)
        
        except Exception as e:
            # データベースエラーなどが発生した場合の応答
            print(f"Error saving email: {e}") 
            return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)
    
    # POSTメソッド以外でアクセスされた場合の応答
    return JsonResponse({'status': 'method not allowed'}, status=405)

# ---------------------------------------------------
# ✨ 画面ビュー ✨
# ---------------------------------------------------
class HomeView(TemplateView):
    """
    ホーム画面用のクラスベースビュー。
    最新のメールデータを取得し、テンプレートに渡す。
    """
    # テンプレートパスを設定
    template_name = 'home/home.html' 

    def get_context_data(self, **kwargs):
        # 1. 親クラスのコンテキストを取得
        context = super().get_context_data(**kwargs)

        # 2. データベース操作を実行
        try:
            # 最新のメール5件を取得するように修正（以前のコードの意図を反映）
            # list() を外してクエリ実行を最適化しても良いですが、ここではシンプルに all() のままにします
            emails = ReceivedEmail.objects.all().order_by('-received_at')[:5]

            # 🚨 以前あったロガーによるデバッグ出力は全て削除 🚨

        except Exception as e:
            # エラーが発生した場合、空のリストを渡す
            # 実際のアプリケーションでは、ここでエラーログを記録すべきですが、今回は削除します
            emails = [] 
            
            # デバッグのために、万が一のDBエラーだけは print で出力しておく
            print(f"FATAL ERROR: Failed to fetch emails: {e}") 

        # 3. メールデータをコンテキストに追加
        context['emails'] = emails
        print(context)
        
        return context