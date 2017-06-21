from instabot import BASE_URL, ACCESS_TOKEN
import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.Get a list of people who have liked the recent post of a user"
        print "f.Like the recent post of a user"
        print "g.Get a list of comments on the recent post of a user"
        print "h.Make a comment on the recent post of a user"
        print "i.Delete negative comments from the recent post of a user"
        print "j.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        #elif choice=="f":
           #insta_username = raw_input("Enter the username of the user: ")
           #like_a_post(insta_username)
        #elif choice=="g":
           #insta_username = raw_input("Enter the username of the user: ")
           #get_comment_list(insta_username)
        #elif choice=="h":
           #insta_username = raw_input("Enter the username of the user: ")
           #make_a_comment(insta_username)
        #elif choice=="i":
           #insta_username = raw_input("Enter the username of the user: ")
           #delete_negative_comment(insta_username)
        #elif choice == "j":
            #exit()
        else:
            print "wrong choice"
            exit()

#FUNCTION DECLARATION FOR SELF INFO OF THE USER.

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'Requesting info for:' + request_url
    my_info = requests.get(request_url).json()
    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username: %s' % (my_info['data']['username'])
            print 'No. of followers: %s' % (my_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (my_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (my_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

#FUNCTION DECLARATION TO GET THE USER ID FROM USER NAME

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

#FUNCTION DECLARATION TO GET THE INFO OF THE USER FROM THE USERNAME

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

#FUNCTION FOR FETCHING THE RECENT POST THE SELF USER ITSELF AND DONLOADED IT

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#FUNCTION FOR FETCHING THE MOST RECENT POST OF ANOTHER USER BY USERNAME

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#FUNCTION FOR FETCHING THE POST ID OF THE RECENT POST OF THE USER

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

#FUNCTION FOR FETCHING THE LIST OF PEOPLE HO LIKED THE RECENT POST OF THE USER

def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    likes_info = requests.get(request_url).json()

    if likes_info['meta']['code'] == 200:
        if len(likes_info['data']):
            for x in range(0, len(likes_info['data'])):
                print likes_info['data'][x]['username']
        else:
                print 'No user has liked the post yet!'
    else:
        print 'Status code other than 200 received!'

start_bot()
