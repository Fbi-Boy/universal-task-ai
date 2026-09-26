from backend.channels.whatsapp_provider import WhatsAppCloudProvider,WhatsAppProviderConfig

class S:
    def get(self,name): return "secret"
class H:
    def post_text(self,*args): return args

def test_provider_uses_secret_provider():
    r=WhatsAppCloudProvider(WhatsAppProviderConfig("https://graph.example","123","wa.token"),H(),S()).send_text("u","hi")
    assert r[2]=="secret"
