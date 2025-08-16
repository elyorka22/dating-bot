#!/bin/bash

echo "🚀 Подготовка к деплою в Railway..."

# Проверяем наличие Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

# Проверяем наличие Railway CLI
if ! command -v railway &> /dev/null; then
    echo "⚠️ Railway CLI не установлен."
    echo "Установите Railway CLI: npm install -g @railway/cli"
    echo "Или используйте веб-интерфейс Railway"
fi

# Инициализируем Git репозиторий (если нужно)
if [ ! -d ".git" ]; then
    echo "📁 Инициализируем Git репозиторий..."
    git init
    git add .
    git commit -m "Подготовка к деплою в Railway"
    echo "✅ Git репозиторий инициализирован"
else
    echo "📁 Git репозиторий уже существует"
    git add .
    git commit -m "Обновление для Railway деплоя"
fi

# Проверяем файлы
echo "📋 Проверяем необходимые файлы..."
required_files=("Procfile" "runtime.txt" "main_railway.py" "config_railway.py" "requirements.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file найден"
    else
        echo "❌ $file не найден"
        exit 1
    fi
done

echo ""
echo "🎉 Проект готов к деплою в Railway!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте репозиторий на GitHub"
echo "2. Загрузите код: git remote add origin YOUR_GITHUB_REPO"
echo "3. Отправьте код: git push -u origin main"
echo "4. Перейдите на railway.app"
echo "5. Создайте новый проект"
echo "6. Подключите GitHub репозиторий"
echo "7. Настройте переменные окружения"
echo "8. Дождитесь деплоя"
echo ""
echo "📖 Подробные инструкции в файле RAILWAY_DEPLOYMENT.md" 