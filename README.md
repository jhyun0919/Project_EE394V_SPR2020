# Optimal Power Flow Project - EE 394V SPR 2020

This is a repository managing report files and experiment codes implementing the contents covered in [[1]](https://ieeexplore.ieee.org/document/8810819).  
If possible, further studies will be covered.

---

### Contents
#### Reports
- [Project Proposal](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/proposal.pdf). 
- [Project Presentation Slides](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/presentation.pptx). 
- [Project_Final_Report](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/final_report.pdf). 

#### Codes
- [DC-OPF solver](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/experiments/matpower7.0/dc_opf_solver.m). 
- [Data Pre-processing](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/experiments/1.%20Build_Dataset_for_NNs.ipynb). 
- [Multi-Label Classification NNs](https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/codes/experiments/2.%20Classifier%20NNs.ipynb). 

---
### Project Progress
- [X] Complete the proposal. 
- [X] Build a DC-OPF solver.
- [X] Pre-process the given datasets.   
- [X] Build a Neural Nets Classifier. 
- [X] Tune the hyper-parameters.  
- [X] Visualize the training process & test result.
- [X] Prepare for the presentation.
- [ ] Finalize the report.
---

## Brief Description of the Project

### Optimal Power Flow
Optimal power flow is used in power system operational planning to estimate the most economical efficiency solution while satisfying demand and safety margins. 

### Problem definition
- Due to increasing uncertainty and variability in energy sources and demand, the optimal solution needs to be updated near real-time to respond to observed uncertainty realizations.
- The existing methods, such as affine control policy [2][3][4] and ensemble control policy [6][7], could not cope with frequent updating due to the high computational complexity.
- The use of machine learning to learn the mapping from uncertainty realization to the optimal solution (direct mapping) struggles when the size of the training dataset is not large enough.

### Main Contributions

- Propose the use of neural network as a classifier to enable extremely low computational complexity compared to the traditional method. 
- Choose to learn the mapping from uncertainty realization to active constraints set at optimality instead of directly map to the adjustment in the generation, which will guarantee the satisfactory performance of the neural net classifier.

<p align="center">
  <img src="https://github.com/jhyun0919/OPF_Porject_EE394V_SPR2020/blob/master/report/figure/trad_vs_propsed.png?raw=true" height="350">
  <br>
    <em>Fig. 1: Traditional Methods vs. The Proposed Method.</em>
</p>


### Experiments
For following numerical experiments steps, we will use dataset from the [IEEE PES PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf) [8].

- Set up OPF test-cases for the learning.
- Check probability distribution of active sets of different OPF test-cases.
- Observation of the change of accuracy according to the number of layers of fully connected layer (FCN).
- Check accuracy of active set top-K classification for different test cases with change in training data set size.

### Further Studies (Optional)

- [X] **Change the Classifier from single-label to multi-label ver.** to predict the status of individual constraints separately, which will be an approach to develop a deeper understanding of various operational patterns, such as clustering of constraints.  
- [ ] Extending the proposed method to AC OPF with non-linear variations.


---

## References

[1] D. Deka and S. Misra. “Learning for DC-OPF: Classifying active sets using neural nets,” 2019 IEEE Milan PowerTech,2019.  
[2] B. Borkowska, “Probabilistic load flow,” IEEE Transactions on Power App. Syst., vol. PAS-93, no. 3, pp. 752–759, 1974.   
[3] M. Vrakopoulou, K. Margellos, J. Lygeros, and G. Andersson, “Probabilistic Guarantees for the N-1 Security of Systems with Wind Power Generation,” in Probabilistic Methods Applied to Power Systems (PMAPS), Istanbul, Turkey, 2012.   
[4] L. Roald, S. Misra, T. Krause, and G. Andersson, “Corrective control to handle forecast uncertainty: A chance constrained optimal power flow,” IEEE Trans. Power Systems, vol. 32, no. 2, pp. 1626–1637, 2017.   
[5] L. Roald, S. Misra, M. Chertkov, and G. Andersson, “Optimal power flow with weighted chance constraints and general policies for generation control,” in IEEE Conference on Decision and Control (CDC). IEEE, 2015, pp. 6927–6933.   
[6] Y. Ng, S. Misra, L. A. Roald, and S. Backhaus, “Statistical learning for DC optimal power flow,” Jan. 2018.   
[7] S. Misra, L. Roald, and Y. Ng, “Learning for convex optimization,” arXiv preprint arXiv:1802.09639, 2018.     
[8] The IEEE PES Task Force on Benchmarks for Validation of Emerging Power System Algorithms, “PGLib Optimal Power Flow Bench-marks,” Published online at https://github.com/power-grid-lib/pglib-opf, accessed: April 3, 2020.  
