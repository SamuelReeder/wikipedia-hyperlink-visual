# CSC111-Project
CSC111 project at U of T. It is a visualization of wikipedia articles using hyperlinks. https://en.wikipedia.org/wiki/Special:WhatLinksHere might be helpful. 

Run within main file:
```
main(<article_title:str>, <depth_of_recursion:int>, <colour_by_connectivity:bool>, <category_filters:set[str]>)
```
`article_title` is the name of the article which will be the root of the graph. `depth_of_recursion` is the maximum depth of recursion in creating this graph. `category_filters` specifies categories which an article must belong to in order to be included in the graph even if it is connected through hyperlinks. An article only has to belong to any one of the specified categories to be included. Each category string must be formatted as `Category:<category_name>` These arguments are case-sensitive.
