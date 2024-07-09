#!/bin/sh
DOCKERNAME="sc_live_feed_ranker_eval"
gcloud config set project sharechat-production
docker build -t $DOCKERNAME .
docker tag $DOCKERNAME gcr.io/sharechat-production/$DOCKERNAME:newcomposer
docker push gcr.io/sharechat-production/$DOCKERNAME:newcomposer
