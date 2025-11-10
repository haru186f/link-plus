from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import ReceivedEmail # models.pyからのインポートを想定

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