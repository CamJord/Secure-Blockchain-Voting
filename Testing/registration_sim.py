"""
A test of the voter registration system by simulating possible registrants.
"""
from time import sleep
import random
import sys
import queue
from voter_db import VoterDB
from registrar import registrar
from blockchain import Blockchain
from Testing.threads import ThreadWithReturnValue

ATTEMPTS = 40
VALID_VOTERS = 20


# helper methods
def sim_reg():
    # init
    sleep(1)
    blockchain = Blockchain()
    database = VoterDB()
    blockchain.add_candidate('recipient 1')
    blockchain.add_candidate('recipient 2')
    blockchain.add_candidate('recipient 3')
    # redirect stdout
    buf = ""
    # simulate 100 attempts to register/vote
    for i in range(ATTEMPTS):
        v_id = random.randrange(1, VALID_VOTERS)
        buf += "\n--------------------------------------------------------------\n" + \
               "Attempt for ID: " + str(v_id) + \
               "\n--------------------------------------------------------------"
        private_key, public_key, msg = registrar(v_id, database)
        buf += "\n" + msg
        buf += "\nPrivate Key (Usually only shown to voter): " + str(private_key)
        buf += "\nPublic Key: " + str(public_key)
        # If registration is succesful
        if not private_key:
            buf += "\nDon't Vote"
        else:
            rec_num = random.randrange(1,5)
            buf += "\nAttempting to vote for recipient " + str(rec_num)
            blockchain.create_transaction(public_key, 'recipient '+str(rec_num), 1)
            trans = blockchain.last_transaction
            buf += "\nSender: " + trans.sender
            buf += "\nRecipient: " + trans.sender

    sleep(1)
    return buf

def animate(process):

    while process.is_alive():
        chars = "⢿⣻⣽⣾⣷⣯⣟⡿"
        for char in chars:
            sys.stdout.write('\r' + 'loading ' + char)
            sleep(.1)
            sys.stdout.flush()
    sys.stdout.write('\rFinished!     ')


print("""
This is a simulation of multiple users attempting to register and vote.\n\
-------------------------------------------------------------------------------\n\
Please comment out the Sim() function as designated in Main for actual use.\n\n\
As the valid voters are randomized, entering the same ID more than once may\n\
result in a user being \"valid\" one time and not another. Use in conjunction with\n\
an actual verification system to avoid this issue.
""")
print("\n")
# Wait for Enter key to be pressed
input("Press Enter to continue...")

# Loading animation during process
que = queue.Queue()

t = ThreadWithReturnValue(target=sim_reg, args=())
t.start()
animate(t)

print("\n")
# Wait for Enter key to be pressed
input("Press Enter to see results...")
print(t.join())

