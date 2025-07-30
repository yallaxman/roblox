import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

class NicknameGenerator:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def generate_nickname(self, style="random", theme="gaming"):
        """
        Генерирует никнейм для Roblox
        
        Args:
            style (str): Стиль никнейма (random, cool, cute, edgy, etc.)
            theme (str): Тема никнейма (gaming, fantasy, space, etc.)
        """
        
        prompt = f"""
        Generate 5 unique and creative nicknames for Roblox game.
        
        Style: {style}
        Theme: {theme}
        
        Requirements:
        - Nicknames must be 3-20 characters
        - ONLY English letters (a-z, A-Z), numbers (0-9) and underscores (_)
        - NO Russian letters, spaces or special characters
        - Unique and memorable
        - Suitable for Roblox gaming platform
        
        Response format:
        1. Nickname1
        2. Nickname2
        3. Nickname3
        4. Nickname4
        5. Nickname5
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Roblox Nickname Generator"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 200,
            "temperature": 0.8
        }
        
        try:
            # Исправляем кодировку в запросе
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # Проверяем кодировку текста
            if not isinstance(generated_text, str):
                generated_text = str(generated_text)
            
            # Принудительно конвертируем в UTF-8
            generated_text = generated_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            # Извлекаем никнеймы из ответа
            nicknames = []
            lines = generated_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('1.') or line.startswith('2.') or 
                           line.startswith('3.') or line.startswith('4.') or line.startswith('5.')):
                    # Убираем номер и точку
                    nickname = line.split('.', 1)[-1].strip()
                    if nickname:
                        # Фильтруем только английские символы
                        filtered_nickname = ''.join(c for c in nickname if c.isalnum() or c == '_')
                        if filtered_nickname and len(filtered_nickname) >= 3:
                            nicknames.append(filtered_nickname)
            
            return nicknames[:5]  # Возвращаем максимум 5 никнеймов
            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к OpenRouter API: {e}")
            return ["ErrorGenerating", "TryAgain", "BotIssue", "CheckAPI", "ContactDev"]
        
        except (KeyError, IndexError) as e:
            print(f"Ошибка при обработке ответа API: {e}")
            return ["ErrorParsing", "TryAgain", "BotIssue", "CheckAPI", "ContactDev"]
        
        except UnicodeEncodeError as e:
            print(f"Ошибка кодировки: {e}")
            return ["UnicodeError", "TryAgain", "BotIssue", "CheckAPI", "ContactDev"]
        
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return ["UnexpectedError", "TryAgain", "BotIssue", "CheckAPI", "ContactDev"]
    
    def generate_custom_nickname(self, user_preference):
        """
        Генерирует никнейм на основе пользовательских предпочтений
        """
        prompt = f"""
        Generate 3 unique nicknames for Roblox based on the following preferences:
        
        User preferences: {user_preference}
        
        Requirements:
        - 3-20 characters
        - ONLY English letters (a-z, A-Z), numbers (0-9) and underscores (_)
        - NO Russian letters, spaces or special characters
        - Unique and memorable
        
        Response format:
        1. Nickname1
        2. Nickname2
        3. Nickname3
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Roblox Nickname Generator"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,
            "temperature": 0.9
        }
        
        try:
            # Исправляем кодировку в запросе
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # Проверяем кодировку текста
            if not isinstance(generated_text, str):
                generated_text = str(generated_text)
            
            # Принудительно конвертируем в UTF-8
            generated_text = generated_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            nicknames = []
            lines = generated_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('1.') or line.startswith('2.') or 
                           line.startswith('3.')):
                    nickname = line.split('.', 1)[-1].strip()
                    if nickname:
                        # Фильтруем только английские символы
                        filtered_nickname = ''.join(c for c in nickname if c.isalnum() or c == '_')
                        if filtered_nickname and len(filtered_nickname) >= 3:
                            nicknames.append(filtered_nickname)
            
            return nicknames[:3]
            
        except UnicodeEncodeError as e:
            print(f"Ошибка кодировки при создании кастомных никнеймов: {e}")
            return ["UnicodeError", "TryAgain", "ContactDev"]
        
        except Exception as e:
            print(f"Ошибка при генерации кастомного никнейма: {e}")
            return ["CustomError", "TryAgain", "ContactDev"]