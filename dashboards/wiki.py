import bx
import dashboards
from flask import url_for
from dashboards import graph as g
from glob import glob
import os.path as op

commands = g.__find_all_commands__(bx, pattern='Command')
commands = {e.__name__.split('.')[-1].lower()[:-7]: e for e in commands}

translate = {'fdg': 'FDG',
             'ftm': 'FTM'}


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
        if op.isfile(fp2):
            img = '<img class="card-img-top" src="%s" alt="">' % fp
        bx_path = op.join(op.dirname(dashboards.__file__), 'app', 'protected', 'bx')
        all_bx = sorted(glob(op.join(bx_path, 'bx_*.xlsx')))
        command = self.command
        subcommand = getattr(self, 'subcommand', None)
        if subcommand not in (None, True):
            command += '_' + subcommand
        files = [op.basename(e) for e in all_bx
                 if op.basename(e).startswith('bx_%s' % command)]

        import pandas as pd
        from datetime import datetime
        links_section = []
        links_subsection = []
        b = ''
        for f in files:

            subc = f.split('_')[2]
            if subc != b:
                if len(links_subsection) != 0:
                    links_section.append(links_subsection)
                if subcommand is True or subcommand is not None:
                    header = '<b>Subcommand <span class="badge badge-info">%s</span></b> :<br/>' % translate.get(subc, subc)
                    links_subsection = [header]
                b = subc
            links = '<div style="padding:10px; margin-bottom:5px; margin-top:5px; border-left: 4px solid #17a2b8">'
            fn = f.split('.xlsx')[0]
            static_path = url_for('dashboards.protected',
                                  filename=op.join('bx', f))
            dt = datetime.strptime(fn[-15:], '%Y%m%d_%H%M%S')
            dt = dt.strftime('%B %d, %Y (%H:%M:%S)')
            df = pd.read_csv(op.join(bx_path, fn + '.csv'))
            columns = ['<span class="badge badge-secondary">%s</span>' % e
                       for e in list(df.columns)]
            n_subjects = len(set(df['ID']))

            ds = '_'.join(f.split('_')[2:-2])
            if subcommand is True or subcommand is not None:
                ds = '_'.join(f.split('_')[3:-2])

            links += 'Dataset: <span class="badge badge-dark">%s</span><br>' % ds
            links += '# subjects: <b>%s</b> <br/>' % str(n_subjects)
            links += 'Created on: <b>%s</b> <br/>' % dt
            links += 'Shape: <b>%s</b> rows x <b>%s</b> columns<br/>' % (len(df), len(columns))

            links += '<br/>Variables (%s) : ' % len(columns) + ' '.join(columns)
            links += '<br><a class="truncate-text" href="%s"><i class="fa fa-download"></i> %s</a></div>' % (static_path, f)

            links_subsection.append(links)
        links_section.append(links_subsection)
        links_section = ['<br>'.join(e) for e in links_section]

        links_section = '<hr>'.join(links_section)
        if links_section == '':
            links_section = '<img style="width:100%" src="/static/images/wip.png">'

        kwargs = {'title': self.title,
                  'desc': desc,
                  'name': command,
                  'img': img,
                  'links': links_section}
        return kwargs


class ArchivingCard(Dictable):
    title = 'Raw MRI quality control (archiving)'
    command = 'archiving'


class ASHSCard(Dictable):
    title = 'Hippocampal subfield segmentation (ASHS)'
    command = 'ashs'
    subcommand = True


class BraakCard(Dictable):
    title = 'Braak regions (FDG)'
    command = 'braak'
    subcommand = True


class BamosCard(Dictable):
    title = 'White matter lesion segmentation (BAMOS)'
    command = 'bamos'
    subcommand = True


class BasilCard(Dictable):
    title = 'Bayesian Inference for Arterial Spin Labeling MRI'
    command = 'basil'


class FreeSurfer6AparcCard(Dictable):
    title = 'Cortical thickness (FreeSurfer v6.0)'
    command = 'freesurfer6hires'
    subcommand = 'aparc'


class FreeSurfer7AparcCard(Dictable):
    title = 'Cortical thickness (FreeSurfer v7.1)'
    command = 'freesurfer7'
    subcommand = 'aparc'


class FreeSurfer6AsegCard(Dictable):
    title = 'Subcortical volumes (FreeSurfer v6.0)'
    command = 'freesurfer6hires'
    subcommand = 'aseg'


class FreeSurfer6HippoSfCard(Dictable):
    title = 'Hippocampal subfield volumetry (FreeSurfer v6.0)'
    command = 'freesurfer6hires'
    subcommand = 'hippoSfVolumes'


class FreeSurfer7AsegCard(Dictable):
    title = 'Subcortical volumes (FreeSurfer v7.1)'
    command = 'freesurfer7'
    subcommand = 'aseg'


class FreeSurfer7AmygNuclCard(Dictable):
    title = 'Amygdala Nuclei volumetry (FreeSurfer v7.1)'
    command = 'freesurfer7'
    subcommand = 'amygNucVolumes'


class FreeSurfer7HypothalCard(Dictable):
    title = 'Hypothalamic subunit segmentation (FreeSurfer v7.2)'
    command = 'freesurfer7'
    subcommand = 'hypothalamus'


class FreeSurfer7ThalamicCard(Dictable):
    title = 'Thalamic nuclei segmentation (FreeSurfer v7.2)'
    command = 'freesurfer7'
    subcommand = 'thalamus'


class FreeSurfer7BrainstemCard(Dictable):
    title = 'Brainstem segmentation (FreeSurfer v7.2)'
    command = 'freesurfer7'
    subcommand = 'brainstem'


class DONSURFCard(Dictable):
    title = 'Diffusion on cortical surface (DONSURF)'
    command = 'donsurf'
    subcommand = True


class PETFDGCard(Dictable):
    title = 'Landau signatures from PET-FDG'
    command = 'fdg'
    subcommand = True


class PETFTMCard(Dictable):
    title = 'Centiloid scale from PET-FTM'
    command = 'ftm'
    subcommand = True


class ScandateCard(Dictable):
    title = 'Acquisition dates'
    command = 'scandates'


class SignatureCard(Dictable):
    title = 'Cortical AD signature'
    command = 'signature'
    subcommand = True
