import os
from datetime import timedelta
from typing import List

from airflow.providers.google.cloud.operators.kubernetes_engine import (
    GKEStartPodOperator,
)
from kubernetes.client import models as k8s_models
from util.kubernetes import Nodepool


class GKEWrapper:
    def __init__(self, dag, compute_project):
        print("Hello Wrapper; GKE")
        self.dag = dag
        self.compute_project = compute_project

    def execute_gke_operator(
        self,
        task_id: str,
        labels: dict,
        nodepool: Nodepool,
        args: List[str],
        image: str,
        resource: k8s_models.V1ResourceRequirements,
        is_delete_operator_pod: bool = True,
        startup_timeout_seconds: int = 60 * 20 * 2,
        retries: int = 1,
        retry_delay: timedelta = timedelta(minutes=10),
        execution_timeout: timedelta = timedelta(hours=10),
        cmd: List[str] = None,
        custm_env_vars: dict = {},
        do_xcom_push: bool = False,
    ) -> GKEStartPodOperator:

        env_vars = {
            "ACTIVE_ENV": os.environ["ACTIVE_ENV"],
            "GOOGLE_APPLICATION_CREDENTIALS": nodepool.secret.value.deploy_target
            + nodepool.secret.value.key,
        }

        for key, value in custm_env_vars.items():
            env_vars[key] = value

        return GKEStartPodOperator(
            dag=self.dag,
            task_id=task_id,
            project_id=self.compute_project,
            location=nodepool.location,
            # node_selector=nodepool.nodepool_name,
            cluster_name=nodepool.cluster_name,
            name=task_id,
            namespace=nodepool.namespace,
            cmds=cmd,
            tolerations=nodepool.tolerations,
            arguments=args,
            image=image,
            image_pull_policy="Always",
            is_delete_operator_pod=is_delete_operator_pod,
            container_resources=resource,
            secrets=[nodepool.secret.value],
            env_vars=env_vars,
            labels=labels,
            startup_timeout_seconds=startup_timeout_seconds,
            retries=retries,
            retry_delay=retry_delay,
            execution_timeout=execution_timeout,
            get_logs=True,
            do_xcom_push=do_xcom_push,
        )
