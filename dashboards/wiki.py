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
                 if op.basename(e).startswith('bx_%s_' % command)]

        import pandas as pd
        from datetime import datetime
        links_section = []
        links_subsection = []
        b = ''
        for f in files:
            if command == 'spm12' and 't1t2' in f:
                subc = '_'.join(files[-1].split('_')[2:4])
            else:
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
                if command == 'spm12' and 't1t2' in f:
                    ds = '_'.join(f.split('_')[4:-2])
                else:
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
    title = 'Raw MRI and PET quality control'
    command = 'archiving'
    subcommand = True


class ASHSCard(Dictable):
    title = 'Hippocampal subfield volumetry (ASHS)'
    command = 'ashs'
    subcommand = True


class BraakCard(Dictable):
    title = 'Braak regions'
    command = 'braak'
    subcommand = True


class BamosCard(Dictable):
    title = 'White matter lesion segmentation (BAMOS)'
    command = 'bamos'
    subcommand = True


class BasilCard(Dictable):
    title = '2D-ASL cerebral perfusion quantification (BASIL)'
    command = 'basil'
    subcommand = True


class FreeSurfer7AparcCard(Dictable):
    title = 'Cortical thickness (FreeSurfer v7.1)'
    command = 'freesurfer7'
    subcommand = 'aparc'


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


class SignatureCard(Dictable):
    title = 'Cortical AD signature (FreeSurfer v7.1)'
    command = 'signature'
    subcommand = True
    desc = """Cortical thickness and GM volume of specific ROIs vulnerable to AD are determined using FreeSurfer 
            version 7.1. Jack's AD signature is calculated as the surface-area weighted average of individual 
            thickness and GM volume values from the following ROIs: bilateral entorhinal, inferior temporal, middle 
            temporal, and fusiform. Dickerson's AD and aging signatures are also computed, based solely on average 
            thickness values in signature-specific ROIs."""


class DONSURFCard(Dictable):
    title = 'Diffusion on cortical surface (DONSURF)'
    command = 'donsurf'
    subcommand = True
    desc = """Surface Mean Diffusivity (MD) averages derived from DWI data and projected onto the cortical surface."""


class PETFDGCard(Dictable):
    title = 'PET-FDG Glucose quantification'
    command = 'fdg'
    subcommand = True
    desc = """<b>FDG quantification pipeline steps</b>

            1. Realignment of all PET image volumes (via SPM12 Realign)
            2. Averaging of realigned PET images (via SPM12), saved as intermediate result file (static_pet.nii.gz)
            3. Optimized (smoothed) version of the averaged PET (optimized_static_pet.nii)
            4. Coregistration of averaged PET images and MRI T1w image to ICBM 152 atlas (via SPM12 Coregister)
            5. Coregistration of resulting PET image to T1 space (via SPM12 Coregister)
            6. Segmentation of T1 image (via SPM12 Segment), outputing the deformation fields and GM-tissue map
            7. Normalization of brain atlases to the T1w image space (via SPM12 Normalize).
            8. Normalization of PET, T1 and GM-tissue images (via SPM12 Normalize).
            9. Reslicing normalized atlas images to the T1w voxel space (via SPM12).
            10. Quantitative normalization:
                - global quantification: compute glucose SUVr for sensitive regions in the MNI space.
                - atlas-based regional quantification: ROI-specific SUVr measurements in the native space for the
                  AAL, Hammers and Desikan-Killiany atlases."""


class PETFTMCard(Dictable):
    title = 'PET-FTM Amyloid quantification'
    command = 'ftm'
    subcommand = True
    desc = """<b>Centiloid pipeline steps</b>

            1. Realignment of all PET image volumes (via SPM12 Realign)
            2. Averaging of realigned PET images (via SPM12), saved as intermediate result file (static_pet.nii.gz)
            3. Optimized (smoothed) version of the averaged PET (optimized_static_pet.nii)
            4. Coregistration of averaged PET images and MRI T1w image to ICBM 152 atlas (via SPM12 Coregister)
            5. Coregistration of resulting PET images to T1 space (via SPM12 Coregister)
            6. Segmentation of T1 image (via SPM12 Segment), outputing the deformation fields and GM-tissue map
            7. Normalization of brain atlases to the T1w image space (via SPM12 Normalize).
            8. Normalization of PET, T1 and GM-tissue images (via SPM12 Normalize).
            9. Reslicing normalized atlas images to the T1w voxel space (via SPM12).
            10. Quantitative normalization:
                - global quantification: compute Centiloid and cortical SUVr in the MNI space.
                - atlas-based regional quantification: ROI-specific SUVr measurements in the native space for the  
                    AAL, Hammers and Desikan-Killiany atlases."""


class ScandateCard(Dictable):
    title = 'Acquisition dates'
    command = 'scandates'


class BamosarterialCard(Dictable):
    title = 'White matter lesion quantification per brain arterial territories'
    command = 'bamosarterial'
    subcommand = True


class DTIAlpsCard(Dictable):
    title = 'DTI-ALPS index'
    command = 'alps'
    subcommand = True


class ASL3DCard(Dictable):
    title = '3D-ASL cerebral perfusion quantification'
    command = 'asl3d'
    subcommand = True


class LcmodelCard(Dictable):
    title = 'Metabolite concentrations on MR Spectroscopy images (LCMODEL)'
    command = 'lcmodel'
    subcommand = True


class CenTauRZCard(Dictable):
    title = 'Tau-PET quantification (CenTauRz)'
    command = 'tau'
    subcommand = True
    desc = """Dockerized SPM12 implementation of the CenTauR method for tau-PET quantification, as defined by the 
            GAAIN <a href="https://www.gaain.org/centaur-project">CenTauR project</a>. 
            CenTauRz values are standardized tau-PET z-scores relative to a reference group on the CenTauR scale.
            """
    

class PymentCard(Dictable):
    title = 'Brain Age (PYMENT)'
    command = 'pyment'
    subcommand = True
    desc = """Automated brain-age prediction from minimally preprocessed T1-weighted MRI data using pretrained 
            deep learning models from the <a href="https://github.com/estenhl/pyment-public">pyment-public</a> project"""


class SPM12Card(Dictable):
    title = 'Structural Volumes — T1 & T1/T2 Segmentation (SPM12)'
    command = 'spm12'
    subcommand = True