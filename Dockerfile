FROM archlinux/base:latest

RUN echo "pl_PL.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
RUN pacman -Sy --noconfirm python python-pip texlive-bin texlive-core gcc
RUN pip3 install Django psycopg2-binary slownie jinja2 uwsgi django-referrer-policy django-csp django-feature-policy

USER http:http
COPY --chown=http:http . /code
WORKDIR /code
CMD ["bash", "-c", "python3 manage.py collectstatic --noinput --clear && exec uwsgi --ini uwsgi.ini"]
