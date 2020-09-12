# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from datetime import datetime
from datetime import date
import pandas as pd
from app import models
from . import util
from app import models
import sqlite3,csv
from django.http.response import JsonResponse
from django.db import IntegrityError

@login_required(login_url="/login/")
def remittance(request):
    return render(request, "remittance.html")

@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def loadInvoice(request):

    todays_date = str(date.today())
    filename = 'data/invoice-'+todays_date+".csv"

    cnx = sqlite3.connect('db.sqlite3')
    with open(filename) as csvfile:
        header=None
        header1=None
        for line in csvfile.readlines()[1:]:
            # print(line)
            if not header:                
                header = [h.replace(' ','_').replace('/','_').replace("\n",'').replace('.','') for h in line.split(',')]
                continue
            record = dict(zip(header,line.split(',')))
            # print (record)

            # break
            h2 = ["'" + h + "'" for h in header]
            header1 = ','.join(h2) + ",create_date,update_date "
            row = ["'" + d +"'" for d in line.replace('\n','').replace('#N/A','').split(',')]
            insert = "insert into app_invoice ({}) values ({})".format(header1,','.join(row)+",'"+str(datetime.now()) + "',''")
            # update=""#@
            # for i,d in enumerate(header):
            #     update += "'{}'={},".format(d,row[i]) 
            # update += " update_date= '{}'".format (str(datetime.now()))
            # where = "company_code='{}' AND vendor='{}' AND document_number='{}'".format(record['Company_Code'],record["Vendor"], record["Document_Number"])
            # update = 'update app_invoice set ' + update + " WHERE " + where
            # print(insert,update)
            # x = Invoice.objects.all().filter(Invoice__Company_Code=record['Company_Code'], Invoice__vendor=record["Vendor"], Invoice__Document_Number=record["Document_Number"])
            # if x.count()==0:
            try:
                # cnx.execute(insert)
                v = models.Vendor.objects.all().filter(vendor=record['Vendor'])  
                print ( v.count(),v[0].vendor,v[0].Name_1,v[0].Email)
                if v.count()>0 and v[0].vendor and v[0].Email:
                    util.sendmail2({"emails":[v[0].Email],"clearing_date":record["Clearing_date"],"amount":record["Amount"],"supplier":v[0].Name_1,"currency":record["currency"].upper()  })#                
                # break
            except Exception as e:
                print(e)
                continue
            # elif  x.count()>0:
            #     cnx.execute(update)

        cnx.commit()
    return JsonResponse({'success':True, 'errorMsg':None})
def loadVendor(request):

    todays_date = str(date.today())
    filename = 'data/Vendor_Master.csv'

    import sqlite3,csv
    from django.http.response import JsonResponse
    from django.db import IntegrityError
    cnx = sqlite3.connect('db.sqlite3')
    with open(filename) as csvfile:
        header=None
        header1=None
        for line in csvfile.readlines()[1:]:
            # print(line)
            if not header:                
                header = [h.replace(' ','_').replace('/','_').replace("\n",'').replace('.','') for h in line.split(',')]
                continue
            record = dict(zip(header,line.split(',')))
            print (record)

            # break
            h2 = ["'" + h + "'" for h in header]
            header1 = ','.join(h2) + ",create_date,update_date "
            row = ["'" + d +"'" for d in line.replace('\n','').replace('#N/A','').split(',')]
            insert = "insert into app_vendor ({}) values ({})".format(header1,','.join(row)+",'"+str(datetime.now()) + "',''")
            # update=""#@
            # for i,d in enumerate(header):
            #     update += "'{}'={},".format(d,row[i]) 
            # update += " update_date= '{}'".format (str(datetime.now()))
            # where = "company_code='{}' AND vendor='{}' AND document_number='{}'".format(record['Company_Code'],record["Vendor"], record["Document_Number"])
            # update = 'update app_invoice set ' + update + " WHERE " + where
            # print(insert,update)
            # x = Invoice.objects.all().filter(Invoice__Company_Code=record['Company_Code'], Invoice__vendor=record["Vendor"], Invoice__Document_Number=record["Document_Number"])
            # if x.count()==0:
            try:
                cnx.execute(insert)    
            except Exception as e :
                print(e)
                continue
            # elif  x.count()>0:
            #     cnx.execute(update)

        cnx.commit()
    return JsonResponse({'success':True, 'errorMsg':None})

