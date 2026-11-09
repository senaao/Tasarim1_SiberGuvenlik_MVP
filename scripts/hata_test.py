"""Gemini bağlantı denemesi. API anahtarı kaynak kodda saklanmaz.

Windows PowerShell'de yalnızca bu terminal oturumu için:
    $env:GEMINI_API_KEY = "ANAHTARINIZ"
    $env:GEMINI_MODEL = "KULLANDIGINIZ_MODEL"

Ardından proje ana dizininde:
    python scripts/hata_test.py

Not: Bu dosya veri seti üretim pipeline'ının bir parçası değildir.
"""

import os

import requests


def main():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    model = os.environ.get("GEMINI_MODEL", "").strip()

    if not api_key:
        print("GEMINI_API_KEY tanımlı değil. Anahtarı dosyaya yazmayın.")
        return
    if not model:
        print("GEMINI_MODEL tanımlı değil. Kullanılabilir model adını ortam değişkenine yazın.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": "In one sentence, define cybersecurity."}]}],
        "generationConfig": {"temperature": 0.2},
    }
    try:
        response = requests.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
            timeout=30,
        )
        print("HTTP durum kodu:", response.status_code)
        if response.ok:
            print("Bağlantı başarılı.")
        else:
            # Servis yanıtı kimlik doğrulama ayrıntılarını içerebilir;
            # test çıktısında hassas bilgileri basmıyoruz.
            print("Bağlantı başarısız. Anahtarı ve model ayarlarını kontrol edin.")
    except requests.RequestException as exc:
        print(f"Bağlantı hatası: {type(exc).__name__}")


if __name__ == "__main__":
    main()
