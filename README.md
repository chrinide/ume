Ume
===

My personal framework/toolbox for a data mining task.

This application's main goal is to provide a framework that is able to increase
reproducibility and productivity for a data mining competition on kaggle.com.

Bootstrapping
-------------

Ume requires very strict dependencies, so setting up a new virtual environment for Ume is recommended:

```
$ pwd
/home/smly/workspace/ume
$ ./bootstrap
(snip)
$ source venv/bin/active
$ which python
/home/smly/workspace/ume/venv/bin/python
$ which pip
/home/smly/workspace/ume/venv/bin/pip
$ pip install https://github.com/smly/ume/archive/v2.0.zip
$ source venv/bin/active
$ which ume
/home/smly/workspace/ume/venv/bin/ume
```

Usage
-----

```
$ ls feature.py utils.py
feature.py  utils.py

$ ume feature -n feature -a
$ ume validate -m data/input/model/lr_tfidf.json
$ ume predict -m data/input/model/lr_tfidf.json -o data/working/result/lr_tfidf.csv
$ cat data/input/model/lr_tfidf.json
{
    "model": {
        "class": "sklearn.linear_model.LogisticRegression",
        "params": {
            "C": 1.0
        }
    },
    "features": [
        "data/working/feature.gen_tfidf.mat"
    ],
    "target": {
        "file": "data/working/feature.gen_y.mat",
        "name": "y"
    },
    "idx": {
        "train": {
            "file": "data/working/feature.gen_y.mat",
            "name": "idx_train"
        },
        "test": {
            "file": "data/working/feature.gen_y.mat",
            "name": "idx_test"
        }
    },
    "metrics": {
        "method": "ume.metrics.apk_score",
        "params": { }
    },
    "prediction": {
        "method": "utils.PredictProba",
        "params": { }
    },
    "cross_validation": {
        "method": "ume.utils.kfoldcv",
        "params": {
            "n_folds": 5
        }
    }
}
```

Documentation
-------------

I have no plan to describe how to use this product in details.
If you are interested in it, plase send me pull request :-)
