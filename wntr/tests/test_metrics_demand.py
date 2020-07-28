from __future__ import division
from nose.tools import *
from os.path import abspath, dirname, join
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal
import wntr

testdir = dirname(abspath(str(__file__)))
datadir = join(testdir,'networks_for_testing')
net3dir = join(testdir,'..','..','examples','networks')


def test_expected_demand_net3_node101():
    inp_file = join(net3dir,'Net3.inp')
    wn = wntr.network.WaterNetworkModel(inp_file)
    
    expected_demand = wntr.metrics.hydraulic.expected_demand(wn)
    ave_expected_demand = wntr.metrics.hydraulic.average_expected_demand(wn)
    
    ex_demand_101 = expected_demand['101']
    ave_ex_demand_101 = ave_expected_demand['101']
    
    expected = 0.012813608
    error = abs((ex_demand_101.mean() - expected)/expected)
    assert_less(error, 0.01) # 1% error
    
    error = abs((ave_ex_demand_101 - expected)/expected)
    assert_less(error, 0.01) # 1% error

def test_wsa():
    
    expected_demand = pd.DataFrame(data=[[12,2],[3,4],[5,10]], columns=['A', 'B'], index=[0,1,2])
    demand = pd.DataFrame(data=[[5,2],[3,2],[3,4]], columns=['A', 'B'], index=[0,1,2])
    
    # WSA at each junction and time
    wsa = wntr.metrics.hydraulic.water_service_availability(expected_demand, demand)
    expected = pd.DataFrame(data=[[5/12,2/2],[3/3,2/4],[3/5,4/10]], columns=['A', 'B'], index=[0,1,2])
    assert_frame_equal(wsa, expected, check_dtype=False)

    # WSA at each junction
    wsa = wntr.metrics.hydraulic.water_service_availability(expected_demand.sum(axis=0), demand.sum(axis=0))
    expected = pd.Series(data=[(5+3+3)/(12+3+5), (2+2+4)/(2+4+10)], index=['A', 'B'])
    assert_series_equal(wsa, expected, check_dtype=False)

    # WSA at each time
    wsa = wntr.metrics.hydraulic.water_service_availability(expected_demand.sum(axis=1), demand.sum(axis=1))
    expected = pd.Series(data=[(5+2)/(12+2), (3+2)/(3+4),(3+4)/(5+10)], index=[0,1,2])
    assert_series_equal(wsa, expected, check_dtype=False)

if __name__ == '__main__':
    test_wsa()
