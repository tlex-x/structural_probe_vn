Files needed:
- requirement.txt
- elmo.py
- en_ewt-ud-{train, dev, test}.raw
- lm_weights.hdf5 (https://github.com/allenai/allennlp/tree/main/test_fixtures/elmo)
- options.json

A few changes to run this experiment in 2025

# A. The allen nlp library only support until python 3.8 so have to install that and run >python: Create Environment

# B. Use ElmO.py instead of original script

# C. Requirement.txt
- json doesnt need to be installed
- allennlp will cause some trouble to install bc essentially you are building it not extracting it. might have to install low level independencies first (below)

# D. Couldn't install Allennlp
Okay, so ChatGPT suggest these, which worked

## 1. Upgrade pip + wheel + setuptools

These errors often go away if you have modern packaging tools:

pip install --upgrade pip setuptools wheel

## 2. Install the low-level dependencies first

Instead of letting AllenNLP build them from source, pull prebuilt wheels:

pip install spacy==3.2.4
pip install cymem==2.0.6 murmurhash==1.0.6 preshed==3.0.6 thinc==8.0.15

## 3. Then install AllenNLP

For Python 3.8, a stable choice is:

pip install allennlp==2.10.1

## 4. Verify

python -c "import allennlp; print(allennlp.__version__)"

You should see 2.10.1.

