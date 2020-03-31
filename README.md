# OPF Project EE 394V SPR2020

This is a repository managing a report and codes that implements the contents covered in [[1]](https://ieeexplore.ieee.org/document/8810819).


### Optimal Power Flow
Optimal power flow is used in power system operational planning to estimate the most economical efficiency solution while satisfying demand and safety margins. 

### Problem definition
- Due to increasing uncertainty and variability in energy sources and demand, the optimal solution needs to be updated near real-time to respond to observed uncertainty realizations.
- The existing method of solving the optimal problem could not cope with frequent updating due to the high computational complexity.

### Main Contribution

- Propose the use of neural network as a classifier to enable extremely low computational complexity compared to the traditional method. 
- Choose to learn the mapping from uncertainty realization to active constraints set at optimality instead of directly map to the adjustment in the generation, which will guarantee the satisfactory performance of the neural net classifier.

### Experiments
For following numerical experiment steps, we will use dataset from the [IEEE PES PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf).

- Set up OPF Test-cases for the learning
- Check probability distribution of active sets of different OPF test-cases
- Observation of the change of accuracy according to the number of layers of fully connected layer (FCN).
- Check accuracy of active set top-K classification for different test cases with change in training data set size.

### Further Study

- How to extend the proposed method to AC OPF with non-linear variations. 
- Adding a set of parallel binary classifiers to predict the status of individual constraints separately, which will be an approach to develop a deeper understanding of various operational patterns, such as clustering of constraints. 


## References

[1] D. Deka and S. Misra. “Learning for DC-OPF: Classifying active sets using neural nets,” 2019 IEEE Milan PowerTech, 2019.
