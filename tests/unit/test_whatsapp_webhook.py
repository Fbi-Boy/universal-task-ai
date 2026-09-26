from backend.channels.whatsapp_webhook import WhatsAppWebhook

def test_challenge_rejects_wrong_token():
    assert WhatsAppWebhook("secret").challenge("wrong","abc").status == 403

def test_challenge_accepts_expected_token():
    assert WhatsAppWebhook("secret").challenge("secret","abc").body == "abc"
