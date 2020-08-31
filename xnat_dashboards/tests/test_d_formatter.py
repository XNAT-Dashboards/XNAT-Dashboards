from xnat_dashboards.data_cleaning import data_formatter
from xnat_dashboards.bbrc import data_formatter as data_formatter_b

formatter_object_connected = data_formatter.Formatter()
formatter_object_connected_b = data_formatter_b.Formatter()


def test_get_projects_details():

    projects = 1
    project_details = formatter_object_connected.get_projects_details(projects)

    assert project_details == 1

    projects = None
    project_details_specific = formatter_object_connected.\
        get_projects_details_specific(projects, 'testUser')

    assert project_details_specific == 1

    projects = [
        {
            'project_access': 'private', 'id': 'id1',
            'project_owners': 'testUser',
            'project_collabs': 'tester 1', 'project_members': 'tester 2'},
        {'project_access': 'private', 'id': 'id2',
            'project_owners': 'testUser2',
            'project_collabs': 'tester 4', 'project_members': 'tester 5'}]

    project_details = formatter_object_connected.get_projects_details(projects)

    assert isinstance(project_details['Number of Projects'], int)
    assert isinstance(project_details['Projects Visibility'], dict)

    project_details_specific = formatter_object_connected.\
        get_projects_details_specific(projects, 'testUser')

    assert isinstance(project_details_specific, dict)


def test_get_subjects_details():

    subjects = 1
    subject_details = formatter_object_connected.get_subjects_details(subjects)

    assert subject_details == 1

    subjects = [
        {
            'project': 'p1', 'ID': 'sb1', 'age': 50,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb2', 'age': 10,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb3', 'age': 20,
            'handedness': 'right', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb4', 'age': 50,
            'handedness': 'left', 'gender': 'F'},
        {
            'project': 'p3', 'ID': 'sb5', 'age': 90,
            'handedness': 'left', 'gender': 'M'},
        {
            'project': 'p2', 'ID': 'sb6', 'age': 74,
            'handedness': 'left', 'gender': 'F'}]

    subject_details = formatter_object_connected.get_subjects_details(
        subjects)

    assert isinstance(subject_details['Number of Subjects'], int)
    assert isinstance(subject_details['Age Range'], dict)
    assert isinstance(subject_details['Gender'], dict)
    assert isinstance(subject_details['Handedness'], dict)
    assert isinstance(subject_details['Subjects/Project'], dict)


def test_get_experiments_details():

    experiments = 1
    experiments_details = formatter_object_connected.get_experiments_details(
        experiments)

    assert experiments_details == 1

    experiments = [
        {
            'project': 'p1', 'ID': 'exp1',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp2',
            'xsiType': 't1', 'subject_ID': 'sb1'},
        {
            'project': 'p1', 'ID': 'exp3',
            'xsiType': 't3', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp4',
            'xsiType': 't2', 'subject_ID': 'sb3'},
        {
            'project': 'p2', 'ID': 'exp5',
            'xsiType': 't1', 'subject_ID': 'sb3'},
        {
            'project': 'p3', 'ID': 'exp6',
            'xsiType': 't2', 'subject_ID': 'sb2'},
        {
            'project': 'p4', 'ID': 'exp7',
            'xsiType': 't1', 'subject_ID': 'sb3'}]

    experiment_details = formatter_object_connected.get_experiments_details(
        experiments)

    assert isinstance(experiment_details['Number of Experiments'], int)
    assert isinstance(experiment_details['Experiments/Project'], dict)
    assert isinstance(experiment_details['Experiment Types'], dict)


def test_get_scans_details():

    scans = 1
    scans_details = formatter_object_connected.get_scans_details(
        scans)

    assert scans_details == 1

    scans = [
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc1', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb3'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc4', 'xnat:imagescandata/type': 't1',
            'project': 'p1', 'xsiType': 'tx1',
            'xnat:imagesessiondata/subject_id': 'sb1'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb1',
            'xnat:imagescandata/id': 'sc3', 'xnat:imagescandata/type': 't3',
            'project': 'p3', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb2'},
        {
            'xnat:imagescandata/quality': 'questionable', 'ID': 'sb2',
            'xnat:imagescandata/id': 'sc2', 'xnat:imagescandata/type': 't3',
            'project': 'p4', 'xsiType': 'tx2',
            'xnat:imagesessiondata/subject_id': 'sb1'}]

    scans_details = formatter_object_connected.get_scans_details(
        scans)

    assert isinstance(scans_details['Number of Scans'], int)
    assert isinstance(scans_details['Scans/Project'], dict)
    assert isinstance(scans_details['Scans Quality'],  dict)
    assert isinstance(scans_details['Scan Types'], dict)
    assert isinstance(scans_details['XSI Scan Types'], dict)


def test_get_resources_details():

    resource_details = formatter_object_connected.get_resources_details()

    assert resource_details is None

    resources = [
        ['p1', 's1', 'r1', 'l1'],
        ['p1', 's2', 'r2', 'l2'],
        ['p1', 's2', 'r3', 'l3'],
        ['p1', 's3', 'r4', 'l4'],
        ['p2', 's3', 'r5', 'l5'],
        ['p2', 's3', 'r6', 'l6'],
        ['p2', 's1', 'r7', 'l7'],
        ['p1', 's1', 'r8', 'l8'],
        ['p9', 's5', 'No Data', 'No Data'],
        ['p9', 's9', 'No Data', 'No Data']]

    resource_details = formatter_object_connected.get_resources_details(
        resources)

    assert isinstance(resource_details, dict)
    assert len(resource_details) == 3

    resources_bbrc = [[
        'p1', 's1', 'r1', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-12-19'}}, 'Exists', '34.3\n'],
        ['p2', 's1', 'r3', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-11-10'}}, 'Not Exists', None],
        ['p2', 's2', 'r3', {'version': 'v3'}, 'Exists', '1.4\n'],
        ['p2', 's2', 'r3', 0, 'Not Exists', None],
        ['p3', 's1', 'r6', {
            'version': 'v2',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-9-20'}}, 'Not Exists', None],
        ['p1', 's2', 'r8', {
            'version': 'v1',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-10-21'}}, 'Exists', '4.3\n'],
        ['p1', 's3', 'r9', {
            'version': 'v2',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-08-22'}}, 'Not Exists', None],
        ['p1', 's4', 'r10', {
            'version': 'v3',
            'HasUsableT1': {'has_passed': True},
            'IsAcquisitionDateConsistent':
            {'has_passed': True, 'data': '2020-9-25'}}, 'Exists', '3.3\n']]

    resource_details = formatter_object_connected.get_resources_details(
        resources)

    resource_details_b = formatter_object_connected_b.get_resource_details(
        resources_bbrc)

    assert len(resource_details_b) == 7
    assert isinstance(resource_details, dict)
    assert len(resource_details) == 3
