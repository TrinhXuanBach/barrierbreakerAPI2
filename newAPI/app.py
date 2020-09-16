from flask import Flask, request, jsonify, json
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlite3 import connect
from model import Home

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_combined_ds.db' 
db = SQLAlchemy(app)

@app.route('/', methods = ['GET'])
def getData():   
    try:
        district = request.args.get('district')
        page     = int(request.args.get('page'))
        minPrice = request.args.get('min_price')
        maxPrice = request.args.get('max_price')
        first    = (page - 1)*20
        last     = page*20

        sql = text('''SELECT Price, Area, Num_Bathroom, Num_Bedroom, Img_Src, Date  
                    FROM Web_Combined_Table 
                    WHERE District = '{}' AND (Price BETWEEN '{}' AND '{}') 
                    LIMIT {} '''.format(district, minPrice, maxPrice, last))
        
        query = text('''SELECT AVG(Price) as average 
                        FROM Web_Combined_Table
                        WHERE District = '{}' AND (Price BETWEEN '{}' AND '{}')'''
                        .format(district, minPrice, maxPrice))
        result = db.engine.execute(sql)
        result_average = db.engine.execute(query)

        listData = []
        total_row = result.fetchall()
        average = result_average.fetchone()['average']

        result.close()
        result_average.close()
        
        length = len(total_row)

        if length < last:
            last = length            

        for x in range(first, last):
            row  = total_row[x]
            home = Home(row['Price'], row['Area'], row['Num_Bathroom'], row['Num_Bedroom'], row['Img_Src'], row['Date']) 
            listData.append(home.toJson())

        return json.dumps({'average' : average,'list_data' : listData})
    except Exception as e:
        print(e)
        return "error"


@app.route('/detailByMenu', methods = ['GET'])
def getDetailDataByMenu():
    try:
        area = request.args.get('area')
        street = request.args.get('street')
        ward = request.args.get('ward')
        orientation = request.args.get('orientation')
        page = int(request.args.get('page'))
    

        first    = (page - 1)*20
        last     = page*20

        condition = conditionQuery(area=area, street=street, ward=ward, orientation=orientation)

        query = text('''SELECT Price, Area, Num_Bathroom, Num_Bedroom, Img_Src, Date
                    FROM Web_Combined_Table 
                    WHERE {}
                    LIMIT {}'''.format(condition, last))
        result = db.engine.execute(query)

        listData = []
        total_row = result.fetchall()
        result.close()

        length = len(total_row)

        if length < last: 
            last = length

        for index in range(first, last):
            row  = total_row[index]
            home = Home(row['Price'], row['Area'], row['Num_Bathroom'], row['Num_Bedroom'], row['Img_Src'], row['Date'])
            listData.append(home.toJson())            

        return json.dumps(listData)
    except Exception as error:
        return "error"        

@app.route('/detailBySearch', methods = ['GET'])
def getDetailBySearch():
    try:
        listData = []
        address = request.args.get('address')
        query   = text('''SELECT Price, Area, Num_Bathroom, Num_Bedroom, Img_Src, Date
                         FROM Web_Combined_Table
                         WHERE Address LIKE '%{}%' '''.format(address))

        result  = db.engine.execute(query)
        total_row = result.fetchall()
        result.close()

        for row in total_row:
            home = Home(row['Price'], row['Area'], row['Num_Bathroom'], row['Num_Bedroom'], row['Img_Src'], row['Date'])
            listData.append(home.toJson())
        return json.dumps(listData)

    except Exception as error:
        return "error"

@app.route('/getDetailAHome', methods = ['GET'])
def getDetailAHome():
    try:
        return "oke"
    except Exception as error:
        return "error"

def conditionQuery(area, street, ward, orientation): 
    condition = ''
    if area:
        condition = condition + "Area = '{}'".format(area) + " AND "

    if street:
        condition = condition + "Street = '{}'".format(street) + " AND "

    if ward:
        condition = condition + "Ward = '{}'".format(ward) + " AND "

    if orientation:
        condition = condition + "Orientation = '{}'".format(orientation) + " AND "    
    return condition[0:len(condition) - 4]

if __name__ == '__main__':
    app.run(debug=True)
