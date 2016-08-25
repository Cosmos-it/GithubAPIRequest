import json
import requests
import csv

# Create an OpenerDirector with support for Basic HTTP Authentication...
#https://api.github.com/orgs/daptiv/repos gets all the repos details
#Example info needed for this program to work. 
# Token = "ef8f22920253fb57ec5f2730292907ad7f00443a"
# response = requests.get(url, headers={"Authorization": "Bearer %s" %Token})
# DaptivPpmPRComments = 'https://api.github.com/repos/daptiv/Ppm/4136/comments'
# DaptivPullsLinks = 'https://api.github.com/repos/daptiv/Ppm/pulls'
# DaptivPpmPrclosed = 'https://api.github.com/repos/daptiv/Ppm/pulls?state=closed&page=1&per_page=100'
# DaptivPpmPrLink = 'https://api.github.com/repos/daptiv/Ppm/pulls?state=open&page=1&per_page=100'
# comments = 'https://api.github.com/repos/daptiv/Ppm/comments/0f0a48e6995b4e0e28cee36aca5c523be1f8d710'
# comment_user = 'https://api.github.com/repos/daptiv/Ppm/comments/{0}'

#Authorization Token and url passed to this method to return data
def Authorization(Token, url):
    response = requests.get(url, headers={"Authorization": "Bearer %s" %Token})
    return response

#Fetch PR links
def GetPullRequestsLinks(reponse):
    cleanedLink = ''
    if 'link' in reponse.headers:
        links = str(reponse.headers['link'])
        char = 'next'
        for char in links:
            cleanedLink = links.replace('<', '').replace('>', '').replace('<', '').replace('rel=', '').split(';')
    print cleanedLink

# Fetch and Save Links JsonFormat (review_comments_links.json)
def GetPRDetailsLinks(json_data):
    links = []
    for link in json_data.json():
        JsonFormat = {}
        JsonFormat['links'] = link[u'url']
        if JsonFormat:
            links.append(JsonFormat)
        with open('data/review_comments_links.json', 'wb') as file:
            json.dump(links, file)           

'''
Load all URL link from (review_comments_links.json)
Then pass the URL to authorization to fetch the data
Then save the data into some form of database. 
Create a JSON data format. Then decide how you want to save.
'''
def GetAllPrData():
    fileName = raw_input("To save current data, provide name with .json extension:.. ")
    data = json.loads(open('data/review_comments_links.json').read())
    toJsonFormat = {}
    jsonDataObject = []
    comments = {}
    for keys in data:
        response = ''
        values = keys[u'links']
        if values:
            toJsonFormat['link'] = values
            response = Authorization(Token, str(values + '/comments'))
            for resp in response.json():
                toJsonFormat['user'] = resp[u'user'][u'login']
                toJsonFormat['created_at'] =resp[u'created_at']
                toJsonFormat['updated_at'] = resp[u'updated_at']
                toJsonFormat['comments'] = resp[u'body']                   
                jsonDataObject.append(toJsonFormat);
                print "------------ Start ----------------"
                print json.dumps(jsonDataObject, indent=1)
                print "------------ End ----------------"
                print "\n"  
    with open('data/'+fileName, 'wb') as file:
        json.dump(jsonDataObject, file)
    print "File save to directory data/"+filename      

'''
Next thing to do.
Nest all comments for specifc users and their dates undet one PR url

'''

print "Program ready: "
print "1. If you wish to load new data,"
print "2. Use Authorization(Token, url)"
print "3. Then pass Authorization response to"
print "   GetPRDetailsLinks "
print "5. Finally call GetAllPrData."
print "\n"
