### Error messages with Comments
| **Sr. No** | **Error Message**                                                                                                                                                                         | **Comments**                                                                          |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| 1      | There are no MSI/Worlds games till {date}! Please enter again! <br>There are no games till {date}! Please enter again!                                                                | There exist no games in the database for the selected mode, upto the entered date |
| 2      | For Tournament rankings, please enter a valid Tournament ID!!                                                                                                                         | Tournament ID field is not entered                                                |
| 3      | Entered Tournament ID {Trn ID} is not a valid {MSI/Worlds} Tournament. Otherwise, this ID is not available in the mapping data provided, or it does not occur till the date mentioned | Invalid Tournament ID has been entered                                            |
| 4      | For Team rankings, please enter a list of Team IDs                                                                                                                                    | Team list field is not entered                                                    |
| 5      | All entered teams have been discarded, please enter valid Team IDs The entered teams may have no matches till the entered date                                                        | All the Teams IDs entered by the user are Invalid                                 |

### 🛫Preprocessing logs

| **Sr. No** | **Log Message**                                                                                                                                                 | **Comments**                                                                                                             |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1      | Running algorithm on MSI/Worlds teams (or) <br> Running algorithm on this MSI/Worlds tournament (or) <br> Running algorithm on all teams                    | Shows which ranking system is being followed                                                                         |
| 2      | Data filtered by date: {date}...                                                                                                                            | User has filled the date field - we now only consider games upto that date                                           |
| 3      | Tournament ID entered = {Trn ID}...                                                                                                                         | Shows the Tournament ID entered by the user                                                                          |
| 4      | Fetching Tournament name: {Trn Name}                                                                                                                        | Fetches the Tournament Name from the Tournament ID using the database                                               |
| 5      | Considering games till Tournament ID {trn_id} only ...                                                                                                      | Since Tournament rankings are selected, we only consider games played till the time of occurrence of this tournament |
| 6      | Choosing only teams in this Tournament ...                                                                                                                   | Since Tournament rankings are selected, we only consider games played by these teams over time                       |
| 7      | Entered Team {Team Name}, ID {Team ID} is not present in {MSI/Worlds} database, discarding Additionally, the team may have no matches till the entered date | In the Team Rankings mode, the entered Team IDs are invalid                                                          |
| 8      | Calculating rankings for all given teams                                                                                                                    | All teams entered in the list of teams are valid                                                                     |

### 🛫Calculation logs

| **Sr. No** | **Log Message**                                                                                                              |
|--------|--------------------------------------------------------------------------------------------------------------------------|
| 1      | Calculating RS Metric ...                                                                                                |
| 2      | Merging back RS Metric scores with main data                                                                             |
| 3      | Calculating League, Section, and Stage scores...                                                                         |
| 4      | Calculating game stats...                                                                                                |
| 5      | Calculating weighted score..                                                                                             |
| 6      | Performing Exponential Moving Average...                                                                                 |
| 7      | Some teams have their Names, Acronyms and Slugs as None <br> >> because their data is not given in the "teams.json" file |

