A LIGHT PYTHON RULE ENGINE

[Description]
This engine can not noly help to check the rules, but also help to find the best candidate rules which might miss some values. For example, a patient might not have sufficient exams, casing no rule matched. In such a case, the doctors should recommend the patient additional exams. But which exams would be the best? This engine can help to figure out this problem. 

本规则引擎不仅可以判断输入是否符合一定的规则，也可以推荐那些缺少判断值, 但最有可能成为决策规则、接下来花费的代价最小、且最具共享效益的规则。

[Example]
The examples please to ref to example.py

[Features]
- Rhombus: to instantiate a judement with some conditions. Usually, a Rhombus object is related to a variable/feature, and each condition is related to a branch.

- Rule: a set of Rhombus objects.

- RuleMap: is responsible for check rules and recommend candidate rules.

