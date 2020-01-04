A LIGHT PYTHON RULE ENGINE

[Description]

This engine can not noly help to check the rules, but also help to find the best candidate rules which might miss some values. For example, a patient might not have sufficient exams, casing no rule matched. In such a case, the doctors should recommend the patient additional exams. But which exams would be the best? This engine can help to figure out this problem. 

本规则引擎不仅可以判断输入是否符合一定的规则，也可以推荐那些缺少判断值, 但最有可能成为决策规则、接下来花费的代价最小、且最具共享效益的规则。

这就像一个医生拿到了一些患者的检查报告，但是根据他的经验（他知道的规则），还不能做出判断，所以就要补充检查，以达到可以做出诊断的目的。一般医生的做法可能是，所有可能的检查都上一遍，然后再去匹配规则。问题是，如果从患者角度出发，我要是只用做一种检查，就有90%以上的比例确诊的话，我是否有必要先把其他检查也做了呢？而且，有两种不同的诊断都可以达到90%的概率，我是不是应该先选择一种更为经济和安全的方式进行检查呢?

针对当前输入的特征向量，以及潜在的目标规则，我们定义了5种指标：
1）历史样本中，通过目标规则能做出判断的比例（比例越高越好）
2）目标规则额外需要补充的检查次数（次数越少越好）
3）目标规则补充检查的总代价（如价格，风险等，越少越好）
4）目标规则所涉及的补充检查，也能辐射到其他潜在规则的数量（即其他规则也依赖这个额外检查，越多越好：当前规则在补充检查后，如果还不能做出判断，这些检查也能更好的帮我们去匹配其他的规则，以减少最终的总代价）
5）目标规则所涉及的补充检查，也能辐射到其他潜在规则，而这些规则在历史样本中，能做出判断的总比例。（越高越好）

现在我们的做法是可以通过以上各个指标做出排序，然后推荐目标规则以及目标规则需要补充的检查/值。

[Example]

The examples please to ref to example.py

[Features]

- Rhombus: to instantiate a judement with some conditions. Usually, a Rhombus object is related to a variable/feature, and each condition is related to a branch.

- Rule: a set of Rhombus objects.

- RuleMap: is responsible for check rules and recommend candidate rules.


[TO DO]

现在我们的做法是可以通过以上各个指标做出排序，然后推荐目标规则以及目标规则需要补充的检查/值。由于这5种指标的差异化，所以很难用一个综合指标去整合这5个指标，给出一个综合推荐。 这个可以深入考虑。
