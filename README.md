# OPF Project EE 394V SPR2020

This is a repository that manages the report and the code file that implements the contents covered in [[1]](https://ieeexplore.ieee.org/document/8810819).


## Abstract

Optimal power flow is used in power system operational planning to estimate the most economical efficiency solution while satisfying demand and safety margins. Due to increasing uncertainty and variability in energy sources and demand, the optimal solution needs to be updated near real-time to respond to observed uncertainty realizations. However, the existing method of solving the optimal problem could not cope with frequent updating due to the high computational complexity. To address this issue, a method was proposed to learn the map- ping between the uncertainty realization and the active constraints set at optimality. In this paper, we propose the use of neural networks as a classifier learning the mapping between the uncertainty realization and the active constraints set at optimality, which has an extremely low computational complexity. Through numerical experiments, we demonstrate the remarkable performance of this approach on systems in the [IEEE PES PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf).



## References

[1] D. Deka and S. Misra. “Learning for DC-OPF: Classifying active sets using neural nets,” 2019 IEEE Milan PowerTech, 2019.
