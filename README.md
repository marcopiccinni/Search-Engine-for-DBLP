# Search-Engine-for-DBLP
This is a University project [(UNIMORE)](https://www.unimore.it/) to search in the [DBLP database](https://dblp.uni-trier.de/) for computer science biography.

### REQUIREMENTS
- python3

The following pip packages are needed in order to compile DBLP Searcher : 
- _psutil==5.6.3_
- _Whoosh==2.7.4_

Or it is possible to use the _requirements_ file:
``` 
pip3 install -r requirements.txt 
```

### USAGE
Once the requirements are installed, run the _main.py_ file: 
``` 
./main.py
```
If there isn't the index directory, the program asks you to create indexes giving it the dblp file path.
It is possile to download the required compressed file using [this link](https://dblp.uni-trier.de/xml/dblp.xml.gz), after unpacking it and use this file path.
Otherwise it is possible to use these indexes generated with the dblp dump (2019-11-06): [Mega](https://mega.nz/#!8IwCDQSa!PzntlBqB10LuACPAPVHRD1-bICRazJZU5ko0GNZ1kKU)

##### SEARCH MODE LANGUAGE
	The following mini language is supported by the query resolver:
	
	f-t-s: ([element-field:] search-pattern)+
	search-pattern: term | "phrasal terms"
	element-field: publication-search | venue-search
	publication-search : publication-element[.publication-field]
	publication-element: publication | article | incollection | inproceedings | phThesis | masterThesis
	publication-field: author | title | year
	venue-search: venue[.venue-field]
	venue-field: title | publisher

	e.g.
	1. information retrieval
	2. "information retrieval"
	3. article: data science
	4. incollection.title: "database logic"
	5. article: science venue.title: springer
	
	note:
	"publication" element is used to search in all publication documents type.

##### OPTIONS
  Some options can be modified to change the behaviours of the search and rank modules.
  It is possible to change the _ranking model_ (bm25f or frequency), the _maximal number of documents_ retrieved and _showed attributes_.
  Moreover there is the fuzzy option: it allows the research of similar terms, but this could generate more false positives.
  
  
###### Notes
The program was tested on:
  * **Ubuntu 18.04** with **Pycharm 2019.2.3 Professional Edition** using **Python 3.7.3**
  * **Windows 10 Home (1903)** whit **Pycharm 2019.2.3 Professional Edition** using **Python 3.7.5**
