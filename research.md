@def title = "Research Experience"

# Research Experience
\tableofcontents

## Overview
I received my B.S. in Physics with a specialization in Astrophysics from the
University of California, Irvine. As an undergraduate I joined the [Kirkby lab](https://faculty.sites.uci.edu/dkirkby/).
My research worked with all-sky images that were taken at Kitt Peak National Observatory.
I developed a convolutional neural network (CNN) to identify clouds that were
moving towards and over the Mayall telescope. The results of this work can be
seen in my repo [kpno-allsky](https://github.com/dylanagreen/kpno-allsky).

As a graduate student I have remained in the Kirkby lab at UCI,
where my current research focuses on using deep learning to develop
data analysis pipelines. As part of the Kirkby lab I am also a part of both
the Dark Energy Spectroscopic Instrument (DESI) survey and the
Legacy Survey of Space and Time (LSST) / Dark Energy Science Collaboration (DESC).
My first project aimed to use deep learning to identify and flag cosmic rays
that appear in spectroscopic images taken for the DESI Survey.
Additionally I wrote and maintain the [desipoint website](https://dylanagreen.github.io/desipoint/),
 which is a web based displayer for the DESI project that displays the current
 pointing of the telescope as well as a variety of other useful parameters.

As part of my work in the DESC I participated in the [tomographic binning challenge](https://github.com/LSSTDESC/tomo_challenge)
which produced a paper that was published in the Open Journal of Astrophysics (see below).
My submission designed an entirely unique clustering algorithm and is outlined
in a jupyter notebook in my fork of the tomographic challenge repo.
I am currently considering rewriting the clustering parts of the notebook into a
paper-styled note for this website, but in the meantime feel free to check out
the [jupyter notebook](https://github.com/dylanagreen/tomo_challenge/blob/master/notebooks/binning_as_clustering.ipynb).

My current work focuses on improving the Convolutional Neural Network (CNN) QuasarNet
so that it can better identify quasars using DESI spectroscopic data.
As part of this work I wrote the entirely numpy-based implementation of QuasarNet,
[QuasarNP](https://github.com/desihub/QuasarNP), which gets run as part of the
spectroscopic reduction pipeline for the DESI Survey. Recently we have
implemented an active learning pipeline that uses visual inspection to label
spectra which QuasarNET finds most useful to have labeled. This work has
produced a nearly 5% improvement in purity compared to the prior weights file.
These results are intended to be included in DESI's first public data release
in late 2023. This work is currently planned to produce a paper on a
similar timeline.

I have 5 days of in person observation experience at the Mayall 4-meter telescope, where I did work commissioning the DESI spectrographs. I have since completed an additional 16 days of remote observing on the Mayall 4-meter. I also have observing experience at Lick Observatory as part of the 2020/21 Burbidge Observational Astronomy Workshop.

## Publications
[Orcid](https://orcid.org/0000-0002-0676-3661)
1. Dethe, T., Gill, H., **Green, D.**, Greensweight, A., Gutierrez, L., He, M., Tajima, T., & Yang, K. ‘Causality and dispersion relations’. *American Journal of Physics* 87, no. 4 (April 2019): 279–90. [doi:10.1119/1.5092679.](https://doi.org/10.1119/1.5092679)
2. Zuntz, J., Lanusse, F., Malz, A. I., Wright, A. H., Slosar, A., Abolfathi, B., ... **Green, D.** ... & Mao, Y. Y. ‘The LSST-DESC 3x2pt Tomography Optimization Challenge’. *The Open Journal of Astrophysics* 4, no. 1 (October 2021): 13. [doi:10.21105/astro.2108.13418.](https://doi.org/10.21105/astro.2108.13418)
3. DESI Collaboration, incl. **Green, D.** ‘Overview of the Instrumentation for the Dark Energy Spectroscopic Instrument’. *The Astronomical Journal* 164, no. 5 (November 2022): 207. [doi:10.3847/1538-3881/ac882b.](https://doi.org/10.3847/1538-3881/ac882b)
4. Guy, J., Bailey, S., ... **Green, D.** ..., Zou, H. ‘The Spectroscopic Data Processing Pipeline for the Dark Energy Spectroscopic Instrument’. *The Astronomical Journal*  165, no. 4 (April 2023): 144. [doi:10.3847/1538-3881/acb212.](https://doi.org/10.3847/1538-3881/acb212)

## Presentations
1. **Green, D.** (2021, February 26). [Deep Learning for Cosmic Ray Identification](/assets/presentations/02_26_21_deepCR_spectro.pdf) desi-data Telecon, Online.
2. **Green, D.** (2021, April 15). [Automated Classification of Quasar Targets in DESI.](/assets/presentations/04_15_21_qnp_research_forum.pdf) DESI Research Forum, Online.
3. **Green, D.** (2022, June 24). [The Future of QuasarNP](/assets/presentations/06_24_22_future_of_qnp.pdf) DESI Collaboration Meeting June 2022, Online