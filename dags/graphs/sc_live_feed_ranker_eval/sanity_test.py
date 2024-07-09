"""
SC Live Feed Ranker Evaluation DAG

"""
import os
from datetime import datetime, timedelta
from functools import partial

import requests
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import (
    GCSToLocalFilesystemOperator,
)
from airflow.models.connection import Connection
from config.config import configuration
from kubernetes.client import models as k8s_models
from operators.bigquery import BigQueryWrapper
from operators.kubernetes import GKEWrapper
from util import slackUtil
from util.alert_tagging import POC
from util.kubernetes import NodespoolList
from util.labels import get_cost_labels
from util.pod_name import Pod

DAG_NAME = "sc_live_feed_ranker_eval"
DAG_FULL_NAME = "PROD_" + DAG_NAME

POC_migration = POC.DEEKSHA_KOUL
mentions = [POC_migration.value]

run_date_time = str("{{ ts }}")
time = str(datetime.utcnow().time())
run_date_time = (
    run_date_time.replace(".", "")
    .replace(":", "")
    .replace("+", "")
    .replace("-", "/")
    .replace("T", "/")
)

task_fail_slack_alert = partial(
    slackUtil.task_fail_slack_alert,
    mentions=["<@U04GY141370>"],
    slack_connections=["slack_live_ranker_eval"],
)


def read_sql_file(file_name, column_names=None, training_table_name=None):
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        sql_command = file.read()
    if column_names is not None:
        sql_command = sql_command.replace("@train_column_names", column_names)
    if training_table_name is not None:
        sql_command = sql_command.replace("@training_table_name", training_table_name)
    return sql_command


default_args = {
    "owner": POC_migration.name,
    "depends_on_past": False,
    "start_date": datetime(2024, 7, 3),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
}

dag = DAG(
    DAG_FULL_NAME,
    schedule_interval=timedelta(days=1),
    tags=[Pod.SC_FEED_LIVE.name],
    user_defined_macros={"project_id": configuration["gcp_projects"]["production"]},
    default_args=default_args,
    on_failure_callback=task_fail_slack_alert,
)

bigquery_project = configuration["bq_connections"]["live"]
bq_wrapper = BigQueryWrapper(dag, bigquery_project)
compute_project = configuration["connections"]["composer_project"]
gke_wrapper = GKEWrapper(dag, compute_project)
node_pool = NodespoolList.n1_highmem_32_tpu.value

dag.doc_md = __doc__


FOLDERNAME_EVAL = "eval_live_feed_ranker"
GCS_BUCKET_NAME = "sharechat-prod-bigquery-data"


def task_success_slack_alert(context, mentions=[], slack_connections=[]):
    if os.environ["ACTIVE_ENV"] == "PRODUCTION":
        slack_msg = """
                {metrics}
                """.format(
            metrics=context.get("ti").xcom_pull(key="model_slack", dag_id=dag.dag_id)
        )

        curl_msg = '{{"text":"{message}"}}'.format(
            message=" ".join(mentions) + slack_msg
        )
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

        for conn_id in slack_connections:
            conn = Connection.get_connection_from_secrets(conn_id)
            slack_webhook_token = BaseHook.get_connection(conn).password
            slack_webhook_base_url = BaseHook.get_connection(conn).host
            url = slack_webhook_base_url + slack_webhook_token
            requests.post(url, data=curl_msg, headers=headers)


task_success_slack_alert = partial(
    task_success_slack_alert,
    mentions=["<@U0608S81C83>"],
    slack_connections=["slack_live_ranker_eval"],
)

with dag:
    end_task = DummyOperator(task_id="end_task")

    eval_data_prep = bq_wrapper.execute_query(
        task_id="SC_Live_Feed_Ranker_EVAL_Data_Preperation",
        write_disposition="WRITE_TRUNCATE",
        timeoutMs=1000 * 60 * 30,
        sql_str=read_sql_file("queries/EVAL.sql"),
    )

    eval_ranker = gke_wrapper.execute_gke_operator(
        task_id="SC_Live_Feed_Ranker_Offline_Online_Comparision",
        cmd=["sh"],
        args=["run_eval.sh", run_date_time, FOLDERNAME_EVAL],
        image="sc-us-armory.platform.internal/sharechat/sc-live-feed-ranker-eval:latest",
        resource=k8s_models.V1ResourceRequirements(
            requests={"memory": "64Gi", "cpu": "2000m"},
            limits={"memory": "100Gi", "cpu": "4000m"},
        ),
        nodepool=node_pool,
        labels=get_cost_labels(
            pod=Pod.SC_FEED_LIVE,
            service=DAG_NAME,
            id="SC_Live_Dollar_Value_Model_Task",
        ),
    )

    slack_alerts_v4 = GCSToLocalFilesystemOperator(
        task_id="send_slack_alert_v4",
        bucket=GCS_BUCKET_NAME,
        object_name=f"{FOLDERNAME_EVAL}/{run_date_time}/offline_eval_message_v4",
        store_to_xcom_key="model_slack",
        on_success_callback=task_success_slack_alert,
        on_failure_callback=task_fail_slack_alert,
    )
    eval_data_prep >> eval_ranker >> slack_alerts_v4 >> end_task
