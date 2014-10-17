#!/usr/bin/python
__author__ = 'Toby Applegate'
#script to upload advert to amazon S3 and delete the previous one
import boto, uuid, os, shutil, glob, sys, argparse #imports librarys
from boto.s3.key import Key
from boto.s3.connection import S3Connection

s3 = S3Connection('XXXXXXXXXXXXX','YYYYYYYYYYYY')    # establishes a connection to amazon S3

def main():                                                                             # executes the script
    parser = argparse.ArgumentParser()          # Manages command line arguments
    parser.add_argument('-b', '--basepath') # Base file path containing the folders in question
    args = parser.parse_args()

    media = {'ipad': [10, 12], 'iphone': [12, 14], 'android': [13, 15]} #nested dict of platform
    for platform,numbers in media.items():  #loops through the ipad etc and the numbers in the nested dict
        str_con_one = numbers[0]      #this variable is used to get the first number in the picture's string
        str_con_two = numbers[1]      #this variable is used to get the second number in the picture's string
        try: #checks to see if user inputted filepath e.g. python s3_sample.py -b /home/picutres etc
            pic_count = ''.join([args.basepath, platform, '/counter_directory_', platform, '/'])
        except TypeError:
            error(TypeError, "You did not input the file path")
        uploaded = ''.join([args.basepath, platform, '/upload_directory_', platform, '/companyad', platform, '.jpg'])
        src_advert = ''.join([args.basepath, platform, '/advert_directory_', platform, '/'])
        website_links = ''.join([args.basepath, '/html_adverts_html_file/links.txt'])
        html_upload = ''.join([args.basepath,'html_adverts_html_file/company-ad-', platform, '.html'])
        ad_string = ''.join(['company-ad-', platform, '.html'])
        dir_ad_string = ''.join([platform, 'advert'])
        upload_string = ''.join(['companyad', platform, '.jpg'])
        reset_string = ''.join([platform, 'advert01.jpg'])
        try: #checks that theres files in the directorys specified above so that the script can iterate through them
            uploadAdvert(pic_count, uploaded, src_advert, website_links, html_upload, ad_string, dir_ad_string, upload_string, reset_string, str_con_one, str_con_two)
        except IndexError:
            error(IndexError, "out of range, cannot iterate files as nothing in pic_count or uploaded (check the dir in these variables)")

def uploadAdvert(pic_count, uploaded, src_advert, website_links, html_upload, ad_string, dir_ad_string, upload_string, reset_string, str_con_one, str_con_two):
    dynamic_bucket = s3.get_bucket('mobile-adverts') # creates new variable with regards to the bucket in amazon
    static_bucket = s3.get_bucket('mobile-adverts') # creates new variable with regards to the bucket in amazon
    html_bucket = s3.get_bucket('mobile-adverts') # creates new variable with regards to the bucket in amazon
    try: #checks file path exists
        my_local_bucket_list = os.listdir(pic_count) #puts contents of pic_count dir to variable
    except OSError:
        error(OSError, ''.join(['The file path: ', pic_count, ' is incorrect or does not exsist']))
    dynamic_picture = Key(dynamic_bucket) # uses bucket and assigns a new variable to that buckets
    static_picture = Key(static_bucket)  # uses bucket and assigns a new variable to that buckets
    html_file = Key(html_bucket)  # uses bucket and assigns a new variable to that buckets
    static_picture.key = upload_string # this varible doesnt change once its passed to this function, will be companyadipad but will change depending on format
    html_file.key = ad_string # this is the html file which will be uploaded
    y = my_local_bucket_list[0] # y is the first (and only) variable in my_local_bucket which is the contents of pic_coutn dir
    advert_in_amazon = int(y[str_con_one:str_con_two]) # converts last two digits of file name to int to be used as a count
    x = True # used so that for loop below only iterates once and only changes the advert once
    try:
        num_of_adverts = len(os.listdir(src_advert)) # gets the nunmber of files in the advert src dir to be used for comparrison in elif statement
    except OSError:
        error(OSError, ''.join(['Following file could not be found: ', uploaded, ' path could be wrong or file not exist']))
    dirlist = os.listdir(src_advert) # gets the contents of the directory and puts it in a list
    sorted_list = sorted(dirlist) # sorts the list of contents from the directory as 'os.listdir' doesnt provide a sorted list of contents
    for i in sorted_list: # for loop iterates through the adverts in sorted_list
        advert_counter = int(i[str_con_one:str_con_two]) # gets int at the end of advert string and converts to an int
        ad_count = advert_counter - 1 # used to iterate through list of web links in html function below
        if advert_counter > advert_in_amazon and x: # if advert in my pc is newer (bigger) then the advert in amazon
            if advert_counter < 10: # if advert is under number 10 its string form is converted e.g. to '05' for naming conventions
                advert_counter = "0" + str(advert_counter) #makes num e.g. 5 to follow naming convention e.g. '5' -> '05'
            str_version_of_advert = str(advert_counter) # changes advert number to string
            dynamic_picture.key = dir_ad_string + str_version_of_advert + '.jpg' # specifys file to be uploaded
            remove(uploaded) # removes previously uplaoded picture from to_be_uploaded dir
            remove_file_in_count_dir(pic_count, dir_ad_string) # removes previously uploaded picture from count folder
            copy_files(src_advert, dynamic_picture, uploaded, pic_count) # copys pic to upload dir (but changes its name to follow name conventions) and to count dir
            delete_old_upload_new(upload_string, uploaded, static_bucket, static_picture) # deletes old pic in amazon and uplods new one
            html(website_links, html_bucket, ad_string, html_upload, ad_count, upload_string, html_file) # updates html file + uploads it
            x = False # so only goes through if statement once so doesnt keep updating the files in amazon
            print ''.join(['Uploading some data to "mobile-adverts" bucket with key: ', dynamic_picture.key]) # lets user see whats being uploaded
        elif advert_in_amazon == num_of_adverts and x: # if the advert number in amazon matches the newest advert
                dynamic_picture.key = reset_string # advert will be reseted to first one
                remove(uploaded) # removes previously uplaoded picture from to_be_uploaded dir
                remove_file_in_count_dir(pic_count, dir_ad_string) # removes previously uploaded picture from count folder
                copy_files(src_advert, dynamic_picture, uploaded, pic_count) # copys pic to upload dir (but changes its name to follow name conventions) and to count dir
                delete_old_upload_new(upload_string, uploaded, static_bucket, static_picture) # resets pic in amazon to first one
                html(website_links, html_bucket, ad_string, html_upload, ad_count, upload_string, html_file) # updates html file + uploads it
                x = False # so only goes through if statement once so doesnt keep updating the files in amazon
                print ''.join(['Resetting the advert in the "mobile-adverts" bucket with key: ', dynamic_picture.key])

def remove(uploaded):
    try: # checks to see if correct file path
        os.remove(uploaded)
    except OSError:
        error(OSError, ''.join(['Following file could not be found to be deleted: ', uploaded, ' path could be wrong or file not exist']))

def remove_file_in_count_dir(pic_count, dir_ad_string):
    for path in glob.glob(pic_count + dir_ad_string + '*.jpg'):
        if os.path.isfile(path):
            os.remove(path) #removes file in path

def copy_files(src_advert, dynamic_picture, uploaded, pic_count):
    try: # checls to see if credentials are correct e.g. files, file paths etc
        shutil.copy2(src_advert + dynamic_picture.key, uploaded) # copys file to be uploaded to a diff directory
        shutil.copy2(src_advert + dynamic_picture.key, pic_count + dynamic_picture.key) # copys file to be uploaded to a diff directoy to keep count on whats being uploaded
    except IOError:
        error(IOError, "the file to be copied to amazon does not exist")
    except OSError:
        error(OSError, "Can not copy file because file does not exist")

def delete_old_upload_new(upload_string, uploaded, static_bucket, static_picture):
    static_bucket.delete_key(upload_string) # delete current advert in Amazon
    try: # checks to see if right dir
        static_picture.set_contents_from_filename(uploaded) # uploads file from specified directory
        static_picture.set_acl('public-read') #doing this last seems to be important for some reason
    except IOError:
        error(IOError, ''.join[('Can not upload file because it does not exist in', uploaded)])

def html(website_links, html_bucket, ad_string, html_upload, ad_count, upload_string, html_file):
    try: # checks document is there and path to document is correct
        html_links = open(website_links)
    except IOError:
        error(IOError, "file containing corresponding web-links does not exist")
    lines = html_links.readlines() # reads from txt file
    html_bucket.delete_key(ad_string) # deletes HTML file in Amazon
    try:
        file = open(html_upload,'w') # opens local HTML file to wirte to
    except IOError:
        error(IOError, ''.join(['HTML upload file at ', html_upload, ' does not exsist, please check file/file path']))
    message = """<html>
    <body>
    <a href""" + """=\"""" + lines[ad_count] + """"><img src="https://s3.amazonaws.com/mobile-adverts/""" + upload_string + """ \"/></a>
    </body>
    </html>"""
    file.write(message) # writes above message to local HTML file
    file.close() # closes local HTML file
    html_file.set_contents_from_filename(html_upload) # uploads local HTML file to Amazon

def error(error_type, error_message):
    if error_type == IOError:
        print(error_message)
        sys.exit()
    elif error_type == OSError:
        print(error_message)
        sys.exit()
    elif error_type == "OSError_no_exit":
        print(error_message)
        sys.exit()
    elif error_type == IndexError:
        print(error_message)
        sys.exit()
    elif error_type == TypeError:
        print(error_message)
        sys.exit()

main()