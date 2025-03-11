# AsyncMailBot

AsyncMailBot — это простой и эффективный бот для получения email-сообщений в мессенджере Телеграм, который использует асинхронный подход для повышения производительности. Он может быть использован для сортировки, отслеживания и получения в требуемом формате email-сообщений ваших почтовых ящиков.

## Функции

- Асинхронная отправка email-сообщений
- Поддержка различных форматов сообщений (текстовые, HTML, файлы)
- Настройка IMAP-соединения
- Логирование отправленных уведомлений
- Модульная архитектура для легкого расширения

## Установка

Чтобы установить AsyncMailBot, выполните следующие шаги:

1. Склонируйте репозиторий:
bash
git clone https://github.com/sergey-brovko/AsyncMailBot.git
cd AsyncMailBot

2. Установите необходимые зависимости:
bash
pip install -r requirements.txt

## Использование

Чтобы запустить AsyncMailBot, выполните следующую команду:
bash
cd docker
docker-compose up --build

## Вклад

Если вы хотите внести изменения в проект, следуйте этим шагам:

1. Fork данного репозитория.
2. Создайте новую ветку (`git checkout -b feature-branch`).
3. Внесите свои изменения и выполните commit (`git commit -m 'Добавил новую функцию'`).
4. Отправьте свои изменения в репозиторий (`git push origin feature-branch`).
5. Создайте Pull Request.

Спасибо, что выбрали AsyncMailBot! Если у вас есть вопросы или предложения, не стесняйтесь обращаться!
