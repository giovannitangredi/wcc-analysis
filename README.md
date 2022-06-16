# wcc-analysis

This repository is used to store all the csv file avout static and time analysis for [WCC](https://github.com/giovannitangredi/wcc).
For time analysis a sequence of versions of various repo are considered, and the resulting graphs are stored in the img folder in the .png format.
For now the plot create are the avarage , minimum and maximum values  for the four metrics in wcc: Sifis plain , Sifis quantized, CRAP and SkunkScore.

All the graphs will be printed in the img directory:
- All graphs abount static analysis will be printed in img/Static
- All graphs abount time analysis will be printed in img/Time

In Static  you will found a graph for each metric, in each graph a bar diagram is showed with all the minimum , maximum and average values for that metric for each project analyzed
In Time there will be graphs for each project analyzed , each project will have a multiple images: one that show the number of complex files and total files present in the project in each version and then two images that have 4 graphs in it the rapresent the variation of minimum and avarage between different version of the project for all four differet metrics analyzed.

## Usage

Run the project with the following command:
```
python3 time-analysis.py
```