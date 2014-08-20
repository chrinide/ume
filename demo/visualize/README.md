```
$ cat sample.csv
"x","A","B"
1,1,4
2,2,5
3,3,6
4,4,8
5,5,10
6,6,20
7,7,30

$ cat sample.json
{
    "datasource": {
        "df": "./sample.csv"
    },
    "plotdata": [
        {
            "plot": [
                {
                    "X": "x",
                    "y": "A",
                    "source": "df",
                    "plot_type": "line",
                    "params": {
                        "linewidth": 0.5,
                        "markersize": 4,
                        "color": [0.8, 0.1, 0.1]
                    }
                },
                {
                    "X": "x",
                    "y": "B",
                    "source": "df",
                    "plot_type": "line",
                    "params": {
                        "linewidth": 0.5,
                        "markersize": 4,
                        "color": [0.1, 0.8, 0.1]
                    }
                }
            ],
            "ax_param": {
                "xlim": [0, 200],
                "xlabel": "average bid price",
                "ylabel": "average bid price",
                "grid": "True"
            }
        },
        {
            "plot": [
                {
                    "X": "x",
                    "y": "A",
                    "source": "df",
                    "plot_type": "scatter",
                    "params": {
                        "linewidth": 0.5,
                        "markersize": 4,
                        "color": [0.8, 0.1, 0.1]
                    }
                },
                {
                    "X": "x",
                    "y": "B",
                    "source": "df",
                    "plot_type": "scatter",
                    "params": {
                        "linewidth": 0.5,
                        "markersize": 4,
                        "color": [0.1, 0.8, 0.1]
                    }
                }
            ],
            "ax_param": {
                "xlim": [0, 200],
                "xlabel": "average bid price",
                "ylabel": "average bid price",
                "grid": "True"
            }
        }
    ]
}

$ ume visualize --json ./sample.json --output ./result.png

$ display ./result.png
```
