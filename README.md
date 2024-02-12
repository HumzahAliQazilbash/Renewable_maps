# Renewable Maps

This repo is deigned to show where particular projects occur and show all other renewable projects in the Verra registry in the same country as the project of interest.

This gives insight into the additionality of renewable projects, showing how many similar projects occur within the same country.  All data is from Berkley's dataset of Verra projects.  There are 2682 projects in this registry and this repo allows the user to create maps for each one.

### Preview
![image](https://github.com/HumzahAliQazilbash/Renewable_maps/assets/152615068/dcebe9b6-ee98-494e-b523-172a663d5a9f)

### Installation

&nbsp;1) Install conda

&nbsp;2) Clone the repo onto your local using `git clone`

&nbsp;3) Install the environment : `conda env create -f environment.yml`

&nbsp;4) Activate the conda environment from the root of the repo: `conda activate renewable_maps` and then `$python create_RES_maps.py` 

&nbsp;5) You will be prompted to enter the project id (eg. `237753`)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If the project id is incorrect then you will be prompted again.

&nbsp;6) The resulting map will be saved in the outputs folder
