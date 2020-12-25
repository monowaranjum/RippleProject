# RippleProject: COMP 7570
![image](https://github.com/monowar-1994/RippleProject/blob/master/Gephi_Network_Graph.png)

This repository contains the files used for the course project of COMP 7570 in Fall 2020 in University of Manitoba. 

# To run this project, follow the following steps:

1. First: run the dbhelper.py ( This will create the database schema and tables for you )
2. Second: run the data_collector.py . Set the variables in the query generation function to your wish. If you want to reduce or increase the wait between requests then just change the variable of waiting time in the code.
3. Run the analyzer.py to run some initial analysis to see if the graph works. 

If you want direct access to the SQLite database for the scraped data, please follow this link: https://drive.google.com/file/d/1siUUxuu629WVcOYDoqOemMVAzQD6VVCJ/view?usp=sharing. Unfortunately Github free version does not allow more than 100 MB file storage. That is why the data is being shared in the drive. 

If you want direct access to the CSV files for the scraped data, please follow this link: https://drive.google.com/drive/folders/1Nh6bUftqQlzMglz-4DzdvitXOGqacJo7?usp=sharing
This file contains all the necessary csv files to run the notebooks. 

To understand how these CSV files were created please refer to the SQL script in the repository. 

If you do have any question regarding this repository, please mail us: anjumm1@myumanitoba.ca or chowdh26@myumanitoba.ca
