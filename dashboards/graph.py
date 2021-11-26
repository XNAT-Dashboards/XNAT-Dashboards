import pandas as pd
from collections import OrderedDict
import os.path as op
import json
import dashboards
from dashboards import filter


def __get_modules__(m):
    import pkgutil
    import logging as log
    modules = []
    prefix = m.__name__ + '.'
    log.info('prefix : %s' % prefix)
    for importer, modname, ispkg in pkgutil.iter_modules(m.__path__, prefix):
        module = __import__(modname, fromlist='dummy')
        if not ispkg:
            modules.append(module)
        else:
            modules.extend(__get_modules__(module))
    return modules


def __find_all_commands__(m, pattern='Graph'):
    """Browses bx and looks for any class named as a Command"""
    import inspect
    modules = []
    classes = []
    modules = __get_modules__(m)
    forbidden_classes = []  # Test, ScanTest, ExperimentTest]
    for m in modules:
        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and pattern in name \
                    and obj not in forbidden_classes:
                classes.append(obj)
    return classes


class BarChart():
    def get_drill(self, g, data):
        res = {}
        for k, v in g['list'].items():
            for item in v:
                res.setdefault(k, []).append(item)
        return res

    def get_chart(self, id, p):
        g = self.get_data(id, p)
        if g['name'] in ['Dates difference (Acquisition date - Insertion date)',
                         'Scans per session']:
            print('toto', g['name'])
            if 'count' not in g.keys():
                raise KeyError("'count' key missing")
            x, y = list(g['count'].keys()), list(g['count'].values())
        else:
            sd = OrderedDict(sorted(g['count'].items(), key=lambda dct: dct[1]))
            x, y = (list(sd.keys()), list(sd.values()))

        data = [{'x': x,
                 'y': y,
                 'type': 'bar',
                 'marker': {'color': g['color']}}]
        layout = {'title': g['name'],
                  'margin': {'l': 100, 'r': 100, 'b': 100, 't': 100}}

        drill = self.get_drill(g, data)
        return (g['id'], data, layout, g.get('id_type', 'other'), g['description'],
                g['name'], drill, g['type'])


class PieChart():
    def get_drill(self, g, data):
        res = {}
        for k, v in g['list'].items():
            for item in v:
                res.setdefault(k, []).append(item)
        return res

    def get_chart(self, id, p):
        g = self.get_data(id, p)

        sd = OrderedDict(sorted(g['count'].items(), key=lambda dct: dct[1]))
        x, y = (list(sd.keys()), list(sd.values()))

        color = g['color']
        colors = ['#00b33c', '#c299ff', '#660066', '#0033cc', ' #009999',
                  '#cccc00', '#ff0066', '#996633', ' #ffaa80', '#99cc00',
                  '#cc00ff', '#ffff99', '#666699', '#000099']
        import random
        if len(x) > len(color):
            n = len(x) - len(color)
            for i in range(0, n):
                c = colors[random.randint(0, len(colors) - 1)]
                color.append(c)

        data = [{'labels': x,
                 'values': y,
                 'type': 'pie'}]
        layout = {'title': g['name'],
                  'colorway': color}

        drill = self.get_drill(g, data)
        return (g['id'], data, layout, g.get('id_type', 'other'), g['description'],
                g['name'], drill, g['type'])


class StackedBarChart():
    def get_drill(self, g, data):
        res = {}
        for k, v in g['list'].items():
            for k2, v2 in v.items():
                res.setdefault(k, {})
                res[k].setdefault(k2, []).append(v2)
        return res

    def get_chart(self, id, p):
        g = self.get_data(id, p)
        x = list(g['count'].keys())

        differ_keys = []
        for k, v in g['count'].items():
            for y in v.keys():
                differ_keys.append(y)
        differ_keys = list(set(differ_keys))

        color = g['color']
        colors = ["#00b33c", "#c299ff", "#660066", "#0033cc", " #009999",
                  "#cccc00", "#ff0066", "#996633", " #ffaa80", "#99cc00",
                  "#cc00ff", "#ffff99", "#666699", "#000099"]
        import random
        if len(x) > len(color):
            n = len(x) - len(color)
            for i in range(0, n):
                c = colors[random.randint(0, len(colors) - 1)]
                color.append(c)

        data = []

        for i in differ_keys:
            y = []
            for k, v in g['count'].items():
                if i in v.keys():
                    y.append(v[i])
                else:
                    y.append(0)
            trace = {'x': x,
                     'y': y,
                     'type': 'bar',
                     'name': i}
            data.append(trace)
        layout = {'title': g['name'],
                  'colorway': color,
                  'barmode': 'stack',
                  'xaxis': {"categoryorder": "total ascending"},
                  'margin': {'l': 100, 'r': 100, 'b': 100, 't': 100}
                  }

        drill = self.get_drill(g, data)
        return (g['id'], data, layout, g.get('id_type', 'other'), g['description'],
                g['name'], drill, g['type'])


class LineChart():

    def get_chart(self, id, p):
        g = self.get_data(id, p)
        data = []
        for k, v in g['count'].items():
            x, y = list(v.keys()), list(v.values())
            trace = {'x': x,
                     'y': y,
                     'type': 'scatter',
                     'name': k}
            data.append(trace)

        color = g['color']
        colors = ["#00b33c", "#c299ff", "#660066", "#0033cc", " #009999",
                  "#cccc00", "#ff0066", "#996633", " #ffaa80", "#99cc00",
                  "#cc00ff", "#ffff99", "#666699", "#000099"]
        import random
        if len(g['count'].keys()) > len(color):
            n = len(g['count'].keys()) - len(color)
            for i in range(0, n):
                c = colors[random.randint(0, len(colors) - 1)]
                color.append(c)

        layout = {'title': g['name'],
                  'colorway': color}

        return (g['id'], data, layout, g.get('id_type', 'other'), g['description'],
                g['name'], None, g['type'])


class ProjectGraph(BarChart):
    name = 'Projects'
    type = 'bar'
    description = 'Shows available projects (and their accessibility).'
    visibility = ["admin", "superuser", "guest"]
    color = "#7394CB"
    id_type = 'project'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        data, x, y = p['projects'], 'project_access', 'id'
        df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
        res = filter.res_df_to_dict(df, x, y)
        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)

        return res


class PerProjectSessionGraph(StackedBarChart):
    name = 'Imaging sessions'
    type = 'stacked_bar'
    description = "Shows sessions per available project."
    visibility = ["admin", "superuser", "guest"]
    color = ["#00cc99", "#ff80ff"]
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        res = filter.res_df_to_stacked(p['experiments'], 'project', 'xsiType', 'ID')
        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class SubjectGraph(BarChart):
    name = "Subjects"
    type = 'bar'
    description = "Shows subjects per available project."
    visibility = ["admin", "superuser"]
    color = "#f3cec9"
    id_type = 'subject'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        data, x, y = p['subjects'], 'project', 'ID'
        df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
        res = filter.res_df_to_dict(df, x, y)
        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class SessionGraph(BarChart):
    name = "Total amount of sessions"
    type = "bar"
    description = "Shows the grand total of available imaging sessions."
    visibility = ["admin", "superuser"]
    color = "#e60000"
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        data, x, y = p['experiments'], 'xsiType', 'ID'
        df = pd.DataFrame([[e[x], e[y]] for e in data], columns=[x, y])
        res = filter.res_df_to_dict(df, x, y)
        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ScanQualityGraph(PieChart):
    name = "Scan quality"
    type = "pie"
    description = "Shows proportions of scans marked as usable, unusable or questionable.",
    visibility = ["admin", "superuser"]
    color = ["#cc0066", "#cc66cc", "#00ace6"]
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        columns = ['xnat:imagescandata/quality', 'ID', 'xnat:imagescandata/id']
        x, y = columns[:2]
        df = pd.DataFrame([[e[x], e[y]] for e in p['scans']], columns=columns[:2])
        df[x].replace({'': 'No Data'}, inplace=True)
        res = filter.res_df_to_dict(df, x, y)
        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ScanTypeGraph(BarChart):
    name = "Scan Types"
    type = "bar"
    description = "Shows the types of scans present in the project."
    visibility = ["admin", "superuser"]
    color = "#ffdb4d"
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id

        fn = dashboards.__file__
        fp = op.join(op.dirname(fn), '..', 'whitelist.json')
        whitelist = json.load(open(fp))
        filtered_scans = [s for s in p['scans']
                          if s['xnat:imagescandata/type'] in whitelist]
        columns = ['xnat:imagescandata/type', 'ID', 'xnat:imagescandata/id']
        x, y = columns[:2]
        df = pd.DataFrame([[e[x], e[y]] for e in filtered_scans],
                          columns=[x, y])
        res = filter.res_df_to_dict(df, x, y)

        for e in ['name', 'id', 'id_type', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ResourcePerTypeGraph(BarChart):
    name = "Resources per type"
    type = "bar"
    description = "Shows numbers of resources per type."
    visibility = ["admin"]
    color = "#FB9A99"

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        resources = [e for e in p['resources'] if len(e) == 4]
        res = filter.get_nres_per_type(resources)
        for e in ['name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class UsableT1SessionGraph(PieChart):
    name = "Sessions with usable T1"
    type = "pie"
    description = "Shows proportions of sessions including a T1-weighted "\
        "scan marked as usable. The test HasUsableT1, which is part of the "\
        "ArchivingValidator process (bbrc-validator), determines if the "\
        "session has a usable T1-weighted scan suited for further processing."\
        " This test passes either if there is one unique and valid sequence"\
        " labelled as T1 or if, in case of multiple matches, only one of them"\
        " is labelled as usable. Fails otherwise. No data refers to"\
        " sessions for which the test has not been completed."
    visibility = ["admin"]
    id_type = 'experiment'
    color = ["#ff66ff", "#70db70", "#ffb84d"]

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        br = [e for e in p['resources'] if len(e) > 4]

        from dashboards import bbrc
        columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
                   'Insert date']
        data = pd.DataFrame(br, columns=columns).set_index('Session')
        tests = bbrc.get_tests(data, ['HasUsableT1', 'IsAcquisitionDateConsistent'])
        data = data.join(tests).reset_index()

        # Usable t1
        res = filter.res_df_to_dict(data, 'HasUsableT1', 'Session')
        for e in ['id_type', 'name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class VersionGraph(PieChart):
    name = "Version Distribution"
    type = "pie"
    description = "Different versions of Archiving validator for each session."
    visibility = ["admin"]
    color = ["#54a0ff", "#00b894"]
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        br = [e for e in p['resources'] if len(e) > 4]

        from dashboards import bbrc
        columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
                   'Insert date']
        data = pd.DataFrame(br, columns=columns).set_index('Session')
        tests = bbrc.get_tests(data, ['HasUsableT1', 'IsAcquisitionDateConsistent'])
        data = data.join(tests).reset_index()
        # Version Distribution
        res = filter.res_df_to_dict(data, 'version', 'Session')
        for e in ['name', 'id', 'color', 'description', 'type', 'id_type']:
            res[e] = getattr(self, e)
        return res


class ValidatorGraph(StackedBarChart):
    name = "BBRC validators"
    type = "stacked_bar"
    description = "Shows the percentage of validators across all available"\
                  " sessions with BBRC validator resource.",
    visibility = ["admin"]
    color = ["#ff9900", "#1abc9c"]

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        br = [e for e in p['resources'] if len(e) > 4]

        from dashboards import bbrc
        columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
                   'Insert date']
        data = pd.DataFrame(br, columns=columns).set_index('Session')
        tests = bbrc.get_tests(data, ['HasUsableT1', 'IsAcquisitionDateConsistent'])
        data = data.join(tests).reset_index()
        res = bbrc.which_sessions_have_validators(data)
        for e in ['name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ConsistentAcquisitionDateGraph(PieChart):
    name = "Is acquisition date consistent across the whole session?"
    type = "pie"
    description = "Displays percentages of sessions showing the same "\
        "acquisition date (should be the normal case). Relies on test "\
        "'IsAcquisitionDateConsistent' which is part of ArchivingValidator."\
        "A session is composed of a set of scans (images) acquired at"\
        "specific timepoints, usually (but not mandatorily) all on the same"\
        " day. This test checks whether the date of an imaging session is"\
        " consistent across its scans, comparing the session 'date' attribute"\
        " (XNAT) with the 'AcquisitionDate' field from the headers of the"\
        " first DICOM file in each scan. This test passes if dates match"\
        " between session and scans. Fails otherwise. No data refers to"\
        " cases where this test has not been completed."
    visibility = ["admin"]
    color = ["#2ecc71", "#3498db", "#9b59b6"]
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        br = [e for e in p['resources'] if len(e) > 4]

        from dashboards import bbrc
        columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
                   'Insert date']
        data = pd.DataFrame(br, columns=columns).set_index('Session')
        tests = bbrc.get_tests(data, ['HasUsableT1', 'IsAcquisitionDateConsistent'])
        data = data.join(tests).reset_index()

        # consistent_acq_date
        res = filter.res_df_to_dict(data, 'IsAcquisitionDateConsistent', 'Session')
        for e in ['id_type', 'name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class DateDifferenceGraph(BarChart):
    name = "Dates difference (Acquisition date - Insertion date)"
    type = "bar"
    description = "Difference between insertion dates and acquisition dates"\
        " per session, if acquisition date present in session test."
    visibility = ["admin"]
    color = "#66ffff"

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id

        from dashboards import bbrc
        resources = [e for e in p['resources'] if len(e) > 4]
        columns = ['Project', 'Session', 'archiving_validator', 'BBRC_Validators',
                   'Insert date']
        data = pd.DataFrame(resources, columns=columns).set_index('Session')
        res = bbrc.diff_dates(data)

        for e in ['name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class SessionsPerSubjectGraph(PieChart):
    name = "Sessions per subject"
    type = "pie"
    description = "Shows numbers of sessions per subject (in proportions)."
    visibility = ["admin", "superuser"]
    color = ["#ccccff", "#ffa31a", "#ffff33"]
    id_type = 'subject'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        res = filter.proportion_graphs(p['experiments'], 'subject_ID', 'ID', 'Subjects with ', ' experiment(s)')
        for e in ['id_type', 'name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ScansPerSessionGraph(BarChart):
    name = "Scans per session"
    type = "bar"
    description = "Shows number of scans per session."
    visibility = ["admin", "superuser"]
    color = "#666699"
    id_type = 'experiment'

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        res = filter.proportion_graphs(p['scans'], 'ID', 'xnat:imagescandata/id', '', ' scans')
        for e in ['id_type', 'id', 'name', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ResourcesPerSessionGraph(StackedBarChart):
    name = "Resources per session"
    type = "stacked_bar"
    description = "Shows numbers of resources per session per project."
    visibility = ["admin"]
    color = ["#33cccc", "#5cd65c", "#ff9900", "#c44dff", "#ff1a1a",
             "#66a3ff", "#cc9900", "#c2c2d6", "#00ffff", "#993333",
             "#336600", "#660066"]

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        resources = [e for e in p['resources'] if len(e) == 4]
        res = filter.get_nres_per_session(resources)
        for e in ['name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res


class ResourcesOverTimeGraph(LineChart):
    name = "Resources (over time)"
    type = "line"
    description = "Shows the grand total of resources - among various types"\
        "- day after day."
    visibility = ["admin", "superuser", "guest"]
    color = ["#ffff1a", "#ff4dff", "#33cc33", "#0099ff", "#ff9900"]

    def __init__(self):
        pass

    def get_data(self, id, p):
        self.id = id
        res = {'count': p['longitudinal_data']}
        for e in ['name', 'id', 'color', 'description', 'type']:
            res[e] = getattr(self, e)
        return res
