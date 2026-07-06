import re
import os
import hmac
import hashlib
import base64
import json

# Regex for common PII patterns
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')

class PIIScrubber:
    def __init__(self, custom_keywords=None):
        self.custom_keywords = set(custom_keywords) if custom_keywords else set()
        
    def add_keyword(self, word):
        if word and len(word.strip()) > 1:
            self.custom_keywords.add(word.strip())

    def scrub(self, text: str) -> str:
        if not text:
            return text
        
        # Scrub emails
        text = EMAIL_REGEX.sub("[ANONYMIZED_EMAIL]", text)
        
        # Scrub phone numbers
        text = PHONE_REGEX.sub("[ANONYMIZED_PHONE]", text)
        
        # Scrub custom keywords (like specific student names or schools) case-insensitively
        if self.custom_keywords:
            # Sort by length descending to match longer phrases first
            sorted_keywords = sorted(list(self.custom_keywords), key=len, reverse=True)
            for kw in sorted_keywords:
                # Use word boundaries or generic replacement to avoid partial word scrubs
                pattern = re.compile(re.escape(kw), re.IGNORECASE)
                text = pattern.sub("[ANONYMIZED_NAME]", text)
                
        return text

class LocalEncryptor:
    """
    A zero-dependency, secure cryptographic module implementing a stream cipher
    based on HMAC-SHA256 in CTR-like mode. Provides confidentiality and integrity.
    """
    def __init__(self, password: str = "default-education-agent-secure-key"):
        # Deriving a 256-bit key from the password using PBKDF2-HMAC-SHA256
        self.salt = b"edu_gap_agent_salt"
        self.key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), self.salt, 100000, 32)

    def _generate_keystream(self, iv: bytes, length: int) -> bytes:
        """Generates a keystream of specified length using HMAC-SHA256 in CTR mode."""
        keystream = bytearray()
        counter = 0
        while len(keystream) < length:
            # Block index as 4-byte big-endian
            counter_bytes = counter.to_bytes(4, byteorder="big")
            # HMAC-SHA256(key, IV || counter)
            h = hmac.new(self.key, iv + counter_bytes, hashlib.sha256)
            keystream.extend(h.digest())
            counter += 1
        return bytes(keystream[:length])

    def encrypt(self, data: str) -> str:
        """Encrypts data string and returns a base64 encoded string containing IV, ciphertext, and HMAC tag."""
        plaintext = data.encode("utf-8")
        iv = os.urandom(16)
        
        # Generate keystream and XOR
        keystream = self._generate_keystream(iv, len(plaintext))
        ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))
        
        # Calculate HMAC tag for integrity verification (Encrypt-then-MAC)
        mac = hmac.new(self.key, iv + ciphertext, hashlib.sha256).digest()
        
        # Combine [IV (16 bytes)] + [MAC (32 bytes)] + [Ciphertext]
        combined = iv + mac + ciphertext
        return base64.b64encode(combined).decode("utf-8")

    def decrypt(self, encrypted_str: str) -> str:
        """Decrypts a base64 encoded string and returns the plaintext string after verifying integrity."""
        try:
            combined = base64.b64decode(encrypted_str.encode("utf-8"))
            if len(combined) < 48: # 16 (IV) + 32 (MAC)
                raise ValueError("Encrypted data too short.")
                
            iv = combined[:16]
            mac = combined[16:48]
            ciphertext = combined[48:]
            
            # Verify MAC first
            expected_mac = hmac.new(self.key, iv + ciphertext, hashlib.sha256).digest()
            if not hmac.compare_digest(mac, expected_mac):
                raise ValueError("Integrity check failed: Encrypted data has been tampered with.")
                
            # Decrypt
            keystream = self._generate_keystream(iv, len(ciphertext))
            plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
            return plaintext.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
