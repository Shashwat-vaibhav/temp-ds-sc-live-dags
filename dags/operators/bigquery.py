from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
    BigQueryInsertJobOperator,
)
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import (
    BigQueryToGCSOperator,
)


class BigQueryWrapper:
    def __init__(self, dag, big_query_project_name):
        print("Wrapper Init")
        self.dag = dag
        self.big_query_project = big_query_project_name
        # self.dataset = dataset
        self.use_legacy_sql = False
        self.allow_large_results = True
        self.priority = "BATCH"
        self.query_location = "US"

    def execute_script(
        self,
        task_id: str,
        sql_str: str,
        destination_project: str = None,
    ) -> BigQueryInsertJobOperator:
        """_summary_

        Args:
            task_id (str): name of the task in airflow
            sql_str (str): sql to be run in BQ
            destination_project (str): destination_project in BQ
        Returns:
            BigQueryInsertJobOperator:
        """

        print("Query: ", sql_str)
        operator = BigQueryInsertJobOperator(
            dag=self.dag,
            task_id=task_id,
            project_id=self.big_query_project
            if destination_project is None
            else destination_project,
            location=self.query_location,
            force_rerun=True,
            gcp_conn_id=self.big_query_project,
            configuration={
                "query": {
                    "query": sql_str,
                    "useLegacySql": self.use_legacy_sql,
                    "allowLargeResults": self.allow_large_results,
                    "priority": self.priority,
                }
            },
        )
        return operator

    # Created wrapper for BigQueryExecuteQueryOperator
    def execute_query(
        self,
        task_id: str,
        sql_str: str,
        write_disposition: str = "WRITE_EMPTY",
        destination_dataset_table: str = None,
        pool: str = None,
        timeoutMs: int = 1000 * 60 * 60,
        time_partitioning: dict = None,
        cluster_fields=None,
    ) -> BigQueryExecuteQueryOperator:
        """_summary_

        Args:
            task_id (str): name of the task in airflow
            sql_str (str): sql to be run in BQ
            destination_dataset_table (str): destination table where data to be stored
            write_disposition (str): action if table already exists
        Returns:
            BigQueryExecuteQueryOperator:
        """

        print("Query: ", sql_str)
        operator = BigQueryExecuteQueryOperator(
            task_id=task_id,
            use_legacy_sql=self.use_legacy_sql,
            write_disposition=write_disposition,
            allow_large_results=self.allow_large_results,
            priority=self.priority,
            api_resource_configs={"query": {"timeoutMs": timeoutMs}},
            sql=sql_str,
            gcp_conn_id=self.big_query_project,  # bigquery_conn_id has been deprecated
            create_disposition="CREATE_IF_NEEDED",
            destination_dataset_table=destination_dataset_table,
            time_partitioning=time_partitioning,
            cluster_fields=cluster_fields,
            pool=pool,
            dag=self.dag,
        )
        return operator

    def execute_export(
        self,
        task_id: str,
        source_table: str,
        gcs_destinations: str,
        export_format: str = "PARQUET",
        compression: str = "NONE",
        field_delimiter: str = ",",
    ) -> BigQueryToGCSOperator:
        """_summary_

        Args:
            task_id (str): name of the task in airflow
            source_table (str): source table to export
            gcs_destination (str): destination google cloud storage bucket location
            export_format (str): CSV , PARQUET , JSON , AVRO
            compression (str): GZIP(CSV , JSON , PARQUET) , DEFLATE(AVRO) , SNAPPY(AVRO , PARQUET) , ZSTD(PARQUET)
            field_delimiter (str): used in csv format
        """

        if source_table == "":
            raise Exception("empty source table")
        if gcs_destinations == "":
            raise Exception("empty gcs destination")

        return BigQueryToGCSOperator(
            task_id=task_id,
            gcp_conn_id=self.big_query_project,
            destination_cloud_storage_uris=gcs_destinations,
            source_project_dataset_table=source_table,
            export_format=export_format,
            compression=compression,
            print_header=True,
            field_delimiter=field_delimiter,
            dag=self.dag,
        )
