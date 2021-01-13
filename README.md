# Natural Selection Model
Simple model for evolution by natural selection, which makes **many** simplifications, and shortcuts.

This small project was undertaken to assist my understanding of object-oriented programming in Python.

## Running
Set permissions, run program: 
```
$ chmod 755 main.py
$ python3 main.py
```

### Modelling: Genetics
* DNA simplified to 16 single nucleobases (A,C,G,T)
* Assumes that a being's phenotype is completely controlled by its genetics - this makes evaluating *fitness* easier

### Modelling: Heritable Variation, Differential Reproduction
* Each being in the initial population has randomly set genetics
* Heritability is modelled with reproduction:
  * Each base of the offspring DNA is picked randomly between both parents
* Differential reproduction:
  * Beings with reproductive advantages have a higher fitness rating
  * Higher fitness correlates to higher rates of survival
  * Which, on average, results in differential reproduction

### Modelling: Fitness
* Fitness is represented as a probability: 0 for unfit, 1 for optimally fit
* Fitness is calculated using the `get_survival_probability()` method
  * closeness of the being's genetics to the specified optimal genetics considered (0-1)
  * result is scaled using the exponential function: `survival_prob = closeness^(exponent), exp >= 1`
  * the higher the exponent, the more selective survivability is (as fitness is graded lower)
  * optimal beings will always be graded optimally fit using this model
* Beings greater than 4 generations old are set to unfit, not progressing to g5

### Modelling: Competition
