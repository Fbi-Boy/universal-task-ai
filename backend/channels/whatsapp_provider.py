from dataclasses import dataclass

@dataclass(frozen=True)
class WhatsAppProviderConfig:
    api_base_url: str
    phone_number_id: str
    access_token_secret_name: str

class WhatsAppCloudProvider:
    """Provider contract; HTTP transport remains behind an injected client."""
    def __init__(self,config:WhatsAppProviderConfig,http_client,secret_provider):
        if not config.api_base_url.startswith("https://"): raise ValueError("HTTPS required")
        self.config=config; self.http=http_client; self.secrets=secret_provider
    def send_text(self,recipient:str,text:str):
        if not recipient or not text.strip(): raise ValueError("recipient and text are required")
        token=self.secrets.get(self.config.access_token_secret_name)
        return self.http.post_text(self.config.api_base_url,self.config.phone_number_id,token,recipient,text)
