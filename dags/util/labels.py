from util.pod_name import Pod


def get_cost_labels(
        pod,
        service, # this should be dag_name, and not dag_full_name
        id, # this should be task_id
        entity="sharechat",
        cloud="gcp",
        environment="prod",
        component="airflow-composer",
        team="ds-sc-feed",
        platform="sharechat",
):
    '''
    Returns a dictionary of cost label key-values. Most parameters have defaults that are likely valid for
    all workloads in this repo.
    The caller needs to provide:
        pod: value of the Pod enum. If it's not a member, an assertion error will be raised.
        service: name of the service associated with this workload. Might be the DAG name.
        id: Likely the DAG name or the task name if the granularity is needed.
    '''
    assert isinstance(pod, Pod), 'The pod parameter must by from the enum Pod, found = {}'.format(pod)
    return {
        'pod': pod.value,
        'service': service,
        'id': id,
        'entity': entity,
        'cloud': cloud,
        'environment': environment,
        'component': component,
        'team': team,
        'platform': platform
    }


def get_cost_labels_dataflow(
        pod,
        service,
        id="sc-prod-ds-ranker-airflow-asia",
        entity="sharechat",
        cloud="gcp",
        environment="prod",
        component="composer",
        team="ds",
):
    '''
    This function returns cost labels associated with dataflow jobs 
    Dataflow jobs require the text to be of lenght 64
    The text should only be made up of lower case letters, numbers, _ , -
    '''

    assert isinstance(pod, Pod), 'The pod parameter must by from the enum Pod, found = {}'.format(pod)
    labels = {
        'pod': pod.value,
        'service': service,
        'id': id,
        'entity': entity,
        'cloud': cloud,
        'environment': environment,
        'component': component,
        'team': team
    }
    return {k: v[:63] for k, v in labels.items()}