# -*- coding: utf-8 -*-

# Add src folder to Python search paths
import sys

sys.path.insert(1, "src")

# Normal imports
import core.controller
import core.model
import core.view
import patterns.command
import patterns.facade
import patterns.mediator
import patterns.observer
import patterns.proxy
import unittest


if __name__ == '__main__':
    # List of test cases classes
    testCases = (core.controller.ControllerTest,
                 core.model.ModelTest,
                 core.view.ViewTest,

                 patterns.command.CommandTest,
                 patterns.facade.FacadeTest,
                 patterns.mediator.MediatorTest,
                 patterns.observer.ObserverTest,
                 patterns.observer.NotifierTest,
                 patterns.proxy.ProxyTest)

    # Discover all the test cases
    loader = unittest.TestLoader()
    suites = []

    for testCase in testCases:
        suites.append(loader.loadTestsFromTestCase(testCase))

    # Run test suite
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))
