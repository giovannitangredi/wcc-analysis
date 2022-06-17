# wcc-analysis

This repository is used to store all the csv file about static and time analysis for [WCC](https://github.com/giovannitangredi/wcc).
For time analysis a sequence of versions of various repo are considered, and the resulting graphs are stored in the img folder in the .png format.
For now the plot create are the average , minimum and maximum values  for the four metrics in wcc: WCC plain , WCC quantized, CRAP and SkunkScore.

All the graphs will be printed in the img directory:
- All graphs about static analysis will be printed in img/Static
- All graphs about time analysis will be printed in img/Time

## Graphs
In Static we found four graphs one for each metric. Each graphs represent the minimum, maximum and average value for the specific metric for both Cyclomatic and Cognitive complexities for each repository used for testing. The bars for each different repository are of different colors.
In Time there are 3 types for each repository:
1.  one image with a graph that show the ration between the total number of files and the number of complex files in the repository analyzed these images have the following name *repo_name*_complex_files.png
2. one image that have a set of four graphs, each graph represent the average variation between different version of the repository analyzed for all the fpur metrics: WCC PLAIN, WCC QUANTIZED, CRAP and SKUNKSCORE. Those images have the following name *repo_name*_avg_.png
3. Last type of image is exactly like the second one but instead of average it show the maximum for each metric. Those images have the following name *repo_name*_max_.png


## Metrics
- WCC Plain: Give each line of the code file a a value equal the complexity of the file , the sum the complexity of all the covered lines and divide the sum by the PLOC (Formula: sum(cov_lines*comp)/PLOC)
- WCC Quantized: For each covered line of the file see if the space is part of has a complexity value greater than 15, if yes the give it a weight of 2 otherwise 1, uncovered line have a weight of 0. The sum all the weights and divide the sum by PLOC of the file.
- CRAP:Created by Alberto Savoia and Bob Evans([link](https://testing.googleblog.com/2011/02/this-code-is-crap.html#:~:text=CRAP%20is%20short%20for%20Change,partner%20in%20crime%20Bob%20Evans.)). Take the total complexity of the file and the coverage in percentage then apply the following formula formula: ``(comp^2)*(1-coverage) +comp``
- SKUNKSCORE: Created by Ernesto Tagwerker ([link](https://www.fastruby.io/blog/code-quality/intruducing-skunk-stink-score-calculator.html)). Take the total complexity of the file , the coverage in percentage, and a COMPLEXITY_FACTOR in this case equal to 25 then apply the following formula formula: ``(comp/COMPLEXITY_FACTOR)*(100-coverage*100)``

## Usage

Run the project with the following command:
For time analysis
```
python3 time-analysis.py
```
For static analysis
```
python3 static-analysis.py
```