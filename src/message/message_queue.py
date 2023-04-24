status_ingestion = ""

from websockets.sync.client import connect

"""
Method to send information to the socket of this server, so clients connected are aware of the status of certain process.
Params
    @message: Message to send to the websocket.
"""
def send_websocket_message(message):
    try:
        with connect("ws://localhost:5564") as websocket:
            websocket.send(message)
    except Exception as ex:
        print(ex)

"""
Method to change the variable status_ingestion according to the given parameters, and send this new value as a message to the websocket server by calling the method send_websocket_message.
Params:
    @status_step: String. Detail of the progress
    @status_progress: Numeric. Progress (desirable in percentage) related to the ingestion of the data
"""    
def update_status(status_step, status_progress):
    global status_ingestion
    status_ingestion = '{step} - Progress: {prog}'.format(step=status_step, prog = status_progress)
    send_websocket_message(status_ingestion)

