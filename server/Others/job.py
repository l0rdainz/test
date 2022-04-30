import uuid

def process_job(job):
    
    totalexp = int((int(job["Tempsweep"][1]) -int(job['Tempsweep'][0])+1)/int(job["Tempsweep"][2]) * job["Replicates"])
    print(totalexp)
    job["Bioreactorsreq"]=int(totalexp/6)
    for exp in range(totalexp):
        job["Experimentid"].append(uuid.uuid4())
    return job






