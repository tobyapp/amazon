amazon
======

Hey welcome to my first project! I wrote this basic script as a work project to rotate an image file and an html file in a bucket in Amazon S3.Tthe reason for this is that out company app each week grabs the html and image file located in this bucket and uses those files to display an advert that when clicked, redirects a user to a particular web address. The process for this was performed manually by uploading an advert and deleting the previous one and editing an HTML file (this was done for each format) but this became very repetitive so a new solution had to be found (and this is where I came in!).


file_rotation.py setup
To get this script to work four directories need to be created for the script to use (how the script uses these directories is in the section below), there would be a directory for each format (for example iPhone, iPad and Android) and in each of these three parent directories a further three child directories are created, one with a list of adverts, one for the chosen advert to be uploaded to Amazon and one to be used as a counter to keep track of what is being uploaded. Along side these three parent directories, another one needs to be created which will hold the HTML file information. Once all this is created the folders needs to be populated, ill use the iPad format for the following example (it is the same process for the other formats): 


1. For the iPad format the first directory that needs to be populated is the advert directory which will hold all the adverts that want to be shown over time with the following naming format: format + advert + number +.jpg (e.g. ipadadvert03.jpg) 
2. Once this directory is populated the first advert to be uploaded needs to be copy and pasted into the counter directory with the same name as the original (e.g. if ipadadvert03.jpg was going to be the first advert to be uploaded then this is copy and pasted into the counter directory)
3. Once this is done the same advert needs to be copy and pasted into the upload directory, but this time the name of the file should be changed to match the following naming format: companyad + format + .jpg (e.g. companyadipad.jpg), this is the naming convention that the apps use when looking for an advert to display
4. The next step is to jump to the HTML directory and create a file called 'links.txt' file (this file is used by all of the HTML adverts) and this file should be a list of web address that each advert should direct a customer to when that advert is clicked (the list must be separated by placing each element on a new line)
5. Steps 1-3 need to be done for each format but step 4 only needs to be done once


To clarify the text above each format needs three directories:
1. advert directory
2. counter directory
3. upload directory

And one directory to be used by all the formats titled HTML for the HTML files.


How file_rotation.py works
Once the setup has been created the script is ready to run, for this explanation I will again use the iPad format but it is the same for all formats:

1. When the script starts it will first look at what's in the counter directory and will convert the file name to an integer (e.g. ipadadvert03.jpg will become 03) to be used as a counter

2. The counter will then be compared to the adverts in the advert directory beginning with the first advert (01)

3. The counter will be compared to every advert in ascending order until a larger one is found

4. (a) Once a larger one is found (e.g. 04) it will replace the file in the counter directory (so ipadadvert03.jpg will become ipadadvert04.jpg) as well as replacing the file in the upload directory

4. (b) If no larger file is found then the counter is reset to 01 (so ipadadvert03.jpg will become ipadadvert01.jpg) as well as replacing the file in the upload directory 

5. The file in the upload directory is then renamed companyadipad.jpg to follow naming conventions in Amazon

6. The advert in Amazon is then deleted and the new file in the upload directory is then uploaded

7.An HTML file is then created referencing the advert in Amazon and a weblink corresponding to the counter (so if the counter == 1 the web link will be bbc.co.uk, if counter ==4 the web link will be msn.com for example) and this then replaces the current HTML file in Amazon

8. This process is then repeated for all three formats.
