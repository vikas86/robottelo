# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
Test class for Subnet CLI
"""

from ddt import data
from ddt import ddt
from robottelo.cli.subnet import Subnet
from robottelo.common.helpers import generate_ipaddr
from robottelo.common.helpers import generate_name
from robottelo.common.helpers import sleep_for_seconds
from nose.plugins.attrib import attr
from tests.cli.basecli import BaseCLI


class SubnetData(dict):
    """
    Dumb class to hold a subnet dictionary object
    """
    pass


def fix_test_name(subnet_data):
    """Dynamically updates the test name for DDT tests"""

    annotated_data = SubnetData(subnet_data)

    # Updates the DDT name to a random value plus the ID of the data object
    setattr(
        annotated_data,
        "__name__", "%d" % int(id(annotated_data)))

    return annotated_data


@ddt
class TestSubnet(BaseCLI):
    """
    Subnet CLI tests.
    """

    subnet_192_168_100 = None

    def setUp(self):
        super(TestSubnet, self).setUp()

        if TestSubnet.subnet_192_168_100 is None:
            TestSubnet.subnet_192_168_100 = "subnet-192168100"
            Subnet.delete({'name': TestSubnet.subnet_192_168_100})
            Subnet.create_minimal(TestSubnet.subnet_192_168_100)

    @attr('cli', 'subnet')
    def test_create(self):
        """
        @Feature: Subnet - Create
        @Test: Check if Subnet can be created
        @Assert: Subnet is created
        """
        result = Subnet.create_minimal()
        self.assertTrue(result.return_code == 0,
                        "Subnet create - exit code %d" %
                        result.return_code)

    @attr('cli', 'subnet')
    def test_info(self):
        """
        @Feature: Subnet - Info
        @Test: Check if Subnet Info is displayed
        @Assert: Subnet Info is displayed
        """
        options = {}
        options['name'] = generate_name(8, 8)
        options['network'] = generate_ipaddr(ip3=True)
        options['mask'] = '255.255.255.0'

        Subnet.create(options)
        sleep_for_seconds(5)

        result = Subnet.info({'name': options['name']})

        self.assertTrue(len(result.stdout) > 1,
                        "Subnet info - returns 1 record")
        self.assertEquals(result.stdout['name'], options['name'],
                          "Subnet info - check name")

    @attr('cli', 'subnet')
    def test_list(self):
        """
        @Feature: Subnet - List
        @Test: Check if Subnet can be listed
        @Assert: Subnet is listed
        """
        result = Subnet.list({'per-page': '10'})
        self.assertGreater(len(result.stdout), 0,
                           "Subnet list - returns > 0 records")

    @attr('cli', 'subnet')
    @data(
        fix_test_name({'network': generate_ipaddr(ip3=True)}),
        fix_test_name({'mask': '255.255.0.0'}),
        fix_test_name({'gateway': '192.168.101.54'}),
        fix_test_name({'dns-primary': '192.168.100.0'}),
        fix_test_name({'dns-secondary': '10.17.100.0'}),
        fix_test_name({
            'network': '192.168.100.0',
            'from': '192.168.100.1',
            'to': '192.168.100.255',
        }),
        fix_test_name({'vlanid': '1'}),
    )
    def test_update_success_ddt(self, option_dict):
        """
        @Feature: Subnet - Update
        @Test: Check if Subnet can be udpated (with different options)
        @Assert: Subnet is updated
        """
        options = {}

        options['name'] = self.subnet_192_168_100
        for option in option_dict:
            options[option] = option_dict[option]
        result = Subnet.update(options)
        self.assertTrue(result.return_code == 0,
                        "Subnet update - exit code %d" %
                        result.return_code)

    @attr('cli', 'subnet')
    def test_delete(self):
        """
        @Feature: Subnet - Delete
        @Test: Check if Subnet can be deleted
        @Assert: Subnet is deleted
        """
        name = generate_name()
        options = {}
        options['name'] = name
        result = Subnet.create_minimal(name)
        self.assertTrue(result.return_code == 0,
                        "Subnet create - exit code %d" %
                        result.return_code)
        result = Subnet.delete(options)
        self.assertTrue(result.return_code == 0,
                        "Subnet delete - exit code %d" %
                        result.return_code)
