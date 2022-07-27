FROM ubuntu
RUN apt update
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN mkdir my_django_project
RUN echo $project_folder
RUN ls
COPY ${project_folder} /home/my_django_project
WORKDIR /home/my_django_project/$project_folder
RUN ls
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
EXPOSE 8000
RUN apt install postgresql-client -y
CMD python3 manage.py makemigrations
CMD python3 manage.py migrate
CMD python3 manage.py runserver 0.0.0.0:8000
