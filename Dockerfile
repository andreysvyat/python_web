FROM python:3.11.4
WORKDIR /home
RUN git clone https://github.com/andreysvyat/python_web.git app
RUN ls -l
WORKDIR /home/app
RUN ls -l
RUN pip install --no-cache-dir -r requirements.txt
RUN python task_tracker/manage.py migrate
CMD ["python", "task_tracker/manage.py", "runserver", "--noreload", "0.0.0.0:8000"]