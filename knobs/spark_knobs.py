'''
    continuous_knobs : dictionary
                        key = knob name
                        data = [min, max, default]
    categorical_knobs : dictionary
                        key = knob name
                        data = [[category data], default]
    boolean_knobs : list, value is true or false and all default is true
'''

continuous_knobs = {'spark.kryoserializer.buffer':[32, 128, 64],
                    'spark.kryoserializer.buffer.max':[32, 128, 64],
                    'spark.locality.wait':[1, 6, 3],
                    'spark.memory.offHeap.size':[0, 4096, 0],
                    'spark.reducer.maxSizeInFlight':[24, 38, 48],
                    'spark.scheduler.revive.interval':[1, 5, 1],
                    'spark.shuffle.file.buffer':[16, 64, 32],
                    'spark.shuffle.io.numConnectionsPerPeer':[1, 5, 1],
                    'spark.shuffle.sort.bypassMergeThreshold':[100, 400, 200],
                    'spark.storage.memoryMapThreshold':[1, 10, 2]
                    }

numeric_categorical_knobs = {'spark.memory.fraction':[[s/10 for s in range(5, 10)], 0.6], # 0.5, 0.6, 0.7, 0.8, 0.9
                     'spark.memory.storageFraction':[[s/10 for s in range(5, 10)], 0.5],
                    }

string_categorical_knobs = {'spark.broadcast.compress':[['true', 'false'], 'true'],
                            'spark.memory.offHeap.enabled':[['true', 'false'], 'true'],
                            'spark.rdd.compress':[['true', 'false'], 'true'],
                            'spark.shuffle.compress':[['true', 'false'], 'true'],
                            'spark.shuffle.spill.compress':[['true', 'false'], 'true'],
                            'spark.sql.codegen.aggregate.map.twolevel.enable':[['true', 'false'], 'true'],
                            'spark.sql.inMemoryColumnarStorage.compressed':[['true', 'false'], 'true'],
                            'spark.sql.inMemoryColumnarStorage.partitionPruning':[['true', 'false'], 'true'],
                            'spark.sql.join.preferSortMergeJoin':[['true', 'false'], 'true'],
                            'spark.sql.retainGroupColumns':[['true', 'false'], 'true'],
                            'spark.sql.sort.enableRadixSort':[['true', 'false'], 'true'],
                            }
# # true, false
# boolean_knobs = ['spark.broadcast.compress', 'spark.memory.offHeap.enabled', 'spark.rdd.compress', 'spark.shuffle.compress', 'spark.shuffle.spill.compress',
#                  'spark.sql.codegen.aggregate.map.twolevel.enable', 'spark.sql.inMemoryColumnarStorage.compressed', 'spark.sql.inMemoryColumnarStorage.partitionPruning',
#                  'spark.sql.join.preferSortMergeJoin', 'spark.sql.retainGroupColumns', 'spark.sql.sort.enableRadixSort'
#                 ]