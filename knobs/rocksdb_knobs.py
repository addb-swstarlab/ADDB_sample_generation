'''
    continuous_knobs : dictionary
                        key = knob name
                        data = [min, max, default]
    categorical_knobs : dictionary
                         key = knob name
                         data = [[category data], default]   
    boolean_knobs : list, value is true or false and all default is true
'''
KB = 1024
MB = 1024 * 1024

continuous_knobs = {'max_background_compactions':[1, 16, 1],
                    'max_background_flushes':[1, 16, 1],
                    'max_write_buffer_number':[2, 8, 2],
                    'min_write_buffer_number_to_merge':[1, 3, 1],
                    'compaction_pri':[0, 3, 0], # 0:kByCompensatedSize 1:kOldestLargestSeqFirst, 2:kOldestSmallestSeqFirst, 3:kMinOverlappingRatio
                    'compaction_style':[0, 3, 0], # 0:kCompactionStyleLevel 1:kCompactionStyleUniversal, 2:kCompactionStyleFIFO, 3:kCompactionStyleNone
                    'level0_file_num_compaction_trigger':[2, 8, 4],
                    'level0_slowdown_writes_trigger':[16, 32, 20],
                    'level0_stop_writes_trigger':[32, 64, 36],
                    'bloom_locality':[0, 1, 0],
                    'block_size':[2, 16, 4096],
                    'max_bytes_for_level_multiplier':[8, 12, 10],
                    'target_file_size_multiplier':[1, 2, 1],
                    'num_levels':[5, 8, 7],
                    }

numeric_categorical_knobs = {'write_buffer_size':[[s*KB for s in range(512, 2049)], 1024*KB],
                             'max_bytes_for_level_base':[[s*MB for s in range(2, 9)], 4*MB],
                             'target_file_size_base':[[s*KB for s in range(512, 2049)], 1024*KB],
                             'memtable_bloom_size_ratio':[[0, 0.05, 0.1, 0.15, 0.2], 0], # 0, 0.05, 0.1, 0.15, 0.2
                             'compression_ratio':[[s/100 for s in range(100)], 0.5], # 0.10 ~ 0.99, ex. 0.12,
                             'cache_index_and_filter_blocks':[[0, 1], 0]
                            }

string_categorical_knobs = {'compression_type':[['snappy', 'zlib', 'lz4', 'none'], 'snappy'],
                            }

# boolean_knobs = ['cache_index_and_filter_blocks'] # 0 or 1