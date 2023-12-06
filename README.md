# SI507_final_project
This is the final project of course SI 507, University of Michigan.

# Aim of this project 
Search specific restaurants and filter out certain types of restaurants in Ann Arbor, Michigan.

# How to interact with this program.
1. Run Yelp.py to get the json file ann_arbor_restaurants.json. (You may need to get a new Yelp API key by yourself and replce my key with it on the Yelp Developers website)
2. Run app.py to start the local user and get a web page, then you can perform the actions of search and filter.
3. You can either search the name of restaurants directly, filter out certain types of restaurants as you like, or do both at the same time.
4. If you want to reset all the values, you don't need to refesh the page. Instead, just click the "Reset" button.
5. If you want to see the details of certain restauran in the result list, you can just click its name, and it will redirect you to the corresponding page on the Yelp website.
6. If you want to see the details of certain restauran on the map, you can just click the position mark and then its name, and it will redirect you to the corresponding page on the Yelp website.

Ps1: plot_graph.py is used to generate an overview of price, ranges, ratings and categories of all restaurants in Ann Arbor.
Ps2: all_xxx.py is used to see all kinds of categories, transactions, review counts of all restaurants in Ann Arbor and save the result in xxx.txt file. Then I can use the results to design the filter forms in web page. You don't need to run them to perform action of search and filter.
Ps3: The result list may be very long, so I split it by pages, with each page containing ten items. You can go to different pages by clicking the page numbers, or just type in a page number and click "Go" button.

An example output will be like this:
![example1](output/1.png)
![example2](output/2.png)
![example3](output/3.png)
![example4](output/4.png)
![example5](output/5.png)
