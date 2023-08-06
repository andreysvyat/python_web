FROM python:3
WORKDIR /home
CMD git clone https://github.com/andreysvyat/python_web.git app
CMD cd app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "task_tracker/manage.py", "runserver", "--noreload"]