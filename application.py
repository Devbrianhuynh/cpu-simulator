from cpu_cache import CPU
from flask import Flask, render_template, request


# Global variables
cpu = None
message = [] # Feedback for the user to indicate a data assign or retrieval
shut_down_data_check = 0 # Checks to see if the user has saved their progress before shutting down; 0 = not saved, 1 = saved
clock_speed_message = None
ram_gbs_message = None
ssd_gbs_message = None


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/computer', methods = ['GET', 'POST'])
def computer():
    global cpu
    global message
    global shut_down_data_check
    global clock_speed_message
    global ram_gbs_message
    global ssd_gbs_message

    if request.method == 'POST' and 'save_specs' in request.form:
        # Edge-case scenario: User clicks on the submit form button before they enter the information; use try/except to prevent errors from occuring
        try:
            model = request.form['model'].lower()
            clock_speed = float(request.form['clock_speed'])
            cores = float(request.form['cores'])
            cache_blocks = int(request.form['cache_blocks'])
            ram_gbs = int(request.form['ram_gbs'])
            ssd_gbs = int(request.form['ssd_gbs'])
            cache_access_time = float(request.form['cache_access_time'])
            ram_access_time = float(request.form['ram_access_time'])
            ssd_access_time = float(request.form['ssd_access_time'])
            cache_write_preference = request.form['cache_write_preference'].lower()

            fine_tune_cpu = request.form.get('fine_tune_cpu') # Not included as a parameter for CPU

        except:
            return render_template('index.html')

        # Send data to the database
        global cpu
        cpu = CPU(model, clock_speed, cores, cache_blocks, ram_gbs, ssd_gbs, cache_access_time, ram_access_time, ssd_access_time, cache_write_preference)

        if fine_tune_cpu == 'fine_tune':
            cpu.clock_speed_fine_tuning()

        global clock_speed_message
        clock_speed_message = str(clock_speed) + 'GHz'

        global ram_gbs_message
        ram_gbs_message = str(ram_gbs) + 'GBs'

        global ssd_gbs_message
        ssd_gbs_message = str(ssd_gbs) + 'GBs'
       
        return render_template('index.html',
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    

    # Store data into cache
    # Button: Submit 
    if request.method == 'POST' and 'store_cache' in request.form:
        topic = request.form['topic']
        description_story_thoughts = request.form['description_story_thoughts']
        
        # Prevent an error from occuring if the user clicks on a button before they even enter any computer specs or address and data
        try:
            store_cache = cpu.add_cache_data(topic, description_story_thoughts) # Collect all of the messages returned by writing and reading the cache, RAM, and SSD
        except:
            return render_template('index.html', warning_message = 'Error: Submit only works if Topic and Description/Story/Thoughts is filled out')
        

        message.append(store_cache)

        # 1 = saved; since we are adding more data to the cache, this new data isn't saved, so the shut_down_data_check = 0
        if shut_down_data_check > 1:
            shut_down_data_check = 0

        return render_template('index.html', 
                               message = message, 
                               execution_time = cpu.get_execution_time(), 
                               shut_down_data_check_message = 'Not Saved',
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    

    # Read data from cache
    # Button: Find Topic 
    if request.method == 'POST' and 'read_cache' in request.form:
        topic = request.form['topic']

        try:
            read_cache = cpu.read_cache_data(topic)
        except:
            return render_template('index.html', warning_message = 'Error: Nothing inside the cache to read')
        
    
        message.append(read_cache)

        execution_time = cpu.get_execution_time()

        # We know that the progress has been saved if the index is (or over) 1
        shut_down_data_check_message = 'Saved' if shut_down_data_check > 1 else 'Not Saved'

        return render_template('index.html', 
                               message = message, 
                               execution_time = execution_time, 
                               shut_down_data_check_message = shut_down_data_check_message,
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    

    # Store data into SSD
    # Button: Save 
    if request.method == 'POST' and 'store_ssd' in request.form:
        topic = request.form['topic']
        description_story_thoughts = request.form['description_story_thoughts']

        try:
            store_ssd = cpu.add_ssd_data(topic, description_story_thoughts)
        except:
            return render_template('index.html', warning_message = 'Error: Save only works if Topic and Description/Story/Thoughts is filled out')
        

        message.append(store_ssd)

        execution_time = cpu.get_execution_time()

        if shut_down_data_check > 1:
            shut_down_data_check = 0

        return render_template('index.html', 
                               message = message, 
                               execution_time = execution_time, 
                               shut_down_data_check_message = 'Not Saved',
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    

    # Read data from SSD
    # Button: Search OS 
    if request.method == 'POST' and 'read_ssd' in request.form:
        topic = request.form['topic']

        try:
            read_ssd = cpu.read_ssd_data(topic)
        except:
            return render_template('index.html', warning_message = 'Error: Nothing inside the SSD to read')
        
        
        message.append(read_ssd)

        execution_time = cpu.get_execution_time()

        shut_down_data_check_message = 'Saved' if shut_down_data_check > 1 else 'Not Saved'

        return render_template('index.html', 
                               message = message, 
                               execution_time = execution_time,
                               shut_down_data_check_message = shut_down_data_check_message,
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    

    # Button: Save Progress 
    if request.method == 'POST' and 'save_progress' in request.form:
        try:
            save_progress = cpu.save_progress()
        except:
            return render_template('index.html', warning_message = 'Error: Nothing inside the RAM to save to the SSD')
        

        message.append(save_progress)

        shut_down_data_check += 1

        return render_template('index.html', 
                               message = message, 
                               shut_down_data_check_message = 'Saved',
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)
    
    
    # Button: Shut Down 
    if request.method == 'POST' and 'shut_down' in request.form:
        if shut_down_data_check == 0:
            try:
                wipeout_progress = cpu.wipeout_progress()
            except:
                return render_template('index.html', warning_message = 'Error: Clicked on Shut Down before using the simulation')
            

            message.append(wipeout_progress)
            message.append('Progress not saved beforehand. Shutting down now')

            shut_down_data_check_message = 'Not Saved'

        elif shut_down_data_check == 1:
            message.append('Progress saved beforehand. Shutting down now')

            shut_down_data_check_message = 'Saved'

        return render_template('index.html', 
                               message = message, 
                               shut_down_data_check_message = shut_down_data_check_message,
                               model = cpu.model,
                               clock_speed_message = clock_speed_message,
                               ram_gbs_message = ram_gbs_message,
                               ssd_gbs_message = ssd_gbs_message)


if __name__ == '__main__':
    app.run(debug=True)










