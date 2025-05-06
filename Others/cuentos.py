from __future__ import annotations

import random
import requests
import os
import json

from datetime import datetime
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

def _prompt(**kwargs):
   
    prompt = """
    Eres un escritor de cuentos, crea para mi un cuento acerca de un planeta desierto, lleno de magia. 
"""
    kwargs['ti'].xcom_push(key='prompt', value=prompt)

def _generate_text_completion(**kwargs):
    """
    Generates text completion using the specified API.

    Args:
        api_url: The URL of the API endpoint.
        api_key: The API key for authorization.
        model: The model to use for text generation (default: "amazon.titan-text-express-v1").
        message: The message to send to the model (default: "Hello AWS!").

    Returns:
        The JSON response from the API, or None if an error occurs.
        Prints an error message to the console if the request fails.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ["API_KEY"]}"
    }

    data = {
        "model": "amazon.titan-text-express-v1",
        "messages": [
            {
                "role": "user",
                "content": kwargs['ti'].xcom_pull(task_ids='prompt', key='prompt')
            }
        ]
    }


    response = requests.post(f"{os.environ["API_URL"]}/chat/completions", headers=headers, data=json.dumps(data))
    # Grabar el resultado:
    now = datetime.now()
    id = now.strftime("%Y-%m-%d-%H%M%S")

    with open(f"{os.environ["AIRFLOW_HOME"]}/data/story-{id}.txt", "w") as f:
        f.write(response.json())


with DAG(
    dag_id="generador_de_cuentos",
    start_date=datetime(2025, 2, 19),
    schedule=None,
    catchup=False,
) as dag:
    
    start = EmptyOperator(task_id="inicio")

    prompt = PythonOperator(
        task_id="prompt",
        python_callable=_prompt,
        provide_context=True,
    )

    story = PythonOperator(
        task_id="story",
        python_callable=_generate_text_completion,
        provide_context=True,
    )

    end = EmptyOperator(task_id="end")

    start >> prompt >> story >> end