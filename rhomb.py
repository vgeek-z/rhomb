# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2020 Nengjun Zhu. All Rights Reserved
# Licensed under the MIT (the "LICENSE")
# 
########################################################################
 
"""
File: rhomb.py
Author: Nengjun Zhu(zhu_nj@sjtu.edu.cn)
Alliation: Shanghai Jiao Tong University
Date: 2020/01/02 12:21:47
"""

from operator import itemgetter
import numpy as np

class Voc:
    def __init__(self, sentence=False):
        self.trimmed = False
        self.word2index = {}
        self.word2count = {}
        self.index2word = {} #{PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 0
        if type(sentence) != type(False):
            self.addSentence(sentence)

    def addSentence(self, sentence):
        for word in sentence:
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    # Remove words below a certain count threshold
    def trim(self, min_count):
        if self.trimmed:
            return
        self.trimmed = True
        keep_words = []

        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        # Reinitialize dictionaries
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3 # Count default tokens

        for word in keep_words:
            self.addWord(word)

class Rhombus:
    def __init__(self, name='', cost=1.):
        '''
        Input:
            name: str
            cost: float
        '''
        self.name = name
        self.cost = cost
        self.conditions = []
    def add_condition(self, str_condtion):
        '''
        Input:
            str_condition: "x >= 2"
        '''
        self.conditions.append(str_condtion)
    def del_condition(self, idx):
        del self.conditions[idx]
    def judge(self, x):
        for i, c in enumerate(self.conditions):
            if eval(c):
                return i
        return None
    def print_conditions(self):
        print 'name: ', self.name
        print 'condition, branch_id'
        for i, c in enumerate(self.conditions):
            print "{}, {}".format(c, i)
    def __call__(self, x):
        return self.judge(x)

class Rule:
    def __init__(self, rhombusList, label, ID, prob=1.):
        '''
        Input:
            rhombusList: [(r1, 1), (r2, 0)]
        '''
        self.rhombusList = rhombusList
        self.prob = prob
        self.label = label
        self.id = ID
        self.rhs, self.bids = self.__extract_rhs_bids__()
    def __extract_rhs_bids__(self):
        rhs, bids = [], []
        for rh, bid in self.rhombusList:
            rhs.append(rh)
            bids.append(bid)
        return rhs, bids
    def check(self, values):
        '''
        Input:
            values: [x1, x2, x3], the length of values must be equal to that of self.rhombusList, not all rhombus
        '''
        if isinstance(values, int):
            values = [values]
        return all([rh(values[i]) == bid for i, (rh, bid) in enumerate(self.rhombusList)])
    def print_rule(self):
        print '{}: '.format(self.id) + ' | '.join(['(' + rh.name + ',' + str(bid)  + ')' + ': ' + rh.conditions[bid] \
                           for (rh, bid) in self.rhombusList])

class RuleMap:
    def __init__(self, rules=[]):
        self.mask = np.zeros(0)
        self.ruleVoc = Voc(rules)
        self.rhVoc = Voc()
        self.num_cond = 0
        self.rh2cond = {}
        self.cond2rh = {}
        self.candidates = {}
        self.__add_rhs__()

    def __add_rhs__(self):
        for ru in self.ruleVoc.index2word.values():
            self.rhVoc.addSentence(ru.rhs)
        self.__gen_rh_cond_map__()
    def __gen_rh_cond_map__(self):
        for rh in self.rhVoc.index2word.values():
            self.rh2cond[self.rhVoc.word2index[rh]] = []
            for _ in xrange(len(rh.conditions)):
                self.cond2rh[self.num_cond] = self.rhVoc.word2index[rh]
                self.rh2cond[self.rhVoc.word2index[rh]].append(self.num_cond)
                self.num_cond += 1

    def add_rules(self, rules):
        self.ruleVoc.addSentence(rules)
        self.__add_rhs__()

    def __gen_map__(self):
        self.mask = np.zeros((self.num_cond, self.ruleVoc.num_words))
        for j, ru in self.ruleVoc.index2word.items():
            rhs, bids = ru.rhs, ru.bids
            for idx, rh in enumerate(rhs):
                i = self.rh2cond[self.rhVoc.word2index[rh]][bids[idx]]
                self.mask[i][j] = 1
        return self.mask

    def check_all(self, values):
        '''
        Input:
            values: [x1, x2, ..., None]
            None represents missing value
            len(values) == the number of all thombus
        '''
        meet_rules = []
        for ru in self.ruleVoc.index2word.values():
            rh_ids = [self.rhVoc.word2index[rh] for rh in ru.rhs]
            if ru.check(itemgetter(*rh_ids)(values)):
                meet_rules.append("{}-{}".format(ru.id, ru.label))
        return meet_rules
    def print_rhs_orders(self):
        print [rh.name for rh in self.rhVoc.index2word.values()]
    def gen_candidate(self, values=[]):
        '''
        Input:
            values: [x1, x2, ..., None]
            None represents missing value
            len(values) == the number of all thombus
        '''
        self.__gen_map__()
        comparison = np.zeros((self.num_cond, self.ruleVoc.num_words))
        del_rhs_ids = [i for i, v in enumerate(values) if v is not None]
        del_row_ids = []
        for rh_id in del_rhs_ids:
            del_row_ids += self.rh2cond[rh_id]
        for ru in self.ruleVoc.index2word.values():
            j = self.ruleVoc.word2index[ru]
            for rh in ru.rhs:
                rh_id = self.rhVoc.word2index[rh]
                if rh.judge(values[rh_id]) is None:
                    continue
                i = self.rh2cond[rh_id][rh.judge(values[rh_id])]
                comparison[i][j] = 1
        #print comparison
        res = self.mask - self.mask * comparison
        for r in del_row_ids:
            indice = np.where(res[r] == 1)
            res[:,indice[0]] = 0
        candidates = {}
        ones = np.where(res == 1)
        for col in set(ones[1]):
            key = (col, self.ruleVoc.index2word[col].id)
            candidates.setdefault(key, {'target_rhs': [], \
                                        'total_cost': 0.0, \
                                        'proba': self.ruleVoc.index2word[col].prob, \
                                        'share_rule_proba': 0.0, 'share_rule_cnt': 0})
            share_rule = set()
            for i, vi in enumerate(res[:, col]):
                if vi == 1:
                    rh_id = self.cond2rh[i]
                    candidates[key]['target_rhs'].append((rh_id, self.rhVoc.index2word[rh_id].name))
                    candidates[key]['total_cost'] += self.rhVoc.index2word[rh_id].cost

                    for j, vj in enumerate(res[i, :]):
                        if vj == 1 and j != col:
                            if j not in share_rule:
                                share_rule.add(j)
                                candidates[key]['share_rule_proba'] += self.ruleVoc.index2word[j].prob
                                candidates[key]['share_rule_cnt'] += 1
        self.candidates = candidates
        return candidates
    def recommend(self, values=[], topK=3, key='num_target_rhs'):
        '''
        Input:
            values: [x1, x2, ..., None]
                None represents missing value
                len(values) == the number of all thombus
            key: num_target_rhs, self_proba, total_cost, share_rule_proba, share_rule_cnt
        '''
        key_map = {'num_target_rhs': [0, False],\
                   'self_proba': [1, True], \
                   'total_cost': [2, False], \
                   'share_rule_proba': [3, True],\
                   'share_rule_cnt': [4, True]}
        if self.candidates == {}:
            self.gen_candidate(values)

        metric_values = {}
        for ru, ms in self.candidates.items():
            metric_values[ru] = [len(ms['target_rhs']), ms['proba'], \
                                     ms['total_cost'], ms['share_rule_proba'], ms['share_rule_cnt']]

        sorted_metric = sorted(metric_values.items(), key=lambda x: x[1][key_map[key][0]], \
                      reverse=key_map[key][1])[:topK]
        return [(ru, self.candidates[ru]['target_rhs']) for ru, _ in sorted_metric], sorted_metric

