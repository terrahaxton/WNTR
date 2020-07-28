from __future__ import print_function
from nose.tools import *
from os.path import abspath, dirname, join
import wntr

testdir = dirname(abspath(str(__file__)))
datadir = join(testdir,'..','..','examples','networks')

"""
Compare results to EPANET GUI using Net3 and Source Quality at
121          SETPOINT      100000  mg/L
121          FLOWPACED     100000  mg/L
121          MASS          6000000000  mg/min
River        CONCEN        100000   mg/L
"""

def test_setpoint_waterquality_simulation():
    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.quality.mode = 'CHEMICAL'
    wn.add_pattern('NewPattern', [1]) #start_time=0, end_time=wn.options.time.duration)
    wn.add_source('Source1', '121', 'SETPOINT', 100, 'NewPattern')
    #WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'SETPOINT', 100, 0, -1)

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    expected = 91661.72*(1e-6/0.001) # Node '159' at hour 6
    #print(results.node)
    error = abs((results.node['quality'].loc[6*3600, '159'] - expected)/expected)
    assert_less(error, 0.0001) # 0.01% error

def test_flowpaced_waterquality_simulation():
    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.quality.mode = 'CHEMICAL'
    wn.add_pattern('NewPattern', [1]) #start_time=0, end_time=wn.options.time.duration)
    wn.add_source('Source1', '121', 'FLOWPACED', 100, 'NewPattern')
    #WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'FLOWPACED', 100, 0, -1)

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    expected = 92246.55*(1e-6/0.001) # Node '159' at hour 6
    error = abs((results.node['quality'].loc[6*3600, '159'] - expected)/expected)
    assert_less(error, 0.0001) # 0.01% error

def test_mass_waterquality_simulation():
    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.quality.mode = 'CHEMICAL'
    wn.add_pattern('NewPattern', [1.0] )# start_time=0, end_time=wn.options.time.duration)
    wn.add_source('Source1', '121', 'MASS', 100, 'NewPattern')
    #WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'MASS', 100, 0, -1)

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    expected = 217903.60*(1e-6/0.001) # Node '159' at hour 6
    error = abs((results.node['quality'].loc[6*3600, '159'] - expected)/expected)
    assert_less(error, 0.0001) # 0.01% error

def test_conc_waterquality_simulation():
    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.quality.mode = 'CHEMICAL'
    wn.add_pattern('NewPattern', [1.0])# start_time=0, end_time=wn.options.time.duration)
    wn.add_source('Source1', 'River', 'CONCEN', 100, 'NewPattern')
    #WQ = wntr.scenario.Waterquality('CHEM', ['River'], 'CONCEN', 100, 0, -1)

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    expected = 91661.72*(1e-6/0.001) # Node '159' at hour 6
    error = abs((results.node['quality'].loc[6*3600, '159'] - expected)/expected)
    assert_less(error, 0.0001) # 0.01% error

def test_age_waterquality_simulation():

    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)

    wn.options.quality.mode = 'AGE'
    #WQ = wntr.scenario.Waterquality('AGE')

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    # WARNING: This does NOT match the EPANET Windows results - it does match
    # the epanet linux binary
    expected = 3.652*3600 # Node '159' at hour 6
    error = abs((results.node['quality'].loc[6*3600, '159'] - expected)/expected)
    #print([expected, results.node['quality'].loc[6*3600, '159']])
    assert_less(error, 0.001) # 0.01% error

def test_trace_waterquality_simulation():
    inp_file = join(datadir,'Net3.inp')

    wn = wntr.network.WaterNetworkModel(inp_file)
    wn.options.quality.mode = 'TRACE'
    wn.options.quality.trace_node = '121'
    #WQ = wntr.scenario.Waterquality('TRACE', ['121'])

    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    #print(results.node.keys())
    expected = 91.66 # Node '159' at hour 6
    error = abs(float(results.node['quality'].loc[6*3600, '159'] - expected)/float(expected))
    assert_less(error, 0.0001) # 0.01% error

if __name__ == '__main__':
    test_setpoint_waterquality_simulation()
    #test_flowpaced_waterquality_simulation()
    #test_mass_waterquality_simulation()
    #test_conc_waterquality_simulation()
    #test_age_waterquality_simulation()
    #test_trace_waterquality_simulation()
