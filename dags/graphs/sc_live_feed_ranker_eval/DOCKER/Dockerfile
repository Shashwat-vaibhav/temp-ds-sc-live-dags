FROM gcr.io/google.com/cloudsdktool/cloud-sdk
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN pip3 install wurlitzer pandas pyarrow seaborn scikit-learn omegaconf google-cloud-bigquery cloud-tpu-client google-cloud fsspec gcsfs db-dtypes
RUN pip3 install xgboost==1.6.2
RUN pip3 install tqdm

ENV ACTIVE_ENV PRODUCTION

COPY . .
