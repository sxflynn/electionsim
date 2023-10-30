# Upper Arlington School Board Election Simulator
Upper Arlington city elections for City Council and School Board typically have a list of candidates competing for multiple open seats. In a state or federal elections operating where voters only vote for one candidate to fill a single open seat, predicting elections take the form of polling and examining fundamentals. Predicting local elections where voters can select multiple candidates with multiple winners is more challenging.  

## How to install (beginners using Mac or Windows)
1. Install `python3` from the official Python [website](https://www.python.org/downloads/).
1. [Download](https://github.com/sxflynn/electionsim/archive/refs/heads/main.zip) this repository to your computer as a zip file. Double click the zip file to unzip it as a folder called `electionsim-main`.
1. [Windows only] Open the `electionsim-main.zip` file on your computer and make sure to click "Extract all..." so it gets extracted to a folder called `electionsim-main`.
1. [Mac only] Open the Terminal app on Mac.
1. [Windows only] Open the Windows Powershell on Windows.
1. Type the command `cd` and then drag the `electionsim-main` folder onto the window, then hit Return.
1. Type `python3 election_cli.py` and it should run. If it gives an error about python3 not being installed, or if it says `No such file or directory` then type the command `pwd` and hit Enter to make sure your Terminal or Powershell is looking in the right directory where the `electionsim-main` folder is.
1. To customize the electorate data, candidates and voter profiles, see below on working with the `config.json` file.


## Installation (advanced)
1. Install `python3`
1. Open `config.json` to edit the candidate and electorate profiles.
1. Run `election_cli.py` to view the results in JSON format.


## How to use `config.json` to customize your election simulations
`election.py` reads in a local file `config.json` as its input. 

| Config parameter  | Description |
| - |:--|
| `candidates`    | The full name of all the candidates on the ballot are listed as a string array.     |
| `voterProfiles`    | The default file contains three profiles: `DEM`, `IND`, and `GOP`. You may add more profiles like `CENTER-DEM`, `CENTER-GOP`, etc for more fine tuned control.<br />The decimal number following each candidate must be between `0` and `1`, although a value inclusive of the range `0.05` and `0.95` is recommended to generate entropy in the simulation.<br/>The decimal number indicates the probability of individual voter selecting this candidate on their ballot. **See below for a more detailed discussion of `voterProfiles`.**|
| `electorate`      | Each `voterProfile` has a corresponding number indicating its percentage of the whole electorate. For example, `"GOP":0.39` means that 39% of the electorate has the `GOP` voter profile. All the `electorate` values must add up to `1.0`.     |
|`electionSettings`|`numOfSims`: The number of times the script will run a single election. Higher numbers will increase processing times.</br> `totalVoters`: The number of voters for each election sim. Higher numbers will increase processing times and also reduce entropy in the final results.</br> `ballotWinners:` By default, the Upper Arlington School Board election will have `2` winners since there are two open seats. You may customize this value for other elections with more than 2 winners. Set the value to `1` to emulate a traditional single-winner election. |
|`message`|Unused config parameter that may be used in future versions to add messages contextualizing the election or justifying the `voterProfiles`.


### `voterProfiles` in depth:
The aim of this program is to allow you to create custom voter profiles which represent the probability that a voter of that profile would add that candidate to their ballot. Let's walk through an example using the default values from the repository:

*  `"DEM":{"Jenny McKenna":0.60` This says that given a single instance of a voter with the `DEM` profile, there is a 60% probability that they will add Jenny McKenna to their ballot. *What it does not represent is 60% of all `DEM` voters will cast a vote for Jenny McKenna.* There is a distinction.
 
*  `"IND":{"Jenny McKenna":0.90` This says that given a single instance of a voter with the `IND` profile, there is a 90% probability that they will add Jenny McKenna to their ballot.

#### If a voter can only choose 2 candidates, but has a 90%+ probability of choosing 3, what happens?
The program has a simple tie-breaking feature to ensure every voter only selects the number of candidates declared in the `ballotWinners` variable. Assuming you set that value to `2`, if a voter ends up selecting 3 candidates, two winners will be chosen from random. Over hundreds of voters and hundreds of election sims, this introduces a small amount of entropy into the results.

#### Where do voter profile numbers come from?
In a typical local election, there are no polls to draw from to guess electoral outcomes. That means that you have to use your own knowledge and intuition to assign these numbers. Given that school board elections have become polarized, you can make an educated guess on how likely a `DEM` or `GOP` voter would select a specific candidate.


### Reading the results:
The program will output a `JSON`-formatted string with `candidatename`, `numberOfWins`, and `probabilityToWin`. 

This is an example of one possible outcome based on a custom set of voter profiles. In this case, `300` elections were run, and the probability of a candidate winning is simple `numberOfWins` divided by the total number of elections. For example, `247/500 = 0.823` which is 82.3% probability.

```
 "candidates": {
        "Glen Dugger": {
            "numberOfWins": 247,
            "probabilityToWin": "82.3%"
        },
        "Liz Stump": {
            "numberOfWins": 183,
            "probabilityToWin": "61.0%"
        },
        "Sumia Mohamed": {
            "numberOfWins": 168,
            "probabilityToWin": "56.0%"
        },
        "Ruth Edmonds": {
            "numberOfWins": 2,
            "probabilityToWin": "0.7%"
        },
        "Jenny McKenna": {
            "numberOfWins": 0,
            "probabilityToWin": "0.0%"
        },
        "Lori Trent": {
            "numberOfWins": 0,
            "probabilityToWin": "0.0%"
        }
```
