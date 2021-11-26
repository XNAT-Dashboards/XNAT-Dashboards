import bx
import dashboards
from flask import url_for
from dashboards import graph as g
from dashboards import config
from glob import glob
import os.path as op


items2 = ['Subcortical volumes (FreeSurfer v6.0)',
         'Cortical thickness (FreeSurfer v7.1)',
         'Subcortical volumes (FreeSurfer v7.1)'
         'Centiloid scale from PET-FTM',
         'Cortical AD signature (Jack et al.)',
         'Cortical AD signature (Dickerson et al.)']

commands = g.__find_all_commands__(bx, pattern='Command')
commands = {e.__name__.split('.')[-1].lower()[:-7]: e for e in commands}


class Dictable():

    def __init__(self):
        pass

    def to_dict(self):
        desc = commands[self.command].__doc__.replace('\n\n', '<br/><br/>')
        ref = ''
        if 'References' in desc:
            ref = '<br/>References:</br>' + \
                  desc.split('References:')[1].replace('\n', '<br/>')
        desc = desc.split('Available subcommands:')[0] + ref

        fp = '/static/images/%s.jpg' % self.__class__.__name__.split('Card')[0].lower()
        img = ''
        fp2 = op.join(op.dirname(dashboards.__file__), 'app', fp[1:])
        print(fp2)
        if op.isfile(fp2):
            img = '<img class="card-img-top" src="%s" alt="">' % fp

        all_bx = glob(op.join(config.BX_PATH, 'bx_*.xlsx'))
        files = [op.basename(e) for e in all_bx
                 if op.basename(e).startswith('bx_%s' % self.command)]

        import pandas as pd
        from datetime import datetime
        links_section = []
        for f in files:
            links = ''
            fn = f.split('.xlsx')[0]
            static_path = url_for('dashboards.protected', filename=f)

            links += '<br><a href="%s">%s</a><br/><br/>' % (static_path, f)
            dt = datetime.strptime(fn[-15:], '%Y%m%d_%H%M%S')
            dt = dt.strftime('%B %d, %Y (%H:%M:%S)')
            df = pd.read_csv(op.join(config.BX_PATH, fn + '.csv'))
            columns = ['<span class="badge badge-secondary">%s</span>' % e
                       for e in list(df.columns)]
            n_subjects = len(set(df['ID']))

            links += '# subjects: <b>%s</b> <br/>' % str(n_subjects)
            links += 'Created on: <b>%s</b> <br/>' % dt
            links += 'Shape: <b>%s</b> rows x <b>%s</b> columns<br/>' % (len(df), len(columns))

            links += '<br/>Variables (%s) : ' % len(columns) + ' '.join(columns)
            links_section.append(links)

        kwargs = {'title': self.title,
                  'desc': desc,
                  'img': img,
                  'links': '<hr>'.join(links_section)}
        return kwargs


class ArchivingCard(Dictable):
    title = 'Raw MRI quality control (archiving)'
    command = 'archiving'


class ASHSCard(Dictable):
    title = 'Hippocampal subfield segmentation (ASHS)'
    command = 'ashs'


class BraakCard(Dictable):
    title = 'Braak regions'
    command = 'braak'


class BamosCard(Dictable):
    title = 'White matter lesion segmentation (BAMOS)'
    command = 'bamos'


class FreeSurfer6Card(Dictable):
    title = 'Cortical thickness (FreeSurfer v6.0)'
    command = 'freesurfer6'


class FreeSurfer7Card(Dictable):
    title = 'Cortical thickness (FreeSurfer v7.1)'
    command = 'freesurfer7'


class DONSURFCard(Dictable):
    title = 'Diffusion on cortical surface (DONSURF)'
    command = 'donsurf'


class PETFDGCard(Dictable):
    title = 'Landau signatures from PET-FDG'
    command = 'fdg'


class PETFTMCard(Dictable):
    title = 'Centiloid scale from PET-FTM'
    command = 'ftm'


class ScandateCard(Dictable):
    title = 'Acquisition dates'
    command = 'scandates'


class SignatureJackCard(Dictable):
    title = 'Cortical AD signature (Jack et al.)'
    command = 'signature'
