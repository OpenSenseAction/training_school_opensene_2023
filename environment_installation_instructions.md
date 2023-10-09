## **Installation instructions**

These are the installation instructions for the Python environment that we use during the “OPENSENSE training school on software and methods for data processing from opportunistic rainfall 
sensors” in Tel Aviv, 2023.

In this instruction, we will use the scientific Python distribution “conda” (https://docs.conda.io/en/latest/) with fully open-source packages from https://conda-forge.org/. With these instructions, you will set up all required Python packages. Note that you will not be able  to actively follow the workshop if you do not successfully set up your Python environment according to our instructions. <ins>If you are familiar with conda environments etc.</ins>, just clone this repository, install the provided environment, and make sure that jupyter lab or notebook is running.

The instructions are designed for users of MS Windows, Linux, or MacOS separately. Note that commands that you have to execute on the command line are given in italic font here.

**MS Windows**
1. Download the “mamba-forge” installer (approx. 100 MB), which provides a small initial Python installation
https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Windows-x86_64.exe
2. Execute the installer and follow the installation instructions. Do not change any of the default settings!
3. Download or clone this repository. Unzip if you choose to download it. The usage of cloning/git is encouraged!
4. Open the program called “Miniforge Prompt”
5. In the command line of “Miniforge Prompt” navigate to the repository downloaded in (3) to the location of the downloaded file “environment.yml” by using e.g.  *cd C:/User/username/Download/*.
(If you are not yet familiar with the command line, you can have a look at [this tutorial](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/))
6. When you are in the same directory as the downloaded “environment.yml” file, execute the following command on the command line: *mamba env create --file environment.yml*  
Note that it may take several minutes till conda calculates which package versions to download. After some minutes you will be presented with a list of Python packages that have to be downloaded. In case the installation does not start, you might need to select “yes” or press Return to start the download and installation. 
7. Activate the environment via the command *conda activate os_training_school*
8. Start jupyterlab (the programming environment that we will use during the workshop) by executing the following command on the command line:  
*jupyter-lab --no-browser*  
copy one of the last two localhost URLs to your favorite web browser (Chrome is recommended for Jupyterlab, we have not tested with Edge but it should also work).
You should see your coding workspace similar [to this image](https://jupyterlab.readthedocs.io/en/stable/) (just without content yet).

**Linux/MacOS**
1. Download mamba-forge for your OS
[https://github.com/conda-forge/miniforge#download](https://github.com/conda-forge/miniforge#download) 
2. Locate the installer shell script in your terminal and run it. Use the default options. Do not change any of the default settings unless you are an expert for using conda and know how to set up conda and conda environments!
3. Clone or download this repository. Unzip if you choose to download it. The usage of cloning/git is encouraged!
4. skip (because you now have conda available in your terminal, but note that there might be some extra steps for the recent MacOS version which use zsh as the default shell, see https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html )
5. Navigate to the repository downloaded in (3) to the location of the downloaded file “environment.yml” by using e.g.
*cd C:/User/username/Download/*  
(If you are not yet familiar with the command line, you can have a look at [this tutorial](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands/))
7. When you are in the same directory as the downloaded “environment.yml” file, execute the following command on the command line:
*mamba env create -f environment.yml*
Note that it may take several minutes till conda calculates which package versions to download. After some minutes you will be presented with a list of Python packages that have to be downloaded. In case the installation does not start, you might need to select “yes” or press Return to start the download and installation. 
8. Activate the environment via the command *conda activate os_training_school*
9. Start jupyterlab (the programming environment that we will use during the workshop)  
*jupyter-lab --no-browser*  
copy one of the last two localhost URLs to your favorite web browser (Chrome is recommended for Jupyterlab). You should see your coding workspace similar [to this image](https://jupyterlab.readthedocs.io/en/stable/) (just without content yet).

