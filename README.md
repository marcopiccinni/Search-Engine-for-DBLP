# Search-Engine-for-DBLP
This is an University project [(UNIMORE)](https://www.unimore.it/) to search in the [DBLP database](https://dblp.uni-trier.de/) for computer science biography.

#### REQUIREMENTS
The following pip packages are needed in order to compile DBLP Searcher : 
- _psutil==5.6.3_
- _Whoosh==2.7.4_

Or it is possible to use the _requirements_ file:
``` 
pip install -r requirements.txt 
```

#### USAGE
Once the requirements are installed, run the _main.py_ file: 
``` 
python3 main.py
```
If there isn't the index directory, the program ask you to create indexes giving it the dblp file path.
It is possile to download the required compressed file using [this link](https://dblp.uni-trier.de/xml/dblp.xml.gz), and after unpack it.
Otherwise it is possible to use these indexes generated with the dblp dump (2019-11-06): [Mega](https://mega.nz/#!Nd4BWYpD!7Az-4w0w6mx_81e2uschCdUWFb8QQJYIhJqiS1i8ZyM)


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

##### OPTIONS
  Some options can be modified to change the behaviours of the search and rank modules.
  It is possible to change the _ranking model_ (vector or frequency), the _maximal number of documents_ retrieved and _showed attributes_.
  Moreover there is the fuzzy option: it allows the search for similar terms, but this could be generate more false positive.
  
###### Notes
The program was tested on **Ubuntu 18.04** with **Pycharm 2019.2.3 Professional Edition** using **Python 3.7**
