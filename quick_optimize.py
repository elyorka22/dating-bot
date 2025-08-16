#!/usr/bin/env python3
import subprocess
import sys

def run_command(command):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🚀 Быстрая оптимизация бота...")
    
    # Команды для оптимизации
    commands = [
        "ssh root@185.23.34.213 'cd /home/botuser/dating_bot && echo \"DATABASE_URL=sqlite:///dating_bot.db\" > .env'",
        "ssh root@185.23.34.213 'cd /home/botuser/dating_bot && echo \"BOT_TOKEN=8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI\" >> .env'",
        "ssh root@185.23.34.213 'systemctl restart dating-bot'",
        "ssh root@185.23.34.213 'systemctl status dating-bot --no-pager'"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"📋 Выполняем шаг {i}/4...")
        success, stdout, stderr = run_command(command)
        
        if success:
            print(f"✅ Шаг {i} выполнен успешно")
            if stdout:
                print(f"📄 Вывод: {stdout[:200]}...")
        else:
            print(f"❌ Ошибка на шаге {i}: {stderr}")
            return False
    
    print("🎉 Оптимизация завершена!")
    print("🚀 Бот теперь должен работать быстрее с SQLite!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 