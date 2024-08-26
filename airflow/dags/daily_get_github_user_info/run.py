from airflow import DAG
from dags.daily_get_github_user_info.user_list import users
from dags.daily_get_github_user_info.collect_the_amount_of_user_repositories import run as get_user_data_request
from airflow.operators.python_operator import PythonOperator # type: ignore
from datetime import datetime, timedelta
import json


dag_name = "daily_get_github_user_info"
default_args = {
    'depends_on_past': False,
    'retries': 1,
    'start_date': datetime.now(),
    'retry_delay': timedelta(minutes=1),

    
}

dag = DAG(
    dag_name,
    default_args= default_args,
    schedule_interval= "@daily",
    max_active_runs= 1,
    catchup= False
)

def get_user_data(**context):
    user_list = []
    for user_number, user_name in enumerate(users):
        print(f"user {user_number + 1}: ", user_name)
        response = get_user_data_request(user_name)
        if response.status_code == 200:
            user_data = response.json()
            print("\nuser data: ", user_data)
            user_list.append(user_data)
        else:
            print(f"Failed to retrieve data for user {user_name}: {response.status_code}")
    context['task_instance'].xcom_push(key='users', value=json.dumps(user_list))

def dumps_user_data(**context):
    users = context['task_instance'].xcom_pull(key='users') or []
    with open('output.json', 'w') as output:
        json.dump(users, output, indent=4, ensure_ascii=False)
    
with (dag):
    get_user_data_task = PythonOperator(
        task_id='get_user_data',
        python_callable=get_user_data,
        dag=dag,
        provide_context=True
    )
    
    dumps_user_data_task = PythonOperator(
        task_id='dumps_user_data',
        python_callable=dumps_user_data,
        dag=dag,
        provide_context=True
    )
    
    get_user_data_task >> dumps_user_data_task