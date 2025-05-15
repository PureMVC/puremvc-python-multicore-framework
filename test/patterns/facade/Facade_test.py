# Facade_test.py
# PureMVC Python Multicore

# Copyright(c) 2025 Saad Shams <saad.shams@puremvc.org>
# Your reuse is governed by the BSD 3-Clause License

import unittest
from typing import List

from puremvc.interfaces import IFacade, INotification, IProxy
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Facade
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.proxy import Proxy


class FacadeTest(unittest.TestCase):
    """Test the PureMVC Facade class."""

    def test_get_instance(self):
        """Tests the Facade Multiton Factory Method """
        # Test Factory Method
        facade: IFacade = Facade.get_instance("FacadeTestKey1", lambda k: Facade(k))

        # test assertions
        self.assertIsNotNone(facade, "Expecting instance not None")
        self.assertIsInstance(facade, IFacade, "Expecting instance implements IFacade")

    def test_register_command_and_send_notification(self):
        """
        Tests Command registration and execution via the Facade.

        This test gets a Multiton Facade instance
        and registers the FacadeTestCommand class
        to handle 'FacadeTest' Notifications.

        It then sends a notification using the Facade.
        Success is determined by evaluating
        a property on an object placed in the body of
        the Notification, which will be modified by the Command.
        """
        # Create the Facade, register the FacadeTestCommand to
        # handle 'FacadeTest' notifications
        facade: IFacade = Facade.get_instance("FacadeTestKey2", lambda k: Facade(k))
        facade.register_command("FacadeTestNote", lambda: FacadeTestCommand())

        # Send notification. The Command associated with the event
        # (FacadeTestCommand) will be invoked, and will multiply 
        # the vo.input value by 2 and set the result on vo.result
        vo = FacadeTestVO(32)
        facade.send_notification("FacadeTestNote", vo)

        # test assertions
        self.assertTrue(vo.result == 64, "Expecting vo.result == 64")

    def test_register_and_remove_command_and_send_notification(self):
        """
        Tests Command removal via the Facade.

        This test gets a Multiton Facade instance
        and registers the FacadeTestCommand class
        to handle 'FacadeTest' Notifications. Then it removes the command.

        It then sends a Notification using the Facade.
        Success is determined by evaluating
        a property on an object placed in the body of
        the Notification, which will NOT be modified by the Command.
        """
        # Create the Facade, register the FacadeTestCommand to
        # handle 'FacadeTest' events
        facade: IFacade = Facade.get_instance("FacadeTestKey3", lambda k: Facade(k))
        facade.register_command("FacadeTestNote", lambda: FacadeTestCommand())
        facade.remove_command("FacadeTestNote")

        # Send notification. The Command associated with the event
        # (FacadeTestCommand) will NOT be invoked, and will NOT multiply 
        # the vo.input value by 2
        vo = FacadeTestVO(32)
        facade.send_notification("FacadeTestNote", vo)

        # test assertions
        self.assertTrue(vo.result != 64, "Expecting vo.result != 64")

    def test_register_and_retrieve_proxy(self):
        """
        Tests the registering and retrieving Model proxies via the Facade.

        Tests `register_proxy` and `retrieve_proxy` in the same test.
        These methods cannot currently be tested separately
        in any meaningful way other than to show that the
        methods do not throw exception when called.
        """
        # register a proxy and retrieve it.
        facade: IFacade = Facade.get_instance("FacadeTestKey4", lambda k: Facade(k))
        facade.register_proxy(Proxy("colors", ["red", "green", "blue"]))
        proxy = facade.retrieve_proxy("colors")

        # test assertions
        self.assertIsInstance(proxy, IProxy, "Expecting proxy is IProxy")

        # retrieve data from proxy
        data: [str] = proxy.data

        # test assertions
        self.assertIsNotNone(data, "Expecting data not None")
        self.assertIsInstance(data, List, "Expecting data is List")
        self.assertTrue(len(data) == 3, "Expecting len(data) == 3")
        self.assertTrue(data[0] == "red", "Expecting data[0] == 'red'")
        self.assertTrue(data[1] == "green", "Expecting data[1] == 'green'")
        self.assertTrue(data[2] == "blue", "Expecting data[2] == 'blue'")

    def test_register_and_remove_proxy(self):
        """Tests the removing Proxies via the Facade."""
        # register a proxy, remove it, then try to retrieve it
        facade: IFacade = Facade.get_instance("FacadeTestKey5", lambda k: Facade(k))
        proxy = Proxy("sizes", ["7", "13", "21"])
        facade.register_proxy(proxy)

        # remove the proxy
        removed_proxy = facade.remove_proxy("sizes")

        # assert that we removed the appropriate proxy
        self.assertTrue(removed_proxy.proxy_name == "sizes",
                        "Expecting removed_proxy.proxy_name() == 'sizes'")

        # make sure we can no longer retrieve the proxy from the model
        proxy = facade.retrieve_proxy("sizes")

        # test assertions
        self.assertIsNone(proxy, "Expecting proxy is None")

    def test_register_retrieve_and_remove_mediator(self):
        """Tests registering, retrieving and removing Mediators via the Facade."""
        # register a mediator, remove it, then try to retrieve it
        facade: IFacade = Facade.get_instance("FacadeTestKey6", lambda k: Facade(k))
        facade.register_mediator(Mediator(Mediator.NAME, object()))

        # retrieve the mediator
        self.assertIsNotNone(facade.retrieve_mediator(Mediator.NAME), "Expecting mediator is not None")

        # remove the mediator
        removed_mediator = facade.remove_mediator(Mediator.NAME)

        # assert that we have removed the appropriate mediator
        self.assertTrue(removed_mediator.mediator_name == Mediator.NAME,
                        "Expecting removed_mediator.mediator_name == Mediator.NAME")

        # assert that the mediator is no longer retrievable
        self.assertIsNone(facade.retrieve_mediator(Mediator.NAME),
                          "Expecting facade.retrieve_mediator(Mediator.NAME) == None")

    def test_has_proxy(self):
        """Tests the has_proxy Method"""
        # register a Proxy
        facade: IFacade = Facade.get_instance("FacadeTestKey7", lambda k: Facade(k))
        facade.register_proxy(Proxy("hasProxyTest", [1, 2, 3]))

        # assert that the model.has_proxy method returns true
        # for that proxy name
        self.assertTrue(facade.has_proxy("hasProxyTest"), "Expecting facade.has_proxy('hasProxyTest') == true")

    def test_has_mediator(self):
        """Tests the hasMediator Method"""
        # register a Mediator
        facade: IFacade = Facade.get_instance("FacadeTestKey8", lambda k: Facade(k))
        facade.register_mediator(Mediator("facadeHasMediatorTest", object()))

        # assert that the facade.hasMediator method returns true
        # for that mediator name
        self.assertTrue(facade.has_mediator("facadeHasMediatorTest"),
                        "Expecting facade.has_mediator('facadeHasMediatorTest') == true")

        facade.remove_mediator("facadeHasMediatorTest")

        # assert that the facade.hasMediator method returns false
        # for that mediator name
        self.assertFalse(facade.has_mediator("facadeHasMediatorTest"),
                         "Expecting facade.has_mediator('facadeHasMediatorTest') == false")

    def test_has_command(self):
        """Test hasCommand method."""
        # register the ControllerTestCommand to handle 'hasCommandTest' notes
        facade: IFacade = Facade.get_instance("FacadeTestKey10", lambda k: Facade(k))
        facade.register_command("facadeHasCommandTest", lambda: FacadeTestCommand())

        # test that hasCommand returns true for hasCommandTest notifications
        self.assertTrue(facade.has_command("facadeHasCommandTest"),
                        "Expecting facade.has_command('facadeHasCommandTest') == true")

        # Remove the Command from the Controller
        facade.remove_command("facadeHasCommandTest")

        # test that hasCommand returns false for hasCommandTest notifications
        self.assertFalse(facade.has_command("facadeHasCommandTest"),
                         "Expecting facade.has_command('facadeHasCommandTest') == false")

    def test_has_core_and_remove_core(self):
        """Tests the hasCore and removeCore methods"""
        # assert that the Facade.hasCore method returns false first
        self.assertFalse(Facade.has_core("FacadeTestKey11"),
                         "Expecting facade.has_core('FacadeTestKey11') == false")

        # register a Core
        Facade.get_instance("FacadeTestKey11", lambda k: Facade(k))

        # assert that the Facade.hasCore method returns true now that a Core is registered
        self.assertTrue(Facade.has_core("FacadeTestKey11"),
                        "Expecting facade.hasCore('FacadeTestKey11') == true")

        # remove the Core
        Facade.remove_core("FacadeTestKey11")

        # assert that the Facade.hasCore method returns false now that the core has been removed.
        self.assertFalse(Facade.has_core("FacadeTestKey11"),
                         "Expecting facade.has_core('FacadeTestKey11') == false")


class FacadeTestCommand(SimpleCommand):
    def execute(self, notification: INotification):
        """
        Fabricate a result by multiplying the input by 2
        :param notification: the Notification carrying the FacadeTestVO
        :type notification: INotification
        """
        vo: FacadeTestVO = notification.body

        # Fabricate a result
        vo.result = 2 * vo.input


class FacadeTestVO:
    def __init__(self, data: int):
        """
        Constructor.
        :param data: input the number to be fed to the FacadeTestCommand
        :type data: int
        """
        self.input = data
        self.result = 0


if __name__ == '__main__':
    unittest.main()
