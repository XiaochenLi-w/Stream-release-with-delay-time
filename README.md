# Delay-allowed Differentially Private Data Stream Release

Tested Python version: 3.11.4

numpy and matplotlib is required.


### Evaluation

To evaluate any method, set

```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time)
```

 Simply run:

```
python ./release/est_compall.py
```
The results and the graphs will be directly output to the screen.


### Sensitivity Truncation Mechanism

To use the sensitivity truncation mechanism, you can set the parameter `Flag=1`, `interval`  refers to the number of data batches between updates, `num_`  is specifically used by CompOrder as the length of each data batch.
```
est_sens_opt(ex, domain_low, domain_high, epsilon_list, round_, tau, buc_size, delay_time, flag = 1, interval_ = 5, num_ = 100)
```




