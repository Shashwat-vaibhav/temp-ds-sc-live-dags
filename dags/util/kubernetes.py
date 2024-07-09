from enum import Enum, unique

from airflow.kubernetes.secret import Secret


@unique
class SCAISecrets(Enum):
    tpu_secret_volume = Secret(
        deploy_type="volume",
        deploy_target="/root/.gcp/",
        secret="ds-composer-psc-sa",
        key="ds-composer-psc-sa.json",
    )

    # plz dont use frs_secret_volume this service account is not available
    frs_secret_volume = Secret(
        deploy_type="volume",
        deploy_target="/root/.gcp/",
        secret="feed-relevance-service-sa",
        key="feed-relevance-service-sa.json",
    )


class Nodepool:
    def __init__(
        self, nodepool, name, location, secret, tolerations=None, namespace="default"
    ):
        self.nodepool_name = nodepool
        self.cluster_name = name
        self.location = location
        self.namespace = namespace
        self.secret = secret
        self.tolerations = tolerations
        # self.toleration = None
        # self.node_selector


@unique
class NodespoolList(Enum):
    n1_highmem_32_cluster = Nodepool(
        {"cloud.google.com/gke-nodepool": "highmem-v1"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "highmem",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    m1_ultramem_80_new_cluster = Nodepool(
        {"cloud.google.com/gke-nodepool": "ultramem-node-pool-new"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "ultramem-new",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    ffm_train_new_cluster = Nodepool(
        {"cloud.google.com/gke-nodepool": "ffm-train-new"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "ffm-train-new",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    # This is used by ranker team for training a control model. Please don't use without consent.
    n1_standard_96_cluster = Nodepool(
        {"cloud.google.com/gke-nodepool": "ffm-train-v2"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "ffm-train-v2",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    n1_standard_16_cluster_gpu = Nodepool(  # gpu used
        {"cloud.google.com/gke-nodepool": "sc-p-ds-training-tpu-cluster-n1-16-gpu"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "nvidia.com/gpu",
                "operator": "Equal",
                "value": "present",
                "effect": "NoSchedule",
            }
        ],
    )

    m1_megamem_96_node_pool = Nodepool(  # gpu used
        {"cloud.google.com/gke-nodepool": "m1-megamem-96"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "nodepool",
                "operator": "Equal",
                "value": "megamem",
                "effect": "NoSchedule",
            }
        ],
    )

    n1_standard_16_cluster_cpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-standard-16-cpu"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "n1-standard-16-cpu",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    n1_highmem_96_cluster_gpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-highmem-96"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "service",
                "operator": "Equal",
                "value": "megamem",
                "effect": "NoSchedule",
            },
        ],
    )

    cast_pool_cpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-standard-16-cpu"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
    )

    cast_pool_asia_south = Nodepool(
        {"cloud.google.com/gke-nodepool": "cast-pool-cpu"},
        "sc-p-ds-training-cluster-2",
        "asia-south1",
        SCAISecrets.tpu_secret_volume,
    )

    n1_highmem_32_tpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-highmem-32-tpu"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "n1-highmem-32-tpu",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )

    n1_standard_16_four_t4_gpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-standard-16-four-t4-gpu"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "n1-standard-16-four-t4-gpu",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            },
            {
                "key": "nvidia.com/gpu",
                "operator": "Equal",
                "value": "present",
                "effect": "NoSchedule",
            },
        ],
    )

    n1_standard_96_cpu = Nodepool(
        {"cloud.google.com/gke-nodepool": "n1-standard-96"},
        "sc-p-ds-training-tpu-cluster-1",
        "us-central1",
        SCAISecrets.tpu_secret_volume,
        [
            {
                "key": "n1-standard-96",
                "operator": "Equal",
                "value": "true",
                "effect": "NoSchedule",
            }
        ],
    )
