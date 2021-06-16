from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import socket

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Work@2021'
app.config['MYSQL_DATABASE_DB'] = 'forms_data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def main():
	return render_template('index2.html')

@app.route("/submit", methods=['POST'])
def form():
	_name = request.form['name']
	_tno = request.form['tno']
	_size = request.form['size']

	cursor.callproc('sp_forms',(_name,_tno,_size))
	data = cursor.fetchall()

	#cursor.execute("SELECT * from formdata_table")
	#result = cursor.fetchall()
	#return render_template('table.html',  result = cursor.fetchall())


	if len(data) == 0:
		conn.commit()
		cursor.execute("SELECT * from formdata_table")
        	#result = cursor.fetchall()
		return render_template('table.html',  result = cursor.fetchall())

		#return render_template('table.html', name = _name, tno = _tno, size = _size)
	else:
		return json.dumps({'error':str(data[0])})

def get_Host_name_IP():
	try:
		host_name = socket.gethostname()
		host_ip = socket.gethostbyname(host_name)
		return json.dumps({"Host IP":host_ip})
	except:
		return json.dumps({"Error": "Unable to get Hostname and IP"})


if __name__ == "__main__":
    app.run()
