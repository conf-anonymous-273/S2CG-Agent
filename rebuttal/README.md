# Common Issues

## Reviewer A/B/C: Limited benckmarks
 
Results: S²CG-Agent vs. GPT-4o on SecCodePLT, 1345 samples in total.

<img width="425" height="97" alt="image" src="https://github.com/user-attachments/assets/c532746a-aef5-4bfb-a62f-908d5d5d58f7" />

Due to time constraints, we only evaluated the performance of S²CG-Agent. S²CG-Agent improved secure coding rate from 57% to 72.19%, improved SA-Pass@1 from 71.15% to 79.63%.
Where the secure coding rate is obtained by the evaluation calculation provided by SecCodePLT.

## Reviewer A/B: Failure cases

**Scheduler missed report:** CWE-295, CWE-339, CWE-477, CWE-601, CWE-611

**LLM repair failed:** CWE-020, CWE-022, CWE-078, CWE-079, CWE-080, CWE-090, CWE-094, CWE-113, CWE-116, CWE-117, CWE-209, CWE-215, CWE-306, CWE-321, CWE-326, CWE-400, CWE-434, CWE-502, CWE-522, CWE-601, CWE-611, CWE-641, CWE-643, CWE-730, CWE-918.

***LLM repair failed case analysis:***

| ID                  | Cause analysis                                               |
| ------------------- | ------------------------------------------------------------ |
| HumanEval/87        | Boundary conditions are not fully processed and all input scenarios are not covered |
| HumanEval/132       | Nested depth calculation logic flaw, insufficient handling of the situation of  “]” |
| CWE-020_codeql_4.py | URL verification regular or whitelist strategies are not strict |
| CWE-078_author_1.py | Lose command verification logic, and the safe subcommand segmentation is not used correctly |
| CWE-918_codeql_1.py | Incomplete implementation of subdomain whitelist function    |
| CWE-020_codeql_1.py | Path concatenation or escape logic does not trigger any safe branches |

***Scheduler missed report case analysis:***

| ID                  | Cause analysis                                               |
| ------------------- | ------------------------------------------------------------ |
| CWE-601_codeql_1.py | No verification was performed on the redirect URL parameters |
| CWE-295_author_1.py | SSL context configuration interface mismatch                 |
| CWE-295_author_2.py | The OpenSSL Context creation process did not trigger an exception path |
| CWE-611_sonar_2.py  | XML parsing does not combine input file                      |

## Reviewer A/C: Statistical testing

We conducted statistical comparisons (p-value and effect size), and the results showed that there were significant differences between S²CG-Agent and baselines in almost all metrics (p<0.05).![截屏 2025-07-25 at 18.28.53@2x](https://p.ipic.vip/2rbxk9.png)![截屏 2025-07-25 at 18.29.22@2x](https://p.ipic.vip/t6l7id.png)![截屏 2025-07-25 at 18.29.54@2x](https://p.ipic.vip/t22q0l.png)

# Reviewer-A

## Question-1

We did experiments on safe priority and function priority and LLM-Agent settings. Experimental results show that when safety is given priority, the SA-Pass@1 increases (98.59%) but the UT-Pass@1 decreases (92.68%); when function is given priority, the UT-Pass@1 increases (95.12%), but the SA-Pass@1 decreases (94.74). While LLM-Agent shows a compromise level in performance on all three metrics, S²CG-Agent outperforms hand-coded-policies and LLM-Agent based methods on all metrics.![截屏 2025-07-25 at 13.37.59@2x](/Users/chenyn/Library/Application Support/CleanShot/media/media_BhTtYP120g/截屏 2025-07-25 at 13.37.59@2x.png)

## Question-2

The output of the checker will be handed over to the "Result Parser" and will not produce ambiguous output. However, we made limitations in prompt, that is, static analysis / fuzzing related modifications can be made without destroying functionality.

## Question-3

Please see common issues.

## Issue-1: Statistical testing 

Please see common issues.

## Issue-2: Limited benchmarks

Please see common issues.

# Reviewer-B

## Question-1

Please see common issues.

## Question-2

The scheduler does not change after training. The scheduler was trained on 2970 samples generated in other benchmarks and already has good predictive capabilities. For fairness in the evaluation, real-time prediction data was not applied to update the scheduler.
In theory, the scheduler can continuously learn feedback through real-time prediction data, especially data with erroneous predictions.

To further prove the effectiveness without scheduler evolution, we extended the S²CG-Agent to a new benchmark, the results shows that the scheduler has good generalization ability, please see common issues.

## Issue-1 Limited benchmarks

Please see common issues.

## Issue-2 Inadequate related-works

We commit to adding the related works.

# Reviewer C

## Issue-1: Results unreliable:

We repeated the S²CG-Agent(GPT-4o) three times, and the results of repeated experiments were stable. In addition, we aggregated the results of the repeated experiments and performed statistical testings. The results showed that there was no significant difference between the paper data and the repeated experiments results, showing the robustness of the results. The results are shown in https://github.com/conf-anonymous-273/S2CG-Agent/tree/main/rebuttal.

![截屏 2025-07-25 at 15.59.44@2x](https://p.ipic.vip/tvkxjn.png)

![截屏 2025-07-25 at 16.03.58@2x](https://p.ipic.vip/r1dgjv.png)

## Issue-2: Unit test & Unfair Setting:

S²CG-Agent is available for unit testing scenarios and is not limited to the IDE. The unit tests used to train the scheduler, give feedback, and ultimately evaluate are separate.

The original LLM that does not provide feedback is the baseline we set. We also set LLM-Agent for baselines, therefore, there is no unfair problem.

## Issue-3: Time-cost:

LLM enhanced code generation methods generally take a long time. For example, ASE'24 Best Paper PairCoder requires an average of 17.57 API calls for a complex problem, while S²CG-Agent only needs an average of 3.9 times.

S²CG-Agent is affected by api call frequency and tool runtime in the working environment, while the original LLM only requires 1 call and is not affected.

## Issue-4: tools:

CodeQL and Bandit are cross-complementary, CodeQL is good at logic vulnerabilities, and Bandit is sensitive to common Python vulnerabilities.
Bear is a static analysis tool as well, and Dai et al. (in https://github.com/conf-anonymous-273/S2CG-Agent/tree/main/rebuttal) did comparative experiments on them, proving that the overall detection coverage of the three is similar.

Dai, S., Xu, J., & Tao, G. (2025). A Comprehensive Study of LLM Secure Code Generation. *ArXiv, abs/2503.15554*.

## Issue-5: Benchmarks:

Please see common issues.
