# Creating Artificial Survey Panels using Large Language Models
*Gabriela Kadlecová, Petra Vidnerová, Roman Neruda, Josef Šlerka*

Instructions to run the experiments:

1. Create the artificial panel

Modify experiments.csv to set parameters (`<model_name>` is one of command-r-plus, claude and gpt-4o). Set the api key, output dir and seed.

```
./run_experiments.sh -f experiments.csv -a <your_api_key> -o paper_experiments -s 42 -m <model_name>
```

2. 

```
for res in paper_experiments/*.pkl; do
    echo "------------"
    echo $res
    if [ -f $res.png ]; then
        echo "Skipping $res"
    fi

    python plot_panel.py $res data/soc_distrust.sav --n_sample 10 --title $res
done

```


------------

### SBP-BRiMS

This repository contains code for the SBP-BRiMS 2024 conference working paper. We present two
studies on generating artificial survey panels - German Bundestag elections 2027 and
Czech parliamentary elections 2021.

The paper is a "working paper", meaning that this code is also **work in progress**.
As the code may regularly change, the conference code will be accessible in branch
`sbp-brims` while `main` will contain ongoing work on the project.

## Instructions
First, clone the repository:
```
git clone -b sbp-brims git@github.com:gabikadlecova/panelart.git
```

Install requirements for our project:
```
pip install -r requirements.txt
```

We provide two documented jupyter notebooks for reproducing our experiments: `czech.ipynb`
and `gen_german.ipynb`. If you want to use the `command-r-plus` model, get your 
api key at [Cohere](https://cohere.com/chat) and paste it in corresponding cells.
