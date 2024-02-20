from datetime import datetime


def save_job_log(jobid, log):
    with open(".prx/jobid.txt", "a+") as f:
        f.write(jobid)
        f.write("\t")
        f.write(str(datetime.now()))
        f.write("\t")
        f.write(log)
        f.write("\n")


def save_job_log_in_csv(jobid, log):
    with open(".prx/jobid.csv", "a+") as f:
        f.write(jobid)
        f.write(",")
        f.write(str(datetime.now()))
        f.write(",")
        f.write(log)
        f.write("\n")
