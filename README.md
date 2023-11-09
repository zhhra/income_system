# income system

This system computes staff's incomes.

Each staff's daily income is computed based on two parts:
1- A base increase or decrease amount
2- projects done per day
So the daily income for each staff would be the summation of mentioned parts above.


# project setup

1. Update set_env_variables.sh file with the correct values.
2. Run set_env_variables.sh file
2. Run "pip install -r requirements.txt".
3. Run "python manage.py migrate".
4. Run "python manage.py runserver".
5. Run "celery -A core worker -l info -B" to run both celery worker and celery beat.
