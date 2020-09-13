# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from datetime import datetime, date, timedelta
import pandas as pd
from app import models
from . import util
from app import models
import sqlite3,csv
from django.http.response import JsonResponse
from django.db import IntegrityError
from api import serializers
from . import static_values
from rest_framework.decorators import api_view
@login_required(login_url="/login/")
def remittance(request):
    v = models.Vendor.objects.all().order_by('vendor')
    data=[]
    for d in v:
        data += [d]
    return render(request, "remittance.html",context={'vendors':data})#

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

def saveInvoiceCSV(invoice,vendor):

    filename='data/'+str(vendor.vendor)+'.csv'#
    with open(filename,'w') as f:
        f.write("Name  of Vendor,Reference,Posting date,Document Date,Clearing Date,Payment method,Check number,Amount,Currency\n" )
        for i in invoice:
            print(i)
            
            f.write(vendor.Name_1+','+i.reference +','+i.posting_date+','+i.clearing_date+','+static_values.payment_method[i.payment_method]+','+i.check +','+str(i.amount) + '\n')
def loadInvoice(request):
    processing_dt=datetime.now() - timedelta(1)
    processing_date = processing_dt.strftime('%m-%d-%Y')
    filename = "data/invoice-"+processing_date+".csv"
    cnx = sqlite3.connect('db.sqlite3')
    header=None
    with open(filename) as csvfile:
        header1=None
        for line in csvfile.readlines()[1:]:
            if not header: 
                header = [h.replace(' ','_').replace('/','_').replace("\n",'').replace('.','') for h in line.split(',')]
                continue
            record = dict(zip(header,line.split(',')))
            # print (record)

            h2 = ["'" + h + "'" for h in header]
            header1 = ','.join(h2) + ",create_date,update_date "
            row = ["'" + d +"'" for d in line.replace('\n','').replace('#N/A','').split(',')]
            insert = "insert into app_invoice ({}) values ({})".format(header1,','.join(row)+",'"+str(datetime.now()) + "',''")
            update=""#@
            for i,d in enumerate(header):
                update += "'{}'={},".format(d,row[i]) 
            update += " update_date= '{}'".format (str(datetime.now()))
            where = "company_code='{}' AND vendor='{}' AND document_number='{}'".format(record['Company_Code'],record["Vendor"], record["Document_Number"])
            update = 'update app_invoice set ' + update + " WHERE " + where
            try:
                cnx.execute(insert)
                # break
            except Exception as e:
                print(e)
                cnx.execute(update)
                # continue
            cnx.commit()
    sendEmailBatchJob(processing_date)
    return JsonResponse({'success':True, 'errorMsg':None})
def sendEmailBatchJob(processing_date):
    print(processing_date)
    cnx = sqlite3.connect('db.sqlite3')
    v = models.Vendor.objects.all().filter(Email__isnull = False)  
    for vendor in v:
        invoice = models.Invoice.objects.all().filter(vendor= vendor.vendor,clearing_date = processing_date)  
        # print(invoice)
        if invoice.count()>0:
            saveInvoiceCSV(invoice,vendor)
                # util.sendMailWithAttachment({"emails":[v[0].Email],"clearing_date":record["Clearing_date"],"amount":record["Amount"],"supplier":v[0].Name_1,"currency":record["Currency"].upper(),'attachment' : savedFilename })#                

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

def vendors(request):
    v = models.Vendor.objects.all().values() 
    # print(v[0])
    data=[]
    for d in v:
        data += [d]
    return JsonResponse({'data':data,'status':200})
@api_view(['GET'])
def invoices(request):
    vendorid=request.GET.get('vendorid',0)
    companyid=request.GET.get('companyid',0)
    clearing_date_range=request.GET.get('clearing_date_range',0)
    print(companyid,vendorid,clearing_date_range)
    v=None
    
    if companyid and vendorid and clearing_date_range:
        d = clearing_date_range.split('-')
        from_date = d[0].strip().split('/')
        from_date = from_date[2]+'-'+from_date[0]+'-'+from_date[1]
        to_date = d[1].strip().split('/')
        to_date = to_date[2]+'-'+to_date[0]+'-'+to_date[1]
        print(from_date,to_date)
        v = models.Invoice.objects.all().filter(company_code=companyid,vendor=vendorid).values() 
        o=[]
        for x in v:
            cd = x['clearing_date'].split('-')
            cd1 = cd[2]+'-'+cd[0]+'-'+cd[1]
            if from_date == to_date and cd1 == from_date :
                    o += [x]
            elif cd1 >= from_date and cd1<=to_date:
                    o += [x]
        return JsonResponse({'count':o.count(),'data':o,'status':200})
    else:   
        v = models.Invoice.objects.all().values() 
    # print(v)
    data=[]
    for d in v:
        data += [d]
    return JsonResponse({'count':v.count(),'data':data,'status':200})
    