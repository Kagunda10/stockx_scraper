# -*- coding: utf-8 -*-
# from gevent import monkey
# monkey.patch_all()
import grequests
import requests
import urllib.request as ur
from bs4 import BeautifulSoup
import random 
import json
from datetime import datetime
import os
import time
from lxml import html
import smtplib
import re
from time import time as timer
import tweepy

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# from notifs_glbal import *
from slacker import Slacker
 

 
def LoadUserAgents(uafile="user_agents.txt"):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                #testshit = str(ua.strip()[1:-1-1])
                testshit = (ua.strip()[1:-1-1])
                #print(testshit)
                #print(ua)
                #print(testshit.decode())
                #print(testshit.decode("utf-8"))
                uas.append(testshit.decode())
                #uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    ua = random.choice(uas)
    return ua

def LoadLumProx(proxfile="lumproxies.txt"):
    proxylist = []
    with open(proxfile) as f:
        for line in f:
            if line:
                line.replace('\n', '')
                try:
                    sep = ':22225:'
                    sep2 = ':lum'
                    namepass = line.split(sep, 1)[1]
                    proxyport = line.split(sep2, 1)[0]
                except:
                    pass#rest = str(sizes)
                testingsomegoodshit = {'https': 'https://' + namepass.replace('\n', '') +'@' + proxyport.replace('\n', '') +'/' , 'http': 'http://' + namepass.replace('\n', '') +'@' + proxyport.replace('\n', '') +'/' }
                #print(testingsomegoodshit)
                proxylist.append(testingsomegoodshit)
    random.shuffle(proxylist)
    thisrandomprox = random.choice(proxylist)
    return thisrandomprox
    #return proxylist
# takes two arguements(SKU, SIze) 
def stockx_main(product_sku, userrrrrsize=None):
    # product_sku = input("SKU or Product: ")
    # userrrrrsize = input("Enter Size or leave blank: ")
    headers = {
        'Host': 'gateway.stockx.com',
        #'jwt-authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdG9ja3guY29tIiwic3ViIjoic3RvY2t4LmNvbSIsImF1ZCI6IndlYiIsImFwcF9uYW1lIjoiYW5kcm9pZCIsImFwcF92ZXJzaW9uIjoiMy44LjciLCJpc3N1ZWRfYXQiOiIyMDE5LTAxLTI2IDE5OjM4OjM5IiwiY3VzdG9tZXJfaWQiOm51bGwsImVtYWlsIjpudWxsLCJjdXN0b21lcl91dWlkIjpudWxsLCJmaXJzdE5hbWUiOm51bGwsImxhc3ROYW1lIjpudWxsLCJnZHByX3N0YXR1cyI6bnVsbCwiZGVmYXVsdF9jdXJyZW5jeSI6IlVTRCIsInNoaXBfYnlfZGF0ZSI6bnVsbCwidmFjYXRpb25fZGF0ZSI6bnVsbCwicHJvZHVjdF9jYXRlZ29yeSI6InNuZWFrZXJzIiwiaXNfYWRtaW4iOm51bGwsInNlc3Npb25faWQiOiIxMjk4NDEyNDg1MjExNjQ0NDAxOCIsImV4cCI6MTU0OTEzNjMxOSwiYXBpX2tleXMiOm51bGx9.YOmTg1cXIZ4miW56rDExwFNXtL-nw9rtmel7zQOZhqw',
        'x-api-key': 'zWW9iZmfu02CDfd9bCWnZ29mKLgHC9AJ5kjUHvVq',
        'app-platform': 'android',
        'app-version': '3.8.7',
        #'x-anonymous-id': '6ef3a949-55e0-450d-aeeb-35ceaa17b134',
        'user-agent': 'okhttp/3.11.0',
    }

    params = (
        ('page', '0'),
        ('query', str(product_sku)),
        #('query', 'jordan 1 retro high'),
        ('filters', ''),
    )
    skuuuuuuname = ''
    shoeeeename = ''
    reallllurl = ''
    newapilink = ''
    try:
        response = requests.get('https://gateway.stockx.com/api/v2/search', 
                                headers=headers,
                                proxies=LoadLumProx(), 
                                params=params, 
                                timeout=7)
        jsonshit = json.loads(response.text)
    except:
        response = ''
        jsonshit = ''
    try:
        #print(jsonshit.keys())
        shoeeeename = jsonshit['hits'][0]['name']
        print(jsonshit['hits'][0]['name'])
        skuuuuuuname = jsonshit['hits'][0]['style_id']
        print(jsonshit['hits'][0]['style_id'])
        #print(jsonshit['hits'][0])
        reallllurl = jsonshit['hits'][0]['url']
        #print(jsonshit['hits'][0]['url'])
        newapilink = 'https://stockx.com/api/products/' + str(jsonshit['hits'][0]['url'])
        print(newapilink)
    except:
        skuuuuuuname = ''
        shoeeeename = ''
        reallllurl = ''
        newapilink = ''

     

     

    numoflinks = 1
     
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': LoadUserAgents(),
    }
    newsession = requests.Session()
    newsession.verify = False
    newsession.cookies.clear()
    #proxies2 = LoadRandomProx()
    #proxies22222 = random.choice(proxies2)
    if newapilink:
        try:
            productpagelink = newsession.get(newapilink + '?includes=market,360&children=&currency=USD', proxies=LoadLumProx(), headers=headers, timeout=7)
            pagedata = BeautifulSoup(productpagelink.content, 'html.parser')
            #print(tessstss)
        except Exception as wthappend:
            pass#print(wthappend)
        #for madeupshit in tessstss:
        try:
            #pagedata = BeautifulSoup(madeupshit.content, 'html.parser')
            #print(madeupshit.text)
            json_dict = json.loads(productpagelink.text)
            #print(json_dict)
            #print('-------')
            #print(json_dict.keys()
            #for someothershit in json_dict['Product']['market'].items()
        except:
            #pagedata = 'N?A?pagedataERROR'
            json_dict = 'N?A?pagedataERROR'
            #print(pagedata)
        #print(json_dict['Product']['title'])
        #print(json_dict['Product'])
        #print(json_dict['Product']['releaseDate'])
        try:
            releasedate = json_dict['Product']['releaseDate']
        except:
            releasedate = 'n/a'
        try:
            total_sold = json_dict['Product']['market']['deadstockSold']
        except:
            total_sold = 'n/a'
        try:
            last72_sold = json_dict['Product']['market']['salesLast72Hours']
        except:
            last72_sold = 'n/a'
        try:
            last_size = json_dict['Product']['market']['lastSaleSize']
            last_size = last_size.replace('.5', '½')
        except:
            last_size = 'n/a'
        try:
            last_sale = json_dict['Product']['market']['lastSale']
        except:
            last_sale = 'n/a'
        lastsoldsize = sizzeeess = '*Size :: ' + str(last_size) + '* | $' + str(last_sale)
        try:
            highest_size = json_dict['Product']['market']['highestBidSize']
            highest_size = highest_size.replace('.5', '½')
        except:
            highest_size = 'n/a'
        try:
            highest_bid = json_dict['Product']['market']['highestBid']
        except:
            highest_bid = 'n/a'
        highest_offer = sizzeeess = '*Size :: ' + str(highest_size) + '* | $' + str(highest_bid)

        newstocklist = []
        sizelist = []
        stocklist = []
        justthesizelist = []
        newtotal = 0
        try:
            for key,value in json_dict['Product']['children'].items():
            #for someothershit in json_dict['Product']['children'].items():
            #for someothershit in json_dict['Product']['children']:
                #print(key,value)
                #print(key)
                #print('-------')
                try:
                    #print(key['shoeSize'])
                    #print(value['shoeSize'])
                    shoe_size = value['shoeSize']
                    #shoe_size = shoe_size.replace('.5', '½')
                except:
                    shoe_size = 'N/a'
                if userrrrrsize:#if shoe_size == 8:
                    if str(shoe_size) == str(userrrrrsize):
                    #if str(shoe_size) == '8':
                        shoe_size = shoe_size.replace('.5', '½')#print(value['market'])
                        try:
                            total_sold = value['market']['deadstockSold']
                        except:
                            total_sold = 'n/a'
                        try:
                            last72_sold = value['market']['salesLast72Hours']
                        except:
                            last72_sold = 'n/a'
                        try:
                            last_size = value['market']['lastSaleSize']
                            last_size = last_size.replace('.5', '½')
                        except:
                            last_size = 'n/a'
                        try:
                            last_sale = value['market']['lastSale']
                        except:
                            last_sale = 'n/a'
                        lastsoldsize = sizzeeess = '*Size :: ' + str(last_size) + '* | $' + str(last_sale)
                        try:
                            highest_size = value['market']['highestBidSize']
                            highest_size = highest_size.replace('.5', '½')
                        except:
                            highest_size = 'n/a'
                        try:
                            highest_bid = value['market']['highestBid']
                        except:
                            highest_bid = 'n/a'
                        highest_offer = sizzeeess = '*Size :: ' + str(highest_size) + '* | $' + str(highest_bid)

                    #    print(value[0]['market'])
                        #print(value)
                        #print('yes')
                        #print(value['market'])
                        #print(key)
                        #print(key)
                        sizzeeess = '*Size* :: ' + str(shoe_size)
                        #if shoe_size == 8:
                        #    print(value[0]['market'])
                            #print(value['market'])
                            #print(key)
                        try:
                            shoe_deadstockSold = value['market']['deadstockSold']
                            shoe_deadstockSold2 = value['market']['deadstockSold']
                        except:
                            shoe_deadstockSold2 = '0'
                            shoe_deadstockSold = '    0'
                            #shoe_deadstockSold = 'N/a'
                        newtotal += int(shoe_deadstockSold2)
                        try:
                            shoe_lastSale = value['market']['lastSale']
                            """#shoe_lastSale = '$' + str(shoe_lastSale)
                            if len(str(shoe_lastSale)) == 4:
                                pass
                            if len(str(shoe_lastSale)) == 3:
                                shoe_lastSale = ' ' + str(shoe_lastSale)
                            if len(str(shoe_lastSale)) == 2:
                                shoe_lastSale = '  ' + str(shoe_lastSale)
                            if len(str(shoe_lastSale)) < 2:
                                shoe_lastSale = '   ' + str(shoe_lastSale)
                            """
                            shoe_lastSale = '$' + str(shoe_lastSale)# + '  '
                            #print(shoe_lastSale)
                        except:
                            shoe_lastSale = 'N/a'
                            
                        try:
                            shoe_saless = str(shoe_deadstockSold) + ' | ' + str(shoe_lastSale)
                            shoe_saless = ('{:11s}::{:5s} | {:5s}'.format(str(sizzeeess),str(shoe_deadstockSold), str(shoe_lastSale)))
                        except:
                            shoe_saless = ''
                        try:
                            #sizee_totals = str(shoe_deadstockSold) + ' | ' + str(sizzeeess)
                            #sizee_totals = ('{:8s} | {}'.format(str(shoe_deadstockSold),str(sizzeeess)))
                            #sizee_totals = ('{} | {}'.format(str(shoe_deadstockSold),str(sizzeeess)))
                            sizee_totals = ('{}| {}'.format(str(sizzeeess),str(shoe_deadstockSold)))
                        except:
                            sizee_totals = ''
                            
                        try:
                            shoe_highestBid = value['market']['highestBid']
                            #shoe_highestBid = '$' + str(shoe_highestBid)
                            """#print(len(shoe_highestBid))
                            if len(str(shoe_highestBid)) == 4:
                                pass
                            if len(str(shoe_highestBid)) == 3:
                                shoe_highestBid = ' ' + str(shoe_highestBid)
                            if len(str(shoe_highestBid)) == 2:
                                shoe_highestBid = '  ' + str(shoe_highestBid)
                            if len(str(shoe_highestBid)) < 2:
                                shoe_highestBid = '   ' + str(shoe_highestBid)
                            #if len(shoe_highestBid) == 1:
                            #    shoe_highestBid = ' 000' + str(shoe_highestBid)
                            """
                            shoe_highestBid = '$' + str(shoe_highestBid)# + '  '
                            #print(shoe_highestBid)
                        except:
                            shoe_highestBid = 'N/a'
                        try:
                            shoe_lowestAsk = value['market']['lowestAsk']
                            """#shoe_lowestAsk = '$' + str(shoe_lowestAsk)
                            if len(str(shoe_lowestAsk)) == 4:
                                pass
                            if len(str(shoe_lowestAsk)) == 3:
                                shoe_lowestAsk = ' ' + str(shoe_lowestAsk)
                            if len(str(shoe_lowestAsk)) == 2:
                                shoe_lowestAsk = '  ' + str(shoe_lowestAsk)
                            if len(str(shoe_lowestAsk)) < 2:
                                shoe_lowestAsk = '   ' + str(shoe_lowestAsk)
                            """
                            shoe_lowestAsk = '$' + str(shoe_lowestAsk)# + '  '
                            #print(shoe_lowestAsk)
                        except:
                            shoe_lowestAsk = 'N/a'

                        try:
                            #shoe_offerrrss = str(shoe_lastSale)  + ' | ' + str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                            #shoe_offerrrss = str(shoe_deadstockSold) + ' | ' + str(shoe_lastSale)  + ' | ' + str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                            #shoe_offerrrss = str(shoe_size) + 'str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                            #shoe_offerrrss = ('{:5s} | {:5s} | {:5s}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk)))
                            #shoe_offerrrss = ('{}|{}|{}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk),str(shoe_deadstockSold)))
                            shoe_offerrrss = ('{}|{}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk)))
                            #shoe_offerrrss = ('{:5s}|{:5s}|{:5s}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk),str(shoe_deadstockSold),))
                        except:
                            shoe_offerrrss = ''
                        #if shoe_size == 8:
                        #    print(value[0]['market'])
                            #print(value['market'])
                            #print(key)
                        shoe_size = shoe_size.replace('.5', '½')

                        sizeandqty = ('{:30s} {:30s}'.format(str(sizee_totals), str(shoe_offerrrss)))
                        justthesizelist.append(sizeandqty)
                        newstocklist.append(sizeandqty)
                        sizelist.append(sizee_totals)
                        stocklist.append(shoe_offerrrss)
                else:
                    sizzeeess = '*Size* :: ' + str(shoe_size)
                    #if shoe_size == 8:
                    #    print(value[0]['market'])
                        #print(value['market'])
                        #print(key)
                    try:
                        shoe_deadstockSold = value['market']['deadstockSold']
                        shoe_deadstockSold2 = value['market']['deadstockSold']
                    except:
                        shoe_deadstockSold2 = '0'
                        shoe_deadstockSold = '    0'
                        #shoe_deadstockSold = 'N/a'
                    newtotal += int(shoe_deadstockSold2)
                    try:
                        shoe_lastSale = value['market']['lastSale']
                        """#shoe_lastSale = '$' + str(shoe_lastSale)
                        if len(str(shoe_lastSale)) == 4:
                            pass
                        if len(str(shoe_lastSale)) == 3:
                            shoe_lastSale = ' ' + str(shoe_lastSale)
                        if len(str(shoe_lastSale)) == 2:
                            shoe_lastSale = '  ' + str(shoe_lastSale)
                        if len(str(shoe_lastSale)) < 2:
                            shoe_lastSale = '   ' + str(shoe_lastSale)
                        """
                        shoe_lastSale = '$' + str(shoe_lastSale)# + '  '
                        #print(shoe_lastSale)
                    except:
                        shoe_lastSale = 'N/a'
                        
                    try:
                        shoe_saless = str(shoe_deadstockSold) + ' | ' + str(shoe_lastSale)
                        shoe_saless = ('{:11s}::{:5s} | {:5s}'.format(str(sizzeeess),str(shoe_deadstockSold), str(shoe_lastSale)))
                    except:
                        shoe_saless = ''
                    try:
                        #sizee_totals = str(shoe_deadstockSold) + ' | ' + str(sizzeeess)
                        #sizee_totals = ('{:8s} | {}'.format(str(shoe_deadstockSold),str(sizzeeess)))
                        #sizee_totals = ('{} | {}'.format(str(shoe_deadstockSold),str(sizzeeess)))
                        sizee_totals = ('{}| {}'.format(str(sizzeeess),str(shoe_deadstockSold)))
                    except:
                        sizee_totals = ''
                        
                    try:
                        shoe_highestBid = value['market']['highestBid']
                        #shoe_highestBid = '$' + str(shoe_highestBid)
                        """#print(len(shoe_highestBid))
                        if len(str(shoe_highestBid)) == 4:
                            pass
                        if len(str(shoe_highestBid)) == 3:
                            shoe_highestBid = ' ' + str(shoe_highestBid)
                        if len(str(shoe_highestBid)) == 2:
                            shoe_highestBid = '  ' + str(shoe_highestBid)
                        if len(str(shoe_highestBid)) < 2:
                            shoe_highestBid = '   ' + str(shoe_highestBid)
                        #if len(shoe_highestBid) == 1:
                        #    shoe_highestBid = ' 000' + str(shoe_highestBid)
                        """
                        shoe_highestBid = '$' + str(shoe_highestBid)# + '  '
                        #print(shoe_highestBid)
                    except:
                        shoe_highestBid = 'N/a'
                    try:
                        shoe_lowestAsk = value['market']['lowestAsk']
                        """#shoe_lowestAsk = '$' + str(shoe_lowestAsk)
                        if len(str(shoe_lowestAsk)) == 4:
                            pass
                        if len(str(shoe_lowestAsk)) == 3:
                            shoe_lowestAsk = ' ' + str(shoe_lowestAsk)
                        if len(str(shoe_lowestAsk)) == 2:
                            shoe_lowestAsk = '  ' + str(shoe_lowestAsk)
                        if len(str(shoe_lowestAsk)) < 2:
                            shoe_lowestAsk = '   ' + str(shoe_lowestAsk)
                        """
                        shoe_lowestAsk = '$' + str(shoe_lowestAsk)# + '  '
                        #print(shoe_lowestAsk)
                    except:
                        shoe_lowestAsk = 'N/a'

                    try:
                        #shoe_offerrrss = str(shoe_lastSale)  + ' | ' + str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                        #shoe_offerrrss = str(shoe_deadstockSold) + ' | ' + str(shoe_lastSale)  + ' | ' + str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                        #shoe_offerrrss = str(shoe_size) + 'str(shoe_highestBid) + ' | ' + str(shoe_lowestAsk)
                        #shoe_offerrrss = ('{:5s} | {:5s} | {:5s}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk)))
                        #shoe_offerrrss = ('{}|{}|{}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk),str(shoe_deadstockSold)))
                        shoe_offerrrss = ('{}|{}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk)))
                        #shoe_offerrrss = ('{:5s}|{:5s}|{:5s}|{}'.format(str(shoe_lastSale),str(shoe_highestBid), str(shoe_lowestAsk),str(shoe_deadstockSold),))
                    except:
                        shoe_offerrrss = ''
                    #if shoe_size == 8:
                    #    print(value[0]['market'])
                        #print(value['market'])
                        #print(key)
                    shoe_size = shoe_size.replace('.5', '½')

                    sizeandqty = ('{:30s} {:30s}'.format(str(sizee_totals), str(shoe_offerrrss)))
                    justthesizelist.append(sizeandqty)
                    newstocklist.append(sizeandqty)
                    sizelist.append(sizee_totals)
                    stocklist.append(shoe_offerrrss)
        except:
            justthesizelist = []
            newstocklist = []
            sizelist = []
            stocklist = []
            newtotal = 0
        #a
        try:
            shoename = str(json_dict['Product']['title'])
            #shoename = str(somethis['shiekh_collection_id'])
        except:
            shoename = 'N/A'
        try:
            skuname = str(json_dict['Product']['styleId'])
            skuname = skuname.replace(' ','')
        except:
            skuname = 'N/A'
        try:
            pricename = str(json_dict['Product']['retailPrice'])
            #shoename = str(somethis['shiekh_collection_id'])
        except :
            pricename = '$n/A'
        try:
            weblink = str(json_dict['Product']['urlKey'])
            weblink = 'https://stockx.com/' + str(weblink)
        except:
            weblink = 'N/A'
        try:
            product_image = json_dict['Product']['media']['imageUrl']
            #urllink = 'https://stockx.com/' + str(urllink)
        except:
            product_image = ''
        stockcount = str(newtotal)
        if stockcount == '0':
            stockcount = 'SOLD OUT'
            slackcolor = '#ff0000'
        else:
            slackcolor = '#36a64f'#print(listofsizeandpids)
        totalstockinfo = ('Total Stock :: ' + str(stockcount))
        twitterstock = ('#sizes: ' + str(stockcount)) 
        szieslis1 = []
        szieslis2 = []
        try:
            sizes_of = 15
            splitthesesizes = [sizelist[i:i+sizes_of] for i in range(0, len(sizelist), sizes_of)]
        except:
            splitthesesizes = []
        try:
            szieslis1 = (splitthesesizes[0])
        except:
            szieslis1 = sizelist
        try:
            szieslis2 = (splitthesesizes[1])
        except:
            szieslis2 = []
        stockssslis1 = []
        stockssslis2 = []
        try:
            sizes_of = 15
            splitthesstocks = [stocklist[i:i+sizes_of] for i in range(0, len(stocklist), sizes_of)]
        except:
            splitthesstocks = []
        try:
            stockssslis1 = (splitthesstocks[0])
        except:
            stockssslis1 = stocklist
        try:
            stockssslis2 = (splitthesstocks[1])
        except:
            stockssslis2 = []
        shoe_worthhhh = ':question_:  '   + ' :question_:  '
        try:
            if int(last_sale) < int(pricename):
                if int(last_sale) == 0:
                    slackcolor = '#ffff00'
                    #shoename = ' :question_:  ' + str(shoename) + ' ' + ' :question_:  '
                    shoe_worthhhh = ':question_:  '   + ' :question_:  '
                else:
                    slackcolor = '#ff0000'
                    #shoename = ' :bricks:  ' + str(shoename) + ' ' + '  :chart_with_downwards_trend: '
                    shoe_worthhhh = ':bricks:  '   + ' :chart_with_downwards_trend:  '
            if int(last_sale) > int(pricename) and  int(last_sale) < (int(pricename) + 50) :
                slackcolor = '#ffff00'
                #shoename = ' :question_:  ' + str(shoename) + ' ' + ' :question_:  '
                shoe_worthhhh = ':question_:  '   + ' :question_:  '
            if (int(last_sale) * 0.875) > (int(pricename) + 40) :
                slackcolor = '#36a64f'
                #shoename = '   :chart_with_upwards_trend:    ' + str(shoename) + ' ' + '    :chart_with_upwards_trend:    '
                shoe_worthhhh = ':chart_with_upwards_trend:  '   + ' :chart_with_upwards_trend:  '
        except:
            slackcolor = '#ffff00'
            shoename = ' :question_:  ' + str(shoename) + ' ' + ' :question_:  '
        try:
            buylink = weblink.replace('https://stockx.com/','https://stockx.com/buy/')
        except:
            buylink = str(weblink)
        try:
            selllink = weblink.replace('https://stockx.com/','https://stockx.com/sell/')
        except:
            selllink = str(weblink)
        #newlist.append(totalstockinfo)
        justthesizelist = ('::'.join(justthesizelist))#twitterstock = ('#sizes: ' + str(stockstatus)) 
        #checkingforchanges =  (' {} {} {} {}|{}'.format( str(skuname),str(shoename),str(weblink), str(newtotal), str(justthesizelist) ))
        #checkingforchanges =  ('{:15s}|| {:10s} ||{:5s}|| {:50s}||{:30s}||{:30s}||{}'.format( str(releasedate),str(skuname), str(last72_sold), str(shoename),str(lastsoldsize),  str(highest_offer), str(shoe_worthhhh) ))
        checkingforchanges =  ('{:15s}|| {:10s} ||{:10s}|| {:50s}||{:30s}||{:30s}||{}'.format( str(releasedate),str(skuname), str(total_sold), str(shoename),str(lastsoldsize),  str(highest_offer), str(shoe_worthhhh) ))
        #print(checkingforchanges)#checkingforchanges = (str(stocks_statuss) + '   ::   ' + str(totalstockinfo) + '   ::   ' + str(shoename) + '   ::   ' + str(updated_date) + '   ::   ' + str(weblink))
        #print(str(totalstockinfo) + '   ::   ' + str(shoename) + '   ::   ' + str(updated_date) + '   ::   ' + str(weblink))
        rightnowi = datetime.now()
        timefornotes = rightnowi.strftime('%I:%M:%S %p EST')
        slackcartlink = "<" + 'https://stockx.com' + "|" + 'CART' + ">"
        slackcheckoutlink = "<" + 'https://stockx.com' + "|" + 'CHECKOUT' + ">"
        slackcheckcartlinks = str(slackcartlink) + '   ||   ' + str(slackcheckoutlink)
        goatlink = "<" + 'https://www.goat.com/search?query=' + str(skuname) + "|" + 'GOAT' + ">"
        ebaylink = "<" + 'http://www.ebay.com/sch/i.html?_nkw=' + str(skuname) + "|" + 'EBAY' + ">"
        stockxlink = "<" + 'https://stockx.com/search?s=' + str(skuname) + "|" + 'STOCKX' + ">"
        fclink = "<" + 'https://www.flightclub.com/catalogsearch/result/?q=' + str(skuname) + "|" + 'FC' + ">"
        printstyledata = ('Style# : :: *' + str(skuname) + '*    || ' + str(goatlink) + ' | ' + str(ebaylink) + ' | ' + str(stockxlink) + ' | ' + str(fclink))
        printstyledata2 = (str(goatlink) + ' | ' + str(ebaylink) + ' | ' + str(stockxlink) + ' | ' + str(fclink))
        authlink = 'https://pbs.twimg.com/profile_images/1081587614141087745/c8Ri17Yf_400x400.jpg'
        currenti = datetime.now()
        currentdate = currenti.strftime('%m-%Y')
        newstocklist = ('\n'.join(newstocklist))                            
        sizelist = ('\n'.join(sizelist))                            
        szieslis1 = ('\n'.join(szieslis1))                            
        szieslis2 = ('\n'.join(szieslis2))                            
        stocklist = ('\n'.join(stocklist))                            
        stockssslis1 = ('\n'.join(stockssslis1))                            
        stockssslis2 = ('\n'.join(stockssslis2))                            
        itimenow = datetime.now()
        rightnow = itimenow.strftime('%I:%M:%S %p EST')
        try:
            if '#' not in weblink:
                random.shuffle(afflist)
                fakelink = random.choice(afflist)
                fakelink = '#' + str(fakelink)
            else:
                fakelink = ''
        except:
            fakelink = ''
        fakeproductpage = str(weblink) + str(fakelink)
        print()
        print('Name: :: ' + str(shoename) + '    Price :: ' + str(pricename))
        print(newstocklist)
        print()
        print(totalstockinfo)
        print('Link: :: ' + str(weblink))
        print()
        payload = {
            "attachments": [
                {
                    "fallback": shoename,# + '   -   ' + totalstockinfo,
                    "color": slackcolor,
                    #"pretext": '*|| Stockx ||*',
                    "author_name": 'RestocksRus - StockX Bot',
                    #"author_link": authlink,
                    "author_icon": authlink,
                    "title": shoename,# + '   -   ' + totalstockinfo,
                    "title_link": fakeproductpage,
                    #"text":  newstocklist,
                    "fields": [
                        {
                            "title": "SKU:",
                            "value": str(skuname),
                            "short": 'true'
                        },
                        {
                            "title": "RETAIL:",
                            "value": '$' + str(pricename),
                            "short": 'true'
                        },
                        {
                            "title": "STATUS:",
                            "value": str(shoe_worthhhh),
                            "short": 'true'
                        },
                        {
                            "title": "RELEASE:",
                            "value": str(releasedate),
                            "short": 'true'
                        },
                        {
                            #"title": "TOTAL | SIZES",
                            "title": "Size | # Sold",
                            "value": sizelist,
                            "short": 'true'
                        },
                        {
                            #"title": "LAST | High | Low ",
                            #"title": "Last|High|Low|Total",
                            "title": "Last|High|Low",
                            "value": stocklist,
                            "short": 'true'
                        },
                        {
                            "title": "TOTAL SOLD",
                            "value": newtotal,
                            "short": 'true'
                        },
                        { 
                            "title": "LAST SALE:",
                            "value": lastsoldsize,
                            "short": 'true'
                        },
                        {
                            "title": "LAST 72 HRS:",
                            "value": last72_sold,
                            "short": 'true'
                        },
                        { 
                            "title": "HIGHEST BID:",
                            "value": highest_offer,
                            "short": 'true'
                        },
                        {
                            "title": "",
                            "value": rightnow
                        }
                    ],
                    "actions": [
                        {
                            "type": "button",
                            "name": "LOGIN",
                            "text": "LOGIN",
                            "url": "https://stockx.com/login",
                            "style": "primary"
                            #"confirm": "Really?"
                        },
                        {
                            "type": "button",
                            "name": "SELL",
                            "text": "SELL",
                            "url": selllink,
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "name": "BUY",
                            "text": "BUY",
                            "url": buylink,
                            "style": "primary"
                        }
                    ],
                    #"image_url": product_image,
                    "thumb_url": product_image,
                    "footer": "RestockRus- StockX Bot",
                    #"footer_icon": product_image,
                    "mrkdwn_in": ["text","fields", "fallback", "pretext"]
                    #"ts": 123456789#"ts": product_image
                }
            ]
        }
        try:
            
            slack_hook = 'https://hooks.slack.com/services/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' ### testing
            requests.post(slack_hook, data = json.dumps(payload), headers={'Content-Type': 'application/json'})
        except:
            print('#!#!#!#!#!#!#!#!#!#! ERROR: SLACK MSG NOT SENT #!#!#!#!#!#!#!#!#!#!')

    else:
        print('NO PRODUCT FOUND')
