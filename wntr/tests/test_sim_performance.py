from __future__ import print_function
import unittest
import sys
import os
import time
import numpy as np
from os.path import abspath, dirname, join
import pandas

pandas.set_option('display.max_rows', 10000)

testdir = dirname(abspath(str(__file__)))
test_datadir = join(testdir,'networks_for_testing')
ex_datadir = join(testdir,'..','..','examples','networks')
results_dir = join(testdir,'performance_results')


def compare_results(wntr_res, epa_res, abs_threshold, rel_threshold):
    abs_diff = abs(wntr_res - epa_res)
    rel_diff = abs_diff / abs(epa_res)
    abs_diffa = abs_diff.mean()
    rel_diffa = rel_diff.mean()
    abs_diffb = abs_diff.mean(axis=1)
    rel_diffb = rel_diff.mean(axis=1)
    diffa = (abs_diffa < abs_threshold) | (rel_diffa < rel_threshold)
    diffb = (abs_diffb < abs_threshold) | (rel_diffb < rel_threshold)
    return diffa.all() and diffb.all()


class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        sys.path.append(results_dir)
        import wntr
        self.wntr = wntr

    @classmethod
    def tearDownClass(self):
        pass

    def test_Net1_performance(self):
        head_diff_abs_threshold = 1e-3
        demand_diff_abs_threshold = 1e-5
        flow_diff_abs_threshold = 1e-5
        rel_threshold = 1e-3

        inp_file = join(ex_datadir, 'Net1.inp')
        wn = self.wntr.network.WaterNetworkModel(inp_file)

        epa_sim = self.wntr.sim.EpanetSimulator(wn)
        epa_res = epa_sim.run_sim()

        sim = self.wntr.sim.WNTRSimulator(wn)
        results = sim.run_sim()

        self.assertTrue(compare_results(results.node['head'], epa_res.node['head'], head_diff_abs_threshold, rel_threshold))
        self.assertTrue(compare_results(results.node['demand'].loc[:, wn.tank_name_list], epa_res.node['demand'].loc[:, wn.tank_name_list], demand_diff_abs_threshold, rel_threshold))
        self.assertTrue(compare_results(results.link['flowrate'], epa_res.link['flowrate'], flow_diff_abs_threshold, rel_threshold))

    def test_Net3_performance(self):
        head_diff_abs_threshold = 1e-3
        demand_diff_abs_threshold = 1e-5
        flow_diff_abs_threshold = 1e-5
        rel_threshold = 1e-3

        inp_file = join(ex_datadir, 'Net3.inp')
        wn = self.wntr.network.WaterNetworkModel(inp_file)

        epa_sim = self.wntr.sim.EpanetSimulator(wn)
        epa_res = epa_sim.run_sim()

        sim = self.wntr.sim.WNTRSimulator(wn)
        results = sim.run_sim()

        self.assertTrue(compare_results(results.node['head'], epa_res.node['head'], head_diff_abs_threshold, rel_threshold))
        self.assertTrue(compare_results(results.node['demand'].loc[:, wn.tank_name_list], epa_res.node['demand'].loc[:, wn.tank_name_list], demand_diff_abs_threshold, rel_threshold))
        self.assertTrue(compare_results(results.link['flowrate'], epa_res.link['flowrate'], flow_diff_abs_threshold, rel_threshold))

    def test_Net6_mod_performance(self):
        head_diff_abs_threshold = 1e-3
        demand_diff_abs_threshold = 1e-5
        flow_diff_abs_threshold = 1e-5
        rel_threshold = 1e-3

        inp_file = join(ex_datadir,'Net6.inp')
        wn = self.wntr.network.WaterNetworkModel(inp_file)
        wn.options.time.duration = 24*3600
        wn.options.time.hydraulic_timestep = 3600
        wn.options.time.report_timestep = 3600
        wn.remove_control('control 72')  # this control never gets activated in epanet because it uses a threshold equal to the tank max level

        epa_sim = self.wntr.sim.EpanetSimulator(wn)
        epa_res = epa_sim.run_sim()

        sim = self.wntr.sim.WNTRSimulator(wn)
        results = sim.run_sim()

        self.assertTrue(compare_results(results.node['head'], epa_res.node['head'], head_diff_abs_threshold, rel_threshold))
        # self.assertTrue(compare_results(results.node['demand'].loc[:, wn.tank_name_list], epa_res.node['demand'].loc[:, wn.tank_name_list], demand_diff_abs_threshold, rel_threshold))
        # self.assertTrue(compare_results(results.link['flowrate'], epa_res.link['flowrate'], flow_diff_abs_threshold, rel_threshold))


if __name__ == '__main__':
    unittest.main()
