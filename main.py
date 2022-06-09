from knobs.knob_infos import spark, redis, rocksdb
from pyDOE import lhs
from scipy.stats.distributions import norm
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=int, default=10, help="Define sample size which is going to create")
opt = parser.parse_args()
MASTER_PATH = 'configs/master/'
SLAVE_PATH = 'configs/slave/'

def convert_outlier(x, dict_dbms, key):
    '''
        x : normed_data
        dict_dbms : dbms.continuous or dbms.numeric_cat or dbms.string_cat
        key : knob name
        
        convert the value above the maximum to the maximum, and do same on minimum
    '''
    len_ = len(dict_dbms[key])
        
    if len_ == 3: # continuous data
        x = np.where(x < dict_dbms[key][0], dict_dbms[key][0], x)
        x = np.where(x > dict_dbms[key][1], dict_dbms[key][1], x)
    elif len_ == 2:
        x = np.where(x <= 0, 0, x)
        x = np.where(x > len(dict_dbms[key][0])-1, len(dict_dbms[key][0])-1, x)
    return x

def write_knobs(selected_db, name, val):
    if name in selected_db.continuous_names:
        knob_line = f'{name} {val}\n'
    if selected_db.numeric_cat_names is not None and name in selected_db.numeric_cat_names:
        knob_line = f'{name} {val}\n'
    if selected_db.string_cat is not None and name in selected_db.string_cat_names:
        knob_line = f'{name} {selected_db.string_cat[name][0][val]}\n'
    return knob_line

def create_conf_file(CONF_FILE, addb_sample, addb, addb_name, addb_len):
    f = open(CONF_FILE, 'w')
    file_inputs = []
    cnt = 0
    for ld in range(len(addb)):
        selected_db = addb[ld]
        file_inputs.append(f'[{addb_name[ld]}]\n')
        for i, name in enumerate(selected_db.knob_names):
            i += sum(addb_len[:ld])
            selected_db = addb[ld]
            val = int(addb_sample[i])
            file_inputs.append(write_knobs(selected_db, name, val))
            if i == addb_len[ld]:
                cnt += 1
        file_inputs.append('\n')
    f.writelines(file_inputs[:-1])
    f.close()
    
def generate_addb_samples(sample_num, addb, addb_name, addb_len):
    addb_lhd = lhs(sum(addb_len), samples=sample_num)

    for a, dbms in enumerate(addb):
        for i, k in enumerate(dbms.knob_names):
            idx = sum(addb_len[:a]) + i
            normed_data = norm(loc=dbms.mean[i], scale=dbms.std[i]).ppf(addb_lhd[:, idx])
            normed_data = np.round(normed_data)

            # If the values are larger than maximum or less than minimum, set the values to be the maximum or minimum values.
            if k in dbms.continuous_names:
                normed_data = convert_outlier(normed_data, dbms.continuous, k)
            if dbms.numeric_cat_names is not None and k in dbms.numeric_cat_names:
                normed_data = convert_outlier(normed_data, dbms.numeric_cat, k)
            if dbms.string_cat_names is not None and k in dbms.string_cat_names:
                normed_data = convert_outlier(normed_data, dbms.string_cat, k)

            addb_lhd[:, idx] = normed_data
        addb_lhd = np.round(addb_lhd)

        for i, k in enumerate(dbms.knob_names):
            if dbms.numeric_cat_names is not None and k in dbms.numeric_cat_names:
                idx = sum(addb_len[:a]) + i
                normed_data = addb_lhd[:, idx]
                for n, data in enumerate(normed_data):
                    normed_data[n] = dbms.numeric_cat[k][0][int(data)]
                addb_lhd[:, idx] = normed_data.astype(float)
    
    addb_samples = addb_lhd
        
    for num, addb_sample in enumerate(addb_samples):
        CONF_NAME = f'addb_config{num}.conf'
        create_conf_file(os.path.join(MASTER_PATH, CONF_NAME), addb_sample[:addb_len[0]], addb[:1], addb_name[:1], addb_len[:1])
        create_conf_file(os.path.join(SLAVE_PATH, CONF_NAME), addb_sample[addb_len[0]:], addb[1:], addb_name[1:], addb_len[1:])
        
if __name__ == "__main__":
    if os.path.isdir(MASTER_PATH):
        os.system(f'rm -rf {MASTER_PATH}')
    os.mkdir(MASTER_PATH)
    
    if os.path.isdir(SLAVE_PATH):
        os.system(f'rm -rf {SLAVE_PATH}')
    os.mkdir(SLAVE_PATH)
            
    sample_num = opt.size
    addb = [spark, redis, rocksdb]
    addb_name = ['spark', 'redis', 'rocksdb']
    addb_len = [len(spark.knob_names), len(redis.knob_names), len(rocksdb.knob_names)]
    
    generate_addb_samples(sample_num=sample_num, addb=addb, addb_name=addb_name, addb_len=addb_len)