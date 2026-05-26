+++
date = '2026-05-26T11:24:46-07:00'
draft = false
title = 'Research Experience'
+++

## Overview
I received my B.S. in Physics with a specialization in Astrophysics from the
University of California, Irvine. As an undergraduate I joined the [Kirkby lab](https://faculty.sites.uci.edu/dkirkby/).
My undergraduate research worked with all-sky images that were taken at Kitt Peak National Observatory.
I developed a convolutional neural network (CNN) to identify clouds that were
moving towards and over the Mayall telescope. The results of this work can be
seen in my repo [kpno-allsky](https://github.com/dylanagreen/kpno-allsky).

As a graduate student I have remained in the Kirkby lab at UCI,
where my current research focuses on using deep learning to develop
data analysis pipelines. As part of the Kirkby lab I am also a part of both
the Dark Energy Spectroscopic Instrument (DESI) survey and the
Legacy Survey of Space and Time (LSST) / Dark Energy Science Collaboration (DESC).

### LSST/DESC
As part of my work in the DESC I participated in the [tomographic binning challenge](https://github.com/LSSTDESC/tomo_challenge)
which produced a paper that was published in the Open Journal of Astrophysics (see below).
My submission designed an entirely unique clustering algorithm and is outlined
in a jupyter notebook in my fork of the tomographic challenge repo.
Feel free to check out
the [jupyter notebook](https://github.com/dylanagreen/tomo_challenge/blob/master/notebooks/binning_as_clustering.ipynb).

### DESI
I am a [DESI builder](https://www.desi.lbl.gov/collaboration/desi-builders/),
and primarily contribute to the data systems and data pipeline development.

My first project aimed to use deep learning to identify and flag cosmic rays
that appear in spectroscopic images taken for the DESI Survey.
Additionally I wrote and maintain the [desipoint website](https://dylanagreen.github.io/desipoint/),
which is a web based displayer for the DESI project that displays the current
pointing of the telescope as well as a variety of other useful parameters.

Current work focuses on improving the Convolutional Neural Network (CNN) QuasarNet
so that it can better identify quasars using DESI spectroscopic data.
As part of this work I wrote the entirely numpy-based implementation of QuasarNet,
[QuasarNP](https://github.com/desihub/QuasarNP), which gets run as part of the
spectroscopic reduction pipeline for the DESI Survey. Recently we have
implemented an active learning pipeline that uses visual inspection to label
spectra which QuasarNET finds most useful to have labeled. This work has
produced a nearly 5% improvement in purity compared to the prior weights file.
These results will be included in DESI's Y3 public data release, date TBD.
A paper is in preparation for publication in 2025.

In 2023 I was awarded the DOE Office of Science Graduate Student Research Fellowship,
and worked for 4 months at Lawrence Berkeley Lab with Dr. Stephen Bailey on
Non-negative matrix factorization (NMF) and applications to the DESI pipeline. While
there I derived a variant of NMF we named [Nearly-NMF](https://doi.org/10.1109/TSP.2024.3474530), which introduces weighting
to standard NMF in a way that correctly handles the presence of *some* negative
data, compared to "standard" NMF which requires all input data to be factorized
to be strictly non-negative. A paper outlining this method was published in
late 2024. Further work outside the SCGSR program has continued to
apply the Nearly-NMF algorithm to real DESI data for possible inclusion
in the data processing pipeline.

I have 5 days of in person observation experience at the Mayall 4-meter telescope, where I did work commissioning the DESI spectrographs. I have since completed an additional 20 days of remote observing on the Mayall 4-meter. I also have observing experience at Lick Observatory as part of the 2020/21 Burbidge Observational Astronomy Workshop.

## Publications
1. DESI Collaboration incl. **Green, D.** (May 2026) 'Data Release 1 of the Dark Energy Spectroscopic Instrument' [The Astronomical Journal](https://doi.org/10.3847/1538-3881/ae4c43)
1. **Green, D.**, Kirkby, D. et al. (October 2025). 'Using Active Learning to Improve Quasar Identification for the DESI Spectra Processing Pipeline.' [Journal of Cosmology and Astroparticle Physic](https://doi.org/10.1088/1475-7516/2025/10/087)
1. DESI Collaboration incl. **Green, D.** (2025) 'DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints' [arXiv](https://arxiv.org/abs/2503.14738)
1. DESI Collaboration incl. **Green, D.** (2025) 'DESI DR2 Results I: Baryon Acoustic Oscillations from the Lyman Alpha Forest' [arXiv](https://arxiv.org/abs/2503.14739)
1. DESI Collaboration incl. **Green, D.** (September 2025) 'DESI 2024 V: Full-Shape Galaxy Clustering from Galaxies and Quasars' [Journal of Cosmology and Astroparticle Physics](https://doi.org/10.1088/1475-7516/2025/09/008)
1. DESI Collaboration incl. **Green, D.** (July 2025) 'DESI 2024 VII: Cosmological Constraints from the Full-Shape Modeling of Clustering Measurements' [Journal of Cosmology and Astroparticle Physics](https://iopscience.iop.org/article/10.1088/1475-7516/2025/07/028/pdf)
1. DESI Collaboration incl. **Green, D.** (July 2025) 'DESI 2024 II: Sample Definitions, Characteristics, and Two-point Clustering Statistics' [Journal of Cosmology and Astroparticle Physics](https://doi.org/10.1088/1475-7516/2025/07/017)
1. DESI Collaboration incl. **Green, D.** (April 2025) 'DESI 2024 III: baryon acoustic oscillations from galaxies and quasars' [Journal of Cosmology and Astroparticle Physics](https://doi.org/10.1088/1475-7516/2025/04/012)
1. DESI Collaboration incl. **Green, D.** (February 2025) 'DESI 2024 VI: cosmological constraints from the measurements of baryon acoustic oscillations' [Journal of Cosmology and Astroparticle Physics](https://dx.doi.org/10.1088/1475-7516/2025/02/021)
1. DESI Collaboration incl. **Green, D.** (January 2025) 'DESI 2024 IV: Baryon Acoustic Oscillations from the Lyman alpha forest' [Journal of Cosmology and Astroparticle Physics](https://dx.doi.org/10.1088/1475-7516/2025/01/124)
1. **Green, D.** & Bailey, S. (October 2024). Algorithms for Non-Negative Matrix Factorization on Noisy Data With Negative Values. [IEEE Transactions on Signal Processing](https://doi.org/10.1109/TSP.2024.3474530)
1. DESI Collaboration incl. **Green, D.** 'The Early Data Release of the Dark Energy Spectroscopic Instrument.' (August 2024) [The Astronomical Journal](https://doi.org/10.3847/1538-3881/ad3217)
1. DESI Collaboration incl. **Green, D.** 'Validation of the Scientific Program for the Dark Energy Spectroscopic Instrument.' (January 2024). [*The Astronomical Journal, 167, 62*](https://dx.doi.org/10.3847/1538-3881/ad0b08)
1. Guy, J., Bailey, S., ... **Green, D.** ..., Zou, H. ‘The Spectroscopic Data Processing Pipeline for the Dark Energy Spectroscopic Instrument’. (April 2023) [*The Astronomical Journal  165, 144.*](https://doi.org/10.3847/1538-3881/acb212)
1. DESI Collaboration, incl. **Green, D.** ‘Overview of the Instrumentation for the Dark Energy Spectroscopic Instrument’. (November 2022) [*The Astronomical Journal 164, 207.*](https://doi.org/10.3847/1538-3881/ac882b)
1. Pat, F., Juneau, S., Böhm, V., ... **Green, D.**, Myers, A. 'Reconstructing and Classifying SDSS DR16 Galaxy Spectra with Machine-Learning and Dimensionality Reduction Algorithms.' (November 2022) [arXiv: 2211.11783](https://arxiv.org/abs/2211.11783)
1. Zuntz, J., Lanusse, F., Malz, A. I., Wright, A. H., Slosar, A., Abolfathi, B., ... **Green, D.** ... & Mao, Y. Y. ‘The LSST-DESC 3x2pt Tomography Optimization Challenge’. (October 2021) [*The Open Journal of Astrophysics 4, 13.*](https://doi.org/10.21105/astro.2108.13418)
1. Dethe, T., Gill, H., **Green, D.**, Greensweight, A., Gutierrez, L., He, M., Tajima, T., & Yang, K. ‘Causality and dispersion relations’. *American Journal of Physics* 87, no. 4 (April 2019): 279–90. [doi:10.1119/1.5092679.](https://doi.org/10.1119/1.5092679)


## Presentations
1. **Green, D.** (2022, June 24). [The Future of QuasarNP](/assets/presentations/06_24_22_future_of_qnp.pdf) DESI Collaboration Meeting June 2022, Online
2. **Green, D.** (2021, April 15). [Automated Classification of Quasar Targets in DESI.](/assets/presentations/04_15_21_qnp_research_forum.pdf) DESI Research Forum, Online.
3. **Green, D.** (2021, February 26). [Deep Learning for Cosmic Ray Identification](/assets/presentations/02_26_21_deepCR_spectro.pdf) desi-data Telecon, Online.
