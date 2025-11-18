from django.views.generic import TemplateView
from django.http import JsonResponse
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
    
# ---------------------------------------------------
# ✨ API ビュー ✨
# ---------------------------------------------------
def api_email_body(request, pk):
    """
    指定された主キー(pk)のメール本文と件名をJSONで返すAPIエンドポイント。
    home.htmlのAJAXリクエストから呼び出されます。
    """
    if request.method == 'GET':
        try:
            # 1. PKに基づいてメールを取得
            email = ReceivedEmail.objects.get(pk=pk)
            
            # 2. データをJSON形式で整形
            data = {
                'subject': email.subject,
                'body': email.body,
            }
            
            # 3. JSONレスポンスを返す
            return JsonResponse(data)
            
        except ReceivedEmail.DoesNotExist:
            # 指定されたIDのメールが見つからない場合
            return JsonResponse({'error': 'Email not found'}, status=404)
        
        except Exception as e:
            # その他のエラーが発生した場合
            logger.error(f"Error fetching email body for PK {pk}: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
            
    # GETメソッド以外でのリクエストを拒否
    return JsonResponse({'error': 'Method not allowed'}, status=405)