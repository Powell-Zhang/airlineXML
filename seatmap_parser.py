import sys
from os import path
import xml.etree.ElementTree as ET
import re
import json

def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

if len(sys.argv) == 1:
    print('no input')
    exit(0)
fileName = sys.argv[1]
if not path.exists(fileName):
    print('file %s not found', fileName)
if fileName == 'seatmap1.xml':
    num = 1
if fileName == 'seatmap2.xml':
    num = 2
if len(sys.argv) > 2:
   nums = sys.argv[2]


tree = ET.parse(fileName)
root = tree.getroot()

if num == 1:
    rows = []
    ns = namespace(root)
    for head in root.findall(ns + 'Body'):
        for child in head:
            ns = namespace(child)
            for h in child.findall('*/' + ns + 'SeatMapResponse'):
                for a in h.findall('*/' + ns + 'CabinClass'):
                    for row in a:
                        clas = row.attrib['CabinType']
                        seats = []
                        for seat in row.findall(ns + 'SeatInfo'):
                            summary = seat.find(ns + 'Summary')
                            tpe = None
                            idx = summary.attrib['SeatNumber']
                            price = None
                            availability = False
                            if summary.attrib['AvailableInd'] == 'true':
                                availability = True
                                price = int(seat.find(ns + 'Service').find(ns + 'Fee').attrib['Amount'] + seat.find(ns + 'Service').find(ns + 'Fee').find(ns + 'Taxes').attrib['Amount'])
                            misc = []
                            for f in seat.findall(ns + 'Features'):
                                if f.text == 'Aisle':
                                    tpe = 'AISLE'
                                elif f.text == 'Center':
                                    tpe = 'CENTER'
                                elif f.text == 'WINDOW':
                                    tpe = 'WINDOW'
                                elif f.text == 'Other_':
                                    misc.append(f.attrib['extension'])
                                else:
                                    misc.append(f.text)
                            seats.append({
                                'Element Type': 'Seat',
                                'Seat Type': tpe,
                                'ID': idx,
                                'Price': price,
                                'Class': clas,
                                'Availability': availability,
                                'Misc': misc
                            })
                        rows.append({'Seats': seats})
elif num == 2:
    ns = namespace(root)
    ids = {}
    for head in root.findall('*/' + ns + 'SeatDefinitionList'):
        for defin in head:
            id = defin.attrib['SeatDefinitionID']

            for d in defin:
                for t in d:
                    text = t.text
            ids.update({id: text})
    rows = []
    for head in root.findall(ns + 'SeatMap'):
        for row in head.findall('*/' + ns + 'Row'):
            rowNum = row.find(ns + 'Number').text
            seats = []
            for seat in row.findall(ns + 'Seat'):
                tpe = 'CENTER'
                idx = rowNum + seat.find(ns + 'Column').text
                price = None
                clas = None
                availability = None
                misc = []
                for ref in seat.findall(ns + 'SeatDefinitionRef'):
                    a = ids.get(ref.text)
                    if (a == 'AVAILABLE'):
                        availability = True
                    elif (a == 'OCCUPIED'):
                        availability = False
                    elif (a == 'AISLE'):
                        tpe = 'AISLE'
                    elif (a == 'WINDOW'):
                        tpe = 'WINDOW'
                    else:
                        misc.append(a)
                seats.append({
                    'Element Type': 'Seat',
                    'Type': tpe,
                    'ID': idx,
                    'Price': price,
                    'Class': clas,
                    'Availability': availability,
                    'Misc': misc
                })
            rows.append({'Seats': seats})
with open(fileName+'_parsed.json', 'w') as outfile:
    json.dump({'Rows': rows}, outfile)

