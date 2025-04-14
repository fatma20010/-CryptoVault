import streamlit as st
import math
from typing import Tuple

# ROT3 Encryption/Decryption
def rot3(text: str, encrypt: bool = True) -> str:
    result = []
    shift = 3 if encrypt else -3
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result.append(chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset))
        else:
            result.append(char)
    return ''.join(result)

# ROT13 Encryption/Decryption
def rot13(text: str) -> str:
    result = []
    shift = 13
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result.append(chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset))
        else:
            result.append(char)
    return ''.join(result)

# Vigenère Encryption/Decryption
def vigenere(text: str, key: str, encrypt: bool = True) -> str:
    result = []
    key = key.lower()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - 97
            if not encrypt:
                shift = -shift
            result.append(chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset))
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

# RSA Key Generation, Encryption, and Decryption
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def mod_inverse(e: int, phi: int) -> int:
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("mod_inverse does not exist")

def generate_rsa_keys() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    p, q = 61, 53
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    while math.gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(text: str, public_key: Tuple[int, int]) -> list:
    e, n = public_key
    return [pow(ord(char), e, n) for char in text]

def rsa_decrypt(ciphertext: list, private_key: Tuple[int, int]) -> str:
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

# Streamlit Interface
def main():
    st.set_page_config(
        page_title="Crypto",
        page_icon="🔒",
        layout="centered",
    )

    # Inject CSS for pastel green background
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #c8e6c9 !important;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        border: 2px solid #ffd700;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #81c784;
        border-color: #ffca28;
    }
    .stTextInput>div>input {
        border: 2px solid #ffd700;
        border-radius: 8px;
        padding: 8px;
        background-color: #ffffff;
    }
    .stSelectbox>div {
        border: 2px solid #ffd700;
        border-radius: 8px;
        background-color: #ffffff;
    }
    h1 {
        color: #2e7d32;
        text-align: center;
        font-size: 32px;
        margin-bottom: 20px;
    }
    h2, h3 {
        color: #388e3c;
    }
    .stMarkdown {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ffd700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stWarning {
        background-color: #e8f5e9;
        border-left: 4px solid #ffd700;
        padding: 10px;
        border-radius: 8px;
    }
    .stError {
        background-color: #ffebee;
        border-left: 4px solid #e57373;
        padding: 10px;
        border-radius: 8px;
    }
    .stContainer {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ffd700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔒 CryptoVault")
    st.markdown("💰 Protégez vos messages avec la sécurité d'un coffre-fort numérique.")

    with st.container():
        text = st.text_input("Entrez votre texte :", placeholder="Saisissez votre message...")
        cipher_type = st.selectbox("Sélectionnez un algorithme :", ["ROT3", "ROT13", "Vigenère", "RSA"])
        vigenere_key = st.text_input("Clé Vigenère (si applicable) :", placeholder="Entrez la clé Vigenère...", disabled=cipher_type != "Vigenère")

        if cipher_type == "RSA":
            st.warning("Pour déchiffrer RSA, copiez-collez la liste chiffrée telle qu'elle apparaît après chiffrement, par exemple : [1369, 1632, 884, 2271, 1632].")

        col1, col2 = st.columns(2)
        with col1:
            encrypt_button = st.button("Chiffrer")
        with col2:
            decrypt_button = st.button("Déchiffrer")

        if encrypt_button and text:
            with st.spinner("Chiffrement en cours..."):
                if cipher_type == "ROT3":
                    result = rot3(text, encrypt=True)
                    st.markdown(f"**Texte Chiffré :** {result}")
                elif cipher_type == "ROT13":
                    result = rot13(text)
                    st.markdown(f"**Texte Chiffré :** {result}")
                elif cipher_type == "Vigenère":
                    if vigenere_key and vigenere_key.isalpha():
                        result = vigenere(text, vigenere_key, encrypt=True)
                        st.markdown(f"**Texte Chiffré :** {result}")
                    else:
                        st.error("Veuillez entrer une clé Vigenère valide (lettres uniquement) !")
                elif cipher_type == "RSA":
                    public_key, _ = generate_rsa_keys()
                    result = rsa_encrypt(text, public_key)
                    st.markdown(f"**Texte Chiffré :** {result}")

        if decrypt_button and text:
            with st.spinner("Déchiffrement en cours..."):
                if cipher_type == "ROT3":
                    result = rot3(text, encrypt=False)
                    st.markdown(f"**Texte Déchiffré :** {result}")
                elif cipher_type == "ROT13":
                    result = rot13(text)
                    st.markdown(f"**Texte Déchiffré :** {result}")
                elif cipher_type == "Vigenère":
                    if vigenere_key and vigenere_key.isalpha():
                        result = vigenere(text, vigenere_key, encrypt=False)
                        st.markdown(f"**Texte Déchiffré :** {result}")
                    else:
                        st.error("Veuillez entrer une clé Vigenère valide (lettres uniquement) !")
                elif cipher_type == "RSA":
                    _, private_key = generate_rsa_keys()
                    try:
                        cleaned_text = text.strip().replace(' ', '')
                        if not (cleaned_text.startswith('[') and cleaned_text.endswith(']')):
                            cleaned_text = f"[{cleaned_text}]"
                        ciphertext = [int(x) for x in cleaned_text.strip('[]').split(',') if x]
                        result = rsa_decrypt(ciphertext, private_key)
                        st.markdown(f"**Texte Déchiffré :** {result}")
                    except ValueError:
                        st.error("Format de texte chiffré RSA invalide ! Veuillez copier-coller la liste exacte.")
                    except Exception as e:
                        st.error(f"Erreur lors du déchiffrement RSA : {str(e)}")

    st.markdown("💰 Made By Fatma Hammedi 2025 | Propulsé par Streamlit")

if __name__ == "__main__":
    main()
