FROM archlinux/base:latest

WORKDIR /code
RUN echo "pl_PL.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
RUN pacman -Sy --noconfirm python python-pip texlive-bin texlive-core gcc
RUN pip3 install Django psycopg2-binary slownie jinja2 uwsgi

COPY . /code
EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
