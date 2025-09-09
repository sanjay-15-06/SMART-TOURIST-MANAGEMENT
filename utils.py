# File: utils.py
from cryptography.fernet import Fernet

# Generate encryption key (run once)
# key = Fernet.generate_key()
# print(key)

KEY = b'YOUR_32_BYTE_KEY_HERE_________'  # Replace with generated key
fernet = Fernet(KEY)

def encrypt_text(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token):
    return fernet.decrypt(token.encode()).decode()

# Multilingual support (sample)
LANGUAGES = {
    "en": {"SOS": "SOS Alert", "IllegalZone": "Entered Restricted Zone"},
    "hi": {"SOS": "एसओएस चेतावनी", "IllegalZone": "प्रतिबंधित क्षेत्र में प्रवेश"},
    "bn": {"SOS": "SOS সতর্কতা", "IllegalZone": "নিষিদ্ধ অঞ্চলে প্রবেশ"}
}

def translate(key, lang="en"):
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)

if __name__ == "__main__":
    encrypted = encrypt_text("Emergency")
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypt_text(encrypted))
    print("Translation (hi):", translate("SOS", "hi"))
