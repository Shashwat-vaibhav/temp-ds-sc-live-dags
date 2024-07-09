import os

import requests
from airflow.hooks.base import BaseHook


def task_fail_slack_alert(
    context, mentions=[], slack_connections=[], ignore_default_channel=False
):
    if os.environ["ACTIVE_ENV"] == "PRODUCTION":
        if not ignore_default_channel:
            slack_connections.append("slack")
        slack_msg = """
                :red_circle: Task Failed.
                *Task*: {task}
                *Dag*: {dag}
                *Execution Time*: {exec_date}
                *Log Url*: {log_url}
                """.format(
            task=context.get("task_instance").task_id,
            dag=context.get("task_instance").dag_id,
            exec_date=context.get("execution_date"),
            log_url=context.get("task_instance").log_url,
        )

        curl_msg = '{{"text":"{message}"}}'.format(
            message=" ".join(mentions) + slack_msg
        )
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

        for conn_id in slack_connections:
            slack_webhook_token = BaseHook.get_connection(conn_id).password
            slack_webhook_base_url = BaseHook.get_connection(conn_id).host
            url = slack_webhook_base_url + slack_webhook_token
            requests.post(url, data=curl_msg, headers=headers)
    else:
        if not ignore_default_channel:
            slack_connections.append("slack")
        slack_msg = """
                :red_circle: Task Failed.
                *Task*: {task}
                *Dag*: {dag}
                *Execution Time*: {exec_date}
                *Log Url*: {log_url}
                """.format(
            task=context.get("task_instance").task_id,
            dag=context.get("task_instance").dag_id,
            exec_date=context.get("execution_date"),
            log_url=context.get("task_instance").log_url,
        )

        curl_msg = '{{"text":"{message}"}}'.format(
            message=" ".join(mentions) + slack_msg
        )
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

        for conn_id in slack_connections:
            slack_webhook_token = BaseHook.get_connection(conn_id).password
            slack_webhook_base_url = BaseHook.get_connection(conn_id).host
            url = slack_webhook_base_url + slack_webhook_token
            requests.post(url, data=curl_msg, headers=headers)


def task_success_slack_alert(context, mentions=[], slack_connections=[]):
    if os.environ["ACTIVE_ENV"] == "PRODUCTION":
        slack_connections.append("slack")
        slack_msg = """
                :success_kid: Task succeeded.
                *Task*: {task}
                *Dag*: {dag}
                *Execution Time*: {exec_date}
                *Log Url*: {log_url}
                """.format(
            task=context.get("task_instance").task_id,
            dag=context.get("task_instance").dag_id,
            exec_date=context.get("execution_date"),
            log_url=context.get("task_instance").log_url,
        )

        curl_msg = '{{"text":"{message}"}}'.format(
            message=" ".join(mentions) + slack_msg
        )
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

        for conn_id in slack_connections:
            slack_webhook_token = BaseHook.get_connection(conn_id).password
            slack_webhook_base_url = BaseHook.get_connection(conn_id).host
            url = slack_webhook_base_url + slack_webhook_token
            requests.post(url, data=curl_msg, headers=headers)
    else:
        slack_connections.append("slack")
        slack_msg = """
                        :success_kid: Task succeeded.
                        *Task*: {task}
                        *Dag*: {dag}
                        *Execution Time*: {exec_date}
                        *Log Url*: {log_url}
                        """.format(
            task=context.get("task_instance").task_id,
            dag=context.get("task_instance").dag_id,
            exec_date=context.get("execution_date"),
            log_url=context.get("task_instance").log_url,
        )

        curl_msg = '{{"text":"{message}"}}'.format(
            message=" ".join(mentions) + slack_msg
        )
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}

        for conn_id in slack_connections:
            slack_webhook_token = BaseHook.get_connection(conn_id).password
            slack_webhook_base_url = BaseHook.get_connection(conn_id).host
            url = slack_webhook_base_url + slack_webhook_token
            requests.post(url, data=curl_msg, headers=headers)
