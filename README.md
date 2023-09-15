This script converts the Blue Shield prefix file to a format that can be imported into Epic.

Example Blue Shield file format:

Prefix|Occurrence in File|Destination (C=BC,T=BS)|Not used|Start Date|End Date

A1A|01|C| |20190101|99999999|

Assumptions:
This import assumes that the prefixes will override the data in the first contact and that the contact date is 1/1/1900.

How to install:
1) Download this repository to your computer. This can be done by cloning the repository from the Github Desktop application or you can enter the following from a Github command line:

git clone https://github.com/Brian-Krumholz/BlueCard_Import

2) Install the dependencies for the project. This can be done from python console with the following command:
pip install -r requirements.txt

How to use:
1) Either execute the buildImport.py file from the IDE or type the following command into the command prompt:
python buildImport.py

    *It is important to note that if you are running the program from the command prompt you should be in the project directory
2) The first time it runs, a config.ini will be created. You should open up the config.ini file and update the settings as needed.
3) Run the program a second time, it will now prompt for the import file. You only need to specify the filename and not the full path.
4) The program will run and create an Epic import file in the output directory specified in config.ini.
5) Transfer the import file to the Epic server.
6) Open up chronicles for the CMP ini.
7) Import the file using the CMP,1001 import specification
8) Open up the CMP in record viewer or data courier and verify that it has the correct number of prefixes in it.
