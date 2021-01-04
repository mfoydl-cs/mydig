from dns import message as msg
from dns import query as q
from dns import name
import time
import sys

try:
    domain = str(sys.argv[1])
except:
    print("Error parsing input, please provide valid domain")

root = 0
rootservers = ["198.41.0.4","199.9.14.201","192.33.4.12",
               "199.7.91.13","192.203.230.10","192.5.5.241",
               "192.112.36.4","198.97.190.53","192.36.148.17",
               "192.58.128.30","193.0.14.129","199.7.83.42","202.12.27.33"]
response = None
stime = time.ctime()
start = time.time() #time.perf_counter()
try:

    message = msg.make_query(domain, 1)
    response = q.udp(message,rootservers[root])
    i=0
    while(len(response.answer)==0):
        if len(response.additional) >0:
            try:
               response2 = q.udp(message, str(response.additional[i].items[0]),20)
            except Exception as e:
                if i < len(response.additional):
                    i=i+1
                else:
                    print(e)
            finally:
                response = response2
    question = response.question
    answer =  response.answer
    if response.answer[0].rdtype == 5:
        try:
            message2 = msg.make_query(str(response.answer[0].items[0]),1)
            response = q.udp(message2,rootservers[root],20)
        except Exception as e:
            print(e)
        finally:
            i=0
            while len(response.answer) == 0:
                if len(response.additional)>0:
                    try:
                        response2 = q.udp(message2, str(response.additional[i].items[0]),20)
                    except Exception as e:
                        if i < len(response2.additional):
                            i=i+1
                        else:
                            print(e)
                    finally:
                        response = response2
            end= time.time()#time.perf_counter()
            print("\nQUESTION SECTION: ")
            for entry in question:
                print(entry)
            print("\nANSWER SECTION: ")
            for entry in answer:
                print(entry)
            for entry in response.answer:
                print(entry)
            print("\nQuery Time: ",(end-start)*1000,"ms")
            print("When: ",stime)
            
    else:
        end = time.time() #time.perf_counter()
        print("\nQUESTION SECTION: ")
        for entry in response.question:
            print(entry)
        print("\nANSWER SECTION: ")
        for entry in response.answer:
            print(entry)
        print("\nQuery Time: ",(end-start)*1000,"ms")
        print("When: ",stime)

    

except Exception as e:
    if root<len(rootservers):
        root=root+1
    else:
        print(e)