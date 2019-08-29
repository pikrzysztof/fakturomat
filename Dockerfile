FROM archlinux/base:latest

WORKDIR /code
RUN pacman -Sy --noconfirm python python-pip texlive-bin texlive-core
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code
EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
