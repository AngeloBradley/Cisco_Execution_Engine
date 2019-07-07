from flask import Flask, render_template, request, jsonify
from importlib import import_module
from __selectionPanelToolBox import loadDeviceList as ldl
from __selectionPanelToolBox import loadTestCaseNames as ltcn
import os, json, queue, threading, time, datetime, sqlite3
from multiprocessing import Process, Queue
import subprocess

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#Route that handles requests triggered by clicking one of the selection panel buttons; handles Device Repository and Test Case Repository but
#not Saved Results
@app.route('/selectionPanelResponse', methods=['POST'])
def selectionPanelResponse():
    repoName = request.form['repository']

    if repoName == 'device_repository':
        data = ldl.loadDeviceList()
        return jsonify(data)

    elif repoName == 'test_case_repository':
        data = ltcn.loadTestCaseNames()
        return jsonify(data)
    elif repoName == 'saved_results':
        pass

#Route that handles requests triggered by a user attempting to upload a script
#This method retrieves the string containing the script data from the AJAX request, creates a new document and dumps the script
#into the new document
@app.route('/userGeneratedScriptUploading', methods=['POST'])
def userGeneratedScriptUploading():
    script = request.form['_script']
    scriptName = request.form['_scriptName'] + '.py'
    returnScriptName = scriptName
    subdirectory = '__test_case_repository'

    scriptName = os.path.join(subdirectory, scriptName)

    scriptWriter = open(scriptName, 'w')
    scriptWriter.write(script)
    scriptWriter.close()

    return jsonify({'name' : returnScriptName})

#Route that handles requests triggered by a user attempting to delete a script from the test case repository
@app.route('/removeScriptsFromRepo', methods=['POST'])
def removeScriptsFromRepo():
    scriptsList = json.loads(request.form['scriptslist'])
    for i in range(len(scriptsList)):
        os.remove("__test_case_repository/" + scriptsList[i])

    
    return jsonify({'ret' : scriptsList})

#Route that returns all of the saved results from the database SavedResults.db located in the root directory
@app.route('/updateDatabase', methods=['POST'])
def updateDatabase():
    data = []

    conn = sqlite3.connect('SavedResults.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM results'):
            data.append(row)

    return jsonify({'database': data})

############################Execution Queue############################
execQ = Queue()
execList = []
@app.route('/executeScripts', methods=['POST'])
def executeScripts():
    scriptsList = json.loads(request.form['scriptslist'])
    for script in scriptsList:
        execQ.put(script)
        execList.append(script)

    return jsonify({'ret' : execList})

databaseResults = {}

def executioner():

    while True:
        #for resource preservation, this loop sleeps for 5 seconds each iteration
        time.sleep(5)
        #if the execution queue is empty it passes to the end of the loop and checks again
        if execQ.empty():
            pass
        else:
            #if the execution queue is not empty, a connection to the database is established, the script is run and the database is updated
            conn = sqlite3.connect('SavedResults.db')
            c = conn.cursor()
            
            dt = datetime.datetime.now()
            test_date_time = '{:%a %m/%d/%y %H:%M %p}'.format(dt)
            testName = execQ.get()
            results_name = ''
            
            #this does yet work as intended, the problem is that any errors encountered by the script appear to be registered by the script
            #itself and the error is never reported back to this try/except statement so the only errors this catches are errors
            #surrounding this script's inability to access or find the specified file
            try:
                pass_fail = 'pass'
                os.system('python __test_case_repository/' + testName)
                print('Test Done!!!')
            except:
                pass_fail = 'fail'
                print('ERROR!!!')
            
            c.execute('INSERT INTO results (date_time, test_name, pass_fail, results_name) VALUES (?, ?, ?, ?)', (test_date_time, testName, pass_fail, results_name))
            
            conn.commit()
            c.close()
            conn.close()
            print('database updated')

if __name__ == '__main__':
    #create a new thread before starting the app, the executioner method is kicked into gear and is always running while the server is running
    #not implemented yet are the instructions for handling a situation in which the executioner method stops running while the server is still up
    t = threading.Thread(target=executioner)
    t.daemon = True
    t.start()
    #debup is set to true because the app is still in development
    app.run(threaded=True, debug=True)
    