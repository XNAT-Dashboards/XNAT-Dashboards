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
        extra_desc = getattr(self, 'desc', '').replace('\n', '<br/>')
        if extra_desc != '':
            extra_desc = '<br><br><div style="border: 0.5px #AAAAAA solid; padding:15px; font-size:10px"> %s </div>' % extra_desc
        url = getattr(commands[self.command], 'url', '')
        if url != '':
            url = '<div style="text-align:right;"><a href="%s">🔗 (click for more details)</a></div><br>' % url
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
            if (subcommand is True or subcommand is not None) and subc != b:
                if len(links_subsection) != 0:
                    links_section.append(links_subsection)
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
                  'url': url,
                  'extra_desc': extra_desc,
                  'links': links_section}
        return kwargs


class ArchivingCard(Dictable):
    title = 'Raw MRI quality control (archiving)'
    command = 'archiving'
    subcommand = True


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
    subcommand = True


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


class FreeSurfer7HippoSfCard(Dictable):
    title = 'Hippocampal subfield volumetry (FreeSurfer v7.1)'
    command = 'freesurfer7'
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
    desc = """<b>Hypothalamic Subunits</b>

            Automated segmentation of the hypothalamus and its associated subunits in T1w
            scans of ~1mm isotropic resolution using a convolutional neural network. Produces
            segmentation maps for 5 subregions:

            Anterior-inferior: suprachiasmatic nucleus; supraoptic nucleus (SON)
            Anterior-superior: preoptic area; paraventricular nucleus (PVN)
            Posterior: mamillary body (including medial and lateral mamillary nuclei);
            lateral hypothalamus; tuberomamillary nucleus (TMN)
            Inferior tubular: infundibular (or arcuate) nucleus; ventromedial nucleus;
            SON; lateral tubular nucleus; TMN
            Superior tubular: dorsomedial nucleus; PVN; lateral hypothalamus


            <i>Automated segmentation of the hypothalamus and associated subunits in brain MRI.</i>
            Billot B. et al. (DOI: <a href="https://doi.org/10.1016/j.neuroimage.2020.117287">10.1016/j.neuroimage.2020.117287</a>)"""


class FreeSurfer7ThalamicCard(Dictable):
    title = 'Thalamic nuclei segmentation (FreeSurfer v7.2)'
    command = 'freesurfer7'
    subcommand = 'thalamus'
    desc = """<b>Thalamic Nuclei</b>

            Parcellation of the thalamus into 25 different nuclei, using a probabilistic
            atlas built with histological data. The parcellation is based on the main T1w
            scan processed through recon-all.

            <i>A probabilistic atlas of the human thalamic nuclei combining ex vivo MRI and histology.</i>
            Iglesias J.E. et al. (DOI: <a href="https://doi.org/10.1016/j.neuroimage.2018.08.012">10.1016/j.neuroimage.2018.08.012</a>)"""


class FreeSurfer7BrainstemCard(Dictable):
    title = 'Brainstem segmentation (FreeSurfer v7.2)'
    command = 'freesurfer7'
    subcommand = 'brainstem'
    desc = """<b>Brainstem Substructures</b>

            Automated segmentation of four different brainstem structures from the input T1
            scan: medulla oblongata, pons, midbrain and superior cerebellar peduncle (SCP).

            <i>Bayesian segmentation of brainstem structures in MRI.</i> Iglesias J.E. et al.
            (DOI: <a href="https://doi.org/10.1016/j.neuroimage.2015.02.065">10.1016/j.neuroimage.2015.02.065</a>)"""


class FreeSurfer7JackCard(Dictable):
    title = 'Cortical AD signature (FreeSurfer v7.1)'
    command = 'freesurfer7'
    subcommand = 'jack'
    desc = """FreeSurfer version 7.1 is used to determine the thickness of specific
        regions of interest (ROIs) vulnerable to AD. The Jack's <i>AD signature<i> is calculated as the surface-area
        weighted average of the individual thickness values of the following ROIs: entorhinal, inferior
        temporal, middle temporal, and fusiform in both hemispheres."""


class DONSURFCard(Dictable):
    title = 'Diffusion on cortical surface (DONSURF)'
    command = 'donsurf'
    subcommand = True


class PETFDGCard(Dictable):
    title = 'Landau signatures from PET-FDG'
    command = 'fdg'
    subcommand = True
    desc = """<b>FDG quantification pipeline steps</b>

            1. Data fetching: given an XNAT PETSession, pulls a PET_FDG_4x5min scan image (NIfTI)
            and a T1_ALFA1 scan image from a closer MRSession from the same subject.
            2. Realignment of all PET image volumes (via SPM12 Realign)
            3. Averaging of realigned PET images (via FSL), saved as intermediate result file (static_pet.nii.gz)
            4. Optimized (smoothed) version of the averaged PET (optimized_static_pet.nii)
            5. Coregistration of averaged PET images and MRI T1w image to ICBM 152 atlas (via SPM12 Coregister)
            6. Coregistration of resulting PET image to T1 space (via SPM12 Coregister)
            7. Segmentation of T1 image (via SPM12 NewSegment), outputing the deformation fields and the GM-tissue image
            8. Normalization of PET, T1 and GM-tissue images (via SPM12 Normalize)
            9. Compute quantification metrics from the input PET images for different regions of reference
            (including cortex, resilience signature and Landau metaROIs SUVr values). Also compute regional quantification
            (cortex SUVr) metrics using AAL and
            Hammers atlases as references.
            10. Results uploading into XNAT as FDG_QUANTIFICATION PETSession resource
            11. Notification: When configured, notify via email the end-user(s)"""


class PETFTMCard(Dictable):
    title = 'Centiloid scale from PET-FTM'
    command = 'ftm'
    subcommand = True
    desc = """<b>Centiloid pipeline steps</b>

            1. Data fetching: given an XNAT PETSession, pulls a PET_Flutemetamol_4x5min scan image (NIfTI)
            and a T1_ALFA1 scan image from a closer MRSession from the same subject.
            2. Realignment of all PET image volumes (via SPM12 Realign)
            3. Averaging of realigned PET images (via FSL), saved as intermediate result file (static_pet.nii.gz)
            4. Optimized (smoothed) version of the averaged PET (optimized_static_pet.nii)
            5. Coregistration of averaged PET images and MRI T1w image to ICBM 152 atlas (via SPM12 Coregister)
            6. Coregistration of resulting PET images to T1 space (via SPM12 Coregister)
            7. Segmentation of T1 image (via SPM12 NewSegment), outputing the deformation fields and the GM-tissue image
            8. Normalization of PET, T1 and GM-tissue images (via SPM12 Normalize)
            9. Compute quantification metrics from the input PET images for different regions of reference
            (including Centiloid and cortex SUVr values). Also compute atlas-based regional quantification
            (cortex SUVr) metrics using AAL and
            Hammers atlases as references.
            10. Results uploading into XNAT as FTM_QUANTIFICATION PETSession resource
            11. Notification: When configured, notify via email the end-user(s)"""


class ScandateCard(Dictable):
    title = 'Acquisition dates'
    command = 'scandates'


class SignatureCard(Dictable):
    title = 'Cortical AD signature'
    command = 'signature'
    subcommand = True
    desc = """FreeSurfer version 6.0 is used to determine the thickness of specific
            regions of interest (ROIs) vulnerable to AD. The Jack's <i>AD signature</i> is calculated as the surface-area
            weighted average of the individual thickness values of the following ROIs: entorhinal, inferior
            temporal, middle temporal, and fusiform in both hemispheres."""
