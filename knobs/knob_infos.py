import knobs.spark_knobs as spark_knobs
import knobs.redis_knobs as redis_knobs
import knobs.rocksdb_knobs as rocksdb_knobs
import numpy as np

class Knobs():
    def __init__(self, continuous, numeric_cat, string_cat):
        self.continuous = continuous
        self.numeric_cat = numeric_cat
        self.string_cat = string_cat
        # self.boolean = boolean
        self.continuous_names = None
        self.numeric_cat_names = None
        self.string_cat_names = None
       
        self.get_name()
        self.get_statistics()
        
    def get_name(self):
        self.knob_names = list(self.continuous.keys())
        self.continuous_names = list(self.continuous.keys())
        if self.numeric_cat is not None:
            self.knob_names += list(self.numeric_cat.keys())
            self.numeric_cat_names = list(self.numeric_cat.keys())
        if self.string_cat is not None:
            self.knob_names += list(self.string_cat.keys())
            self.string_cat_names = list(self.string_cat.keys())
        # self.knob_names += list(self.boolean)
        # self.boolean_names = list(self.boolean)
        
    def get_statistics(self):
        self.mean = []
        self.std = []
        for k in self.continuous.keys():
            knob_range = range(self.continuous[k][0], self.continuous[k][1]+1)
            self.mean.append(np.mean(knob_range))
            self.std.append(np.std(knob_range))
        
        if self.numeric_cat is not None:
            for k in self.numeric_cat.keys():
                knob_range = range(len(self.numeric_cat[k][0]))
                self.mean.append(np.mean(knob_range))
                self.std.append(np.std(knob_range))
        
        if self.string_cat is not None:
            for k in self.string_cat.keys():
                knob_range = range(len(self.string_cat[k][0]))
                self.mean.append(np.mean(knob_range))
                self.std.append(np.std(knob_range))
                
        # for k in self.boolean:
        #     knob_range = [0, 1]
        #     self.mean.append(np.mean(knob_range))
        #     self.std.append(np.std(knob_range))
            
        
           
spark = Knobs(continuous=spark_knobs.continuous_knobs,
              numeric_cat=spark_knobs.numeric_categorical_knobs,
              string_cat=None,
              )

redis = Knobs(continuous=redis_knobs.continuous_knobs,
              numeric_cat=None,
              string_cat=redis_knobs.string_categorical_knobs,
              )

rocksdb = Knobs(continuous=rocksdb_knobs.continuous_knobs,
              numeric_cat=rocksdb_knobs.numeric_categorical_knobs,
              string_cat=rocksdb_knobs.string_categorical_knobs,
              )