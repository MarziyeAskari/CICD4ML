import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score
import skops.io as sio
# pip install skops
# pip install numpy
# pip uninstall scikit-learn -y
# pip install scikit-learn==1.3.2

drug_df = pd.read_csv("Data/drug200.csv")
drug_df = drug_df.sample(frac=1)
drug_df.head(3)

X = drug_df.drop(columns="Drug", axis=1).values
y = drug_df["Drug"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=125)


cat_str = [1, 2, 3]
cat_num = [0, 4]
new_pipline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),  # optional for RandomForest
    ]
)
transform = ColumnTransformer(
    [
        ("encoder", OrdinalEncoder(), cat_str),
        ("num_scaler", new_pipline, cat_num)]
)



pipe = Pipeline(
    steps=[
        ("preprocessing", transform),
        ("model", RandomForestClassifier(random_state=125, n_estimators=100)),
    ]
)
pipe.fit(X_train, y_train)


prediction = pipe.predict(X_test)
accuracy = accuracy_score(y_test, prediction)
f1 = f1_score(y_test, prediction, average="macro")

print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

with open("Results/metrics.txt", "w") as f:
    f.write(f"/nAccuracy : {round(accuracy, 2) * 100}% /n F1 : {round(f1, 2)}.\n")
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, prediction, labels=pipe.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe.classes_)
disp.plot()
plt.savefig("Results/model_results.png", dpi=120)

sio.dump(pipe, "Model/drug_pipeline.skops")
#obj = sio.load("Model/drug_pipeline.skops", trusted=True)
