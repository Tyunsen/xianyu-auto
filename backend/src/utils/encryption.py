"""
Cookie 加密工具
"""
import base64
from cryptography.fernet import Fernet
import hashlib
import os


class CookieEncryptor:
    """Cookie 加密器"""

    def __init__(self, key: str = None):
        """
        初始化加密器

        Args:
            key: 加密密钥，如果未提供则从环境变量或生成
        """
        if key is None:
            key = os.getenv("ENCRYPTION_KEY")

        if not key:
            # 生成一个密钥（开发环境使用）
            key = Fernet.generate_key().decode()
            print(f"警告: 未设置 ENCRYPTION_KEY，已生成新密钥: {key[:20]}...")
            print("生产环境请设置环境变量 ENCRYPTION_KEY")

        if isinstance(key, str):
            key = key.encode()

        # 确保密钥是有效的 Fernet 密钥（32字节 base64 编码）
        try:
            self.cipher = Fernet(key)
        except Exception:
            # 如果不是有效密钥，使用密码派生
            key = hashlib.sha256(key).digest()
            self.cipher = Fernet(base64.urlsafe_b64encode(key))

    def encrypt(self, data: str) -> str:
        """
        加密数据

        Args:
            data: 要加密的明文

        Returns:
            加密后的字符串
        """
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        解密数据

        Args:
            encrypted_data: 加密的字符串

        Returns:
            解密后的明文
        """
        if not encrypted_data:
            return ""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            print(f"解密失败: {e}")
            return ""


# 全局加密器实例
_encryptor = None


def get_encryptor() -> CookieEncryptor:
    """获取全局加密器实例"""
    global _encryptor
    if _encryptor is None:
        _encryptor = CookieEncryptor()
    return _encryptor
