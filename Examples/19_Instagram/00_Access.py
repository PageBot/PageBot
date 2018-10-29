# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     00_Access.py
#
#     Examples how to use the InstagramView, reading/writing on Instagram
#
#     https://github.com/facebookarchive/python-instagram  
#    

from instagram.client import InstagramAPI

access_token = "8759299402.3e3cf2b.8b2e6d0ccd664e3e8955548993c649c0"
client_secret = "b21318ea3d3a4795a7b2e89080f1b120"

api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)
#for media in recent_media:
#   print(media.caption.text)