#!/bin/sh
set -e
runtime=$1
folder=$2

gcloud config list account
if test -f "/root/.gcp/ds-tpu-sa.json"; then
    gcloud auth activate-service-account --key-file=/root/.gcp/ds-tpu-sa.json
    export GOOGLE_APPLICATION_CREDENTIALS=/root/.gcp/ds-tpu-sa.json
fi

if test -f "/root/.gcp/ds-composer-psc-sa.json"; then
    gcloud auth activate-service-account --key-file=/root/.gcp/ds-composer-psc-sa.json
fi
gcloud config list account

echo "Downloading data files from eval table to gcs"
bq extract --destination_format PARQUET --compression GZIP maximal-furnace-783:sc_livestream_data.eval_sc_live_feed_multi_obj_ranker  gs://sharechat-prod-bigquery-data/$folder/$runtime/data/*.parquet
echo "Downloading data files from gcs to local"
gsutil -m cp -r gs://sharechat-prod-bigquery-data/$folder/$runtime/data/ ./

echo "Downloading Model files"
sh download_model.sh
echo "Downloaded Model Files"

echo "Evaluation Begins"
python3 eval.py v4
echo "Evaluation Done"

echo "Uploading Results Message to GS"
gsutil -m cp -r offline_eval_message_v4 gs://sharechat-prod-bigquery-data/$folder/$runtime/
echo "Done Uploading"

echo "Appending the results in BQ Table for Superset Chart"
bq load --autodetect --replace=false --source_format=CSV maximal-furnace-783:sc_livestream_data.ranker_model_alerts ./alerts_v4.csv
echo "All Done!"
