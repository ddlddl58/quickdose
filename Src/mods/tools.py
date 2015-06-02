#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jan 16, 2014

@author: hofmanr8

this module containts different auxiliary functions for processing of dates etc.
'''

import datetime
DATE_FORMAT = "%Y%m%d %H%M%S"


def get_run_name(time_step, source_id):
    """
    generates a directory name suitable for a source s at time step t
    """
    return "R_t=%4.4d_id=%4.4d" % (time_step, source_id)

def make_flexpart_date(date):
    """
    converts datetime into flexpart date string format
    """
    DATE_FORMAT_F = "%Y%m%d %H%M%S"
    return date.strftime(DATE_FORMAT_F)

def make_tree_date(date):
    """
    makes tree data string format from datetime
    """
    DATE_FORMAT_T = "%Y%m%d_%H"
    return date.strftime(DATE_FORMAT_T)

def get_minute_range(min_date, max_date):
    """
    return the length of a time interval between two dates in minutes
    """
    delta = max_date - min_date
    return int(delta.days*24*60 + delta.seconds/60.)

def get_sec_range(min_date, max_date):
    """
    return the length of a time interval between two dates in minutes
    """
    delta = max_date - min_date
    return int(delta.days*24*3600 + delta.seconds)

def get_date_from_str(date_str):
    """
    returns datetime.datetime from string date
    """
    return datetime.datetime.strptime(date_str, DATE_FORMAT)

def gds(date):
    """
    just a wrapper with a short name for get_date_from_str()
    """
    return get_date_from_str(date)

def get_lon_lat_dict(data_dict):
    """
    return a dictionary where keys are stationa codes and vals are tuples with their their (lon, lat)
    """
    lon_lat_d = {}
    for station in data_dict.keys():
        lon_lat_d[station] = (data_dict[station]["lon"], data_dict[station]["lat"]) 
        
    return lon_lat_d
    
    
def make_synoptic_dates(date1, date2, modulo=3):
    """
    date1, date2 are datetime objects
    floors the datetime to the nearest synoptic hour, ie. must be modulo 3
    - timedelat between date1 and date2 remians the same, they are just shifted to
    be aligned with synoptic dates
    """
    
    time_delta_orig = date2 - date1
    
    if time_delta_orig == datetime.timedelta(seconds=12*3600 - 1):
        #print "...Modifiying 11:59:59 into 12:00:00" 
        time_delta_orig = datetime.timedelta(seconds=12*3600)
    
    y = date1.year
    m = date1.month
    d = date1.day
    h = date1.hour
    mi = date1.minute
    
    if h%modulo != 0. or mi > 0.:
        date1_syn = datetime.datetime(y,m,d,h - h%modulo) + datetime.timedelta(seconds=modulo*3600.)
    else:
        date1_syn = datetime.datetime(y,m,d,h) #only seconds can be clipped
                                      
    date2_syn = date1_syn + time_delta_orig
    
    return date1_syn, date2_syn

def get_min_max_synaptic_dates(samples):
    """
    return minimum and maximum dates in a list of samples
    """
    #initialization - reversed
    maxd, mind = make_synoptic_dates( gds(samples[0][2]), gds(samples[0][3]) )
    
    for samp in samples:
        date1 = gds(samp[2])
        date2 = gds(samp[3])
        
        date1_s, date2_s = make_synoptic_dates( date1, date2 )
        
        if date1_s < mind:
            mind = date1_s
        if date2_s > maxd:
            maxd = date2_s
            
    return mind, maxd
        
    