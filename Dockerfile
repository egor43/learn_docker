FROM python:3.7

# Создание группы пользователей uwsgi
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask uWSGI requests redis
WORKDIR /app
COPY app /app
# Добавление файла скрипта в контейнер
COPY cmd.sh /

# Использование EXPOSE для объявления портов, доступных для хоста и других контейнеров
EXPOSE 9090 9191
# Определение имени пользователя uwsgi для всех последующих строк (включая CMD и ENTRYPOINT)
USER uwsgi
# вызов скрипта из инструкции CMD
CMD ["/cmd.sh"]
