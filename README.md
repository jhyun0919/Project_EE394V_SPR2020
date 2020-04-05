# OPF Project EE 394V SPR2020

This is a repository managing a report and codes that implements the contents covered in [[1]](https://ieeexplore.ieee.org/document/8810819).  
If possible, further studies will be covered.

---

### Contents
#### Reports
- [X] [Project_Proposal.pdf](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/proposal.pdf)
- [ ] [Project_Final_Report.pdf](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/final_report.pdf)
#### Codes
- [ ] [Implementation Codes](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/tree/master/codes)
- [ ] [Further Study Implementation Codes](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/tree/master/codes) (Optional)

---
### Project Progress
- [X] Complete the [proposal](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/proposal.pdf). (30 MAR 20)
- [X] Build a [data parser](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/pglib-opf-master/data_parser.ipynb). (04 APR 20)
- [ ] [Pre-process dataset](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/experiments/data_preprocess.ipynb) for each test case.
- [ ] Build a [neural nets classifier](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/experiments/classifier.ipynb).
- [ ] Tune the hyper-parameters & visualize the training process.
- [ ] Finalize the report.
- [ ] Prepare for the presentation.
---

## Brief description of the project

### Optimal Power Flow
Optimal power flow is used in power system operational planning to estimate the most economical efficiency solution while satisfying demand and safety margins. 

### Problem definition
- Due to increasing uncertainty and variability in energy sources and demand, the optimal solution needs to be updated near real-time to respond to observed uncertainty realizations.
- The existing method of solving the optimal problem could not cope with frequent updating due to the high computational complexity.

### Main Contributions

- Propose the use of neural network as a classifier to enable extremely low computational complexity compared to the traditional method. 
- Choose to learn the mapping from uncertainty realization to active constraints set at optimality instead of directly map to the adjustment in the generation, which will guarantee the satisfactory performance of the neural net classifier.

### Experiments
For following numerical experiments steps, we will use dataset from the [IEEE PES PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf) [2].

- Set up OPF test-cases for the learning.
- Check probability distribution of active sets of different OPF test-cases.
- Observation of the change of accuracy according to the number of layers of fully connected layer (FCN).
- Check accuracy of active set top-K classification for different test cases with change in training data set size.

### Further Studies (Optional)

- [ ] Extending the proposed method to AC OPF with non-linear variations. 
- [ ] Adding a set of parallel binary classifiers to predict the status of individual constraints separately, which will be an approach to develop a deeper understanding of various operational patterns, such as clustering of constraints. 

---

## References
[1] D. Deka and S. Misra. “Learning for DC-OPF: Classifying active sets using neural nets,” 2019 IEEE Milan PowerTech, 2019.  
[2] The IEEE PES Task Force on Benchmarks for Validation of Emerging Power System Algorithms, “PGLib Optimal Power Flow Bench-marks,” Published online at https://github.com/power-grid-lib/pglib-opf, accessed: April 3, 2020.
