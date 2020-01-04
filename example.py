# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2020 Nengjun Zhu. All Rights Reserved
# Licensed under the MIT (the "LICENSE")
# 
########################################################################
 
"""
File: example.py
Author: Nengjun Zhu(zhu_nj@sjtu.edu.cn)
Affiliation: Shanghai Jiao Tong University
Date: 2020/01/02 12:23:53
"""

#Examples

#Creating Rhombus
import numpy as np

from rhomb import Rhombus
from rhomb import Rule
from rhomb import RuleMap

print 'Creating  Rhombus ======================='
age = Rhombus(name='age', cost=0.5)
age.add_branch("x >= 50")
age.add_branch("x < 50")
age.print_branches()
print 

sex = Rhombus(name='sex', cost=1)
sex.add_branch("x == 'male'")
sex.add_branch("x == 'female'")
sex.add_branch("x == 'other'")
sex.print_branches()
print 

weight = Rhombus(name='weight', cost=2)
weight.add_branch("x > 65 and x < 80")
weight.print_branches()
print 

edu = Rhombus(name='edu', cost=3)
edu.add_branch("x in ['high', 'middle']")
edu.print_branches()
print 

#Creating Rules
print 'Creating Rules ======================='
ru1 = Rule([(age, 0), (sex, 0), (weight, 0)], 'great', 'ru1', 0.2)
ru2 = Rule([(age, 0), (edu, 0)], 'excellent', 'ru2', 0.8)
ru3 = Rule([(age, 1)], 'excellent', 'ru3', 0.8)

#ru1.check([50, 'male', None])
ru1.print_rule()
ru2.print_rule()
ru3.print_rule()
print 

#Creating RuleMap
rmap = RuleMap([ru1, ru2, ru3])

#Checking Rules
print 'Checking Rules ======================='

feas = [60, None, None, None]
print 'Input feas with the values: '
rmap.print_rhs_orders()
print feas, "\n"

meet_rules = rmap.check_all(feas)
if meet_rules == []:
    # Recommending rules to be considered.
    print "The following rules should be considered for next steps: "
    res, sorted_metric = rmap.recommend(feas, key='self_proba')
    print res, '\n'
else:
    print "The following rules are decision rules with their labels: "
    print meet_rules, '\n'

#Checking Rules
print 'Checking Rules ======================='

feas = [40, None, None, None]
print 'Input feas with the values: '
rmap.print_rhs_orders()
print feas, "\n"

meet_rules = rmap.check_all(feas)
if meet_rules == []:
    # Recommending rules to be considered.
    print "The following rules should be considered for next steps: "
    res, sorted_metric = rmap.recommend(feas, key='self_proba')
    print res, '\n'
else:
    print "The following rules are decision rules with their labels: "
    print meet_rules, '\n'
