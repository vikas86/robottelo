"""Test class for Compute Profile UI

:Requirement: Computeprofile

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: ComputeResources

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
from fauxfactory import gen_string
from nailgun import entities

from robottelo.decorators import tier2
from robottelo.decorators import upgrade


@tier2
@upgrade
def test_positive_end_to_end(session, module_loc, module_org):
    """Perform end to end testing for compute profile component

    :id: 5445fc7e-7b3f-472f-8a94-93f89aca6c22

    :expectedresults: All expected CRUD actions finished successfully

    :CaseLevel: Integration

    :CaseImportance: High
    """
    name = gen_string('alpha')
    new_name = gen_string('alpha')
    compute_resource = entities.LibvirtComputeResource(
        location=[module_loc], organization=[module_org], url='qemu+ssh://root@test/system'
    ).create()
    with session:
        session.computeprofile.create({'name': name})

        assert entities.ComputeProfile().search(query={'search': 'name={0}'.format(name)}), (
            'Compute profile {0} expected to exist, but is not included in the search '
            'results'.format(name)
        )
        compute_resource_list = session.computeprofile.list_resources(name)
        assert '{} (Libvirt)'.format(compute_resource.name) in [
            resource['Compute Resource'] for resource in compute_resource_list
        ]
        session.computeprofile.rename(name, {'name': new_name})
        assert entities.ComputeProfile().search(query={'search': 'name={0}'.format(new_name)}), (
            'Compute profile {0} expected to exist, but is not included in the search '
            'results'.format(new_name)
        )
        session.computeprofile.delete(new_name)
        assert not entities.ComputeProfile().search(
            query={'search': 'name={0}'.format(new_name)}
        ), (
            'Compute profile {0} expected to be deleted, but is included in the search '
            'results'.format(new_name)
        )
