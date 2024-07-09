#!/bin/bash

download_model() {
  model_dir=$1
  model_group=$2
  echo "Downloading Model Dir: $model_dir"

  saved_models_path="./models/${model_group}"
  mkdir -p $saved_models_path
  if [ ! -z "$model_dir" ]; then
    gsutil -m -q cp -r "${model_dir}*json" "${saved_models_path}"
  fi

  echo "Downloaded Model Dir: $model_dir in $model_group"
}

model_path=$(gsutil cat gs://sharechat-prod-bigquery-data/live_feed_ranker_v4/multi_obj_v4)
model_group="multi-objective-v4"
download_model $model_path $model_group
