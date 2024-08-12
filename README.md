# SBP-BRiMS '24 - Creating Artificial Survey Panels Is Still Difficult
*Gabriela Kadlecová, Petra Vidnerová, Roman Neruda, Josef Šlerka*

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
