'''
    continuous_knobs : dictionary
                        key = knob name
                        data = [min, max, default]
    boolean_knobs : list, value is true or false and all default is true
'''

continuous_knobs = {'hash-max-ziplist-value':[16, 256, 64],
                    'hz':[1, 40, 10],
                    }
string_categorical_knobs = {'lazyfree-lazy-expire':[['yes', 'no'], 'no'], 
                            'lazyfree-lazy-server-del':[['yes', 'no'], 'no'],
                            'lazyfree-lazy-eviction':[['yes', 'no'], 'no'],
                            'activerehashing':[['yes', 'no'], 'yes']
                            }
# # yes or no
# boolean_knobs = ['lazyfree-lazy-expire', 'lazyfree-lazy-server-del', 'lazyfree-lazy-eviction', 'activerehashing']