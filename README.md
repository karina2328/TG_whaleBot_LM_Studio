# TG_Bot_LM_Studio_example_1
 
Репозиторий содержит скрипт для запуска телеграм бота. 
Для запуска необходимо предварительно установить <a href="https://lmstudio.ai/">LM Studio</a> и 
загрузить с платформы <a href="https://huggingface.co/">Hugging Face</a> языковую модель. 

Также нужно предварительно создать Telegram бота и подключить к проекту.
Создать своего Telegram бота можно с помощью TG бота @BotFather.

## Функциональность бота
* команды: 
   - /start (выводится приветствие и список доступных команд)
   - /model (выводит название используемой LLM)
   - /hello - приветствие
   - /clear - очистка контекста
* запросы пользователя пересылаются LLM, запущеной на этом компьютере, а затем ответ пересылается пользователю

## Особенности бота
LLM запоминает контекст в рамках текущей переписки и отвечает на запрос пользователя с учётом сохранённой информации. 


