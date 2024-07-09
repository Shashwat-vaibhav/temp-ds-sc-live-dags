import os
import sys
from datetime import datetime

import pandas as pd
import xgboost as xgb
from config.config import version_expt_variant_map, version_feature_map
from sklearn.metrics import roc_auc_score

version = sys.argv[1]
exptId, variant = version_expt_variant_map[version]
print("Evaluation starting for ", version, exptId, variant)
input_features = version_feature_map[version]
labels_columns = ["join_label", "acj_label", "gift_label"]
ranker_scores_columns = [
    "combinedRankerScore",
    "feedModelAcjScore",
    "feedModelJoinScore",
    "feedModelTcmScore",
    "feedModelGiftScore",
]

label_score_map = {
    "join_label": "feedModelJoinScore",
    "acj_label": "feedModelAcjScore",
    "tcm_label": "feedModelTcmScore",
    "gift_label": "feedModelGiftScore",
}


print("Loading data ....")
data = []
extra_columns = ["exptId", "variant"]
for file in os.listdir("data/"):
    data.append(
        pd.read_parquet(
            "data/" + file,
            engine="pyarrow",
            use_threads=True,
            columns=input_features
            + labels_columns
            + ranker_scores_columns
            + extra_columns,
        )
    )
data = pd.concat(data).reset_index(drop=True)
# data = data[(data["exptId"] == exptId) & (data["variant"] == variant)]
print(
    "Data Loaded!, len(data): ", len(data), "with len(features): ", len(input_features)
)
features = data[input_features]
features = features.astype("float32")
labels = data[labels_columns]
ranker_Scores = data[ranker_scores_columns]

predictions = {}
message = f"Offline Online SC Live Rankers Evaluation - {version}\n"

auc_df = pd.DataFrame()
auc_df["time"] = [datetime.now().date(), datetime.now().date()]
auc_df["score_type"] = ["eval", "eval_inference"]
auc_df["version"] = version
for label in labels_columns:
    print(f"for label: {labels[label].value_counts(normalize=True)}")

    prev_model = xgb.Booster()
    prev_model.load_model(
        f"models/multi-objective-{version}/{version}_feed_model_{label}.json"
    )

    predictions[label] = prev_model.predict(
        xgb.DMatrix(features),
        validate_features=False,
        iteration_range=(0, prev_model.best_ntree_limit),
    )

    offline_auc_score = roc_auc_score(labels[label], predictions[label])

    online_auc_score = roc_auc_score(
        labels[label], ranker_Scores[label_score_map[label]]
    )

    auc_df["auc_" + label] = [online_auc_score, offline_auc_score]

    message += (
        label
        + ": AUC Online Model: {:.6f}, AUC Offline Model: {:.6f}".format(
            online_auc_score, offline_auc_score
        )
        + "\n"
    )
print(message)

auc_df.to_csv(f"alerts_{version}.csv", index=False)
f = open(f"offline_eval_message_{version}", "w")
f.write(message)
f.close()
