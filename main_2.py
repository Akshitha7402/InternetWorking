import random
import time

# Define the network parameters
pAllocationSlotMin = 500  # microseconds
pAllocationSlotResolution = 500  # microseconds
SymbolRate = 600  # kilosymbols per second
Npreamble = 90  # bits
Sheader = 1
Nheader = 31  # bits
UPppduBits = 512  # bits
ACKppduBits = 40  # bits
pSIFS = 192  # microseconds
nSlot = 255  # maximum number of slots in the superframe
nSlot_BAN1 = 100
nSlot_BAN2 = 200
nSlot_BAN3 = 150
nSlot_BAN4 = 120
nSlot_BAN5 = 180

Tslot_BAN1 = 0.010
Tslot_BAN2 = 0.015
Tslot_BAN3 = 0.012
Tslot_BAN4 = 0.011
Tslot_BAN5 = 0.013


# Define the functions to calculate the superframe parameters
def calculate_Tslot(L):
    return (
        pAllocationSlotMin + L * pAllocationSlotResolution
    ) / 1000000  # convert to seconds


def calculate_L(Tslot):
    return int(
        (Tslot - pAllocationSlotMin / 1000000) / (pAllocationSlotResolution / 1000000)
    )


def calculate_Tpkt():
    return (Npreamble + Sheader * Nheader + UPppduBits / 2) / (
        SymbolRate * 1000
    )  # convert to seconds


def calculate_TpktAck():
    return (Npreamble + Sheader * Nheader + ACKppduBits / 2) / (
        SymbolRate * 1000
    )  # convert to seconds


def calculate_EstimatedTime():
    Tpkt = calculate_Tpkt()
    TpktAck = calculate_TpktAck()
    return 2 * pSIFS / 1000000 + TpktAck + Tpkt + pSIFS / 1000000


def listen_B2():
    # Simulate B2 channel listening with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print("Cluster head finished listening on B2 channel.")


def send_response_frame(L, nSlot, EstimatedTime):
    # Simulate sending response frame with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print(
        f"Cluster head finished sending response frame with L={L}, nSlot={nSlot}, EstimatedTime={EstimatedTime:.6f} seconds."
    )


def listen_response_frame():
    # Simulate listening for response frame with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print("Cluster head finished listening for response frame.")


def listen_beacon():
    # Simulate listening for beacon with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print("Member node finished listening for beacon.")


def send_request_frame(Tpkt):
    # Simulate sending request frame with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print(f"Member node finished sending request frame with Tpkt={Tpkt:.6f} seconds.")


def PhaseReceivedpkts():
    # Simulate receiving packets with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    # TODO: Implement receiving packets


def superframe_interleaving(head_ban, coexistence):
    if head_ban:
        if coexistence:
            # Cluster head listens on B2 and sends response frame
            print("Cluster head listening on B2 channel...")
            listen_B2()
            L = calculate_L(
                Tslot_BAN1
            )  # assume BAN1 is the first member of the cluster
            nSlot = max(nSlot_BAN1, nSlot_BAN2, nSlot_BAN3, nSlot_BAN4, nSlot_BAN5)
            Tslot = calculate_Tslot(L)
            EstimatedTime = calculate_EstimatedTime()
            print(
                f"Cluster head sending response frame with L={L}, nSlot={nSlot}, EstimatedTime={EstimatedTime:.6f} seconds..."
            )
            send_response_frame(L, nSlot, EstimatedTime)
        else:
            # Cluster head listens for response frame and sends its own response frame
            print("Cluster head listening for response frame...")
            listen_response_frame()
            L = calculate_L(Tslot_BAN5)  # assume BAN5 is the cluster head
            nSlot = max(nSlot_BAN1, nSlot_BAN2, nSlot_BAN3, nSlot_BAN4, nSlot_BAN5)
            Tslot = calculate_Tslot(L)
            EstimatedTime = calculate_EstimatedTime()
            print(
                f"Cluster head sending response frame with L={L}, nSlot={nSlot}, EstimatedTime={EstimatedTime:.6f} seconds"
            )
            send_response_frame(L, nSlot, EstimatedTime)
    else:
        if coexistence:
            # Member node listens for beacon and sends request frame
            print("Member node listening for beacon...")
            listen_beacon()
            Tpkt = calculate_Tpkt()
            print("Member node sending request frame...")
            send_request_frame(Tpkt)
        else:
            # Member node listens for response frame
            print("Member node listening for response frame...")
            listen_response_frame()

    if not head_ban and not coexistence:
        # Member node sends ACK frame and receives packets
        print("Member node sending ACK frame...")
        send_ack_frame()
        PhaseReceivedpkts()


def send_ack_frame():
    # Simulate sending ACK frame with random delay
    delay = random.uniform(0, 50)  # delay in microseconds
    time.sleep(delay / 1000000)  # convert delay to seconds
    print("Member node finished sending ACK frame.")


# Run the simulation for all possible cases
print("Starting simulation...")

# Case 1: Cluster head, coexistence
print("\nCase 1: Cluster head, coexistence")
superframe_interleaving(True, True)

# Case 2: Cluster head, no coexistence
print("\nCase 2: Cluster head, no coexistence")
superframe_interleaving(True, False)

# Case 3: Member node, coexistence
print("\nCase 3: Member node, coexistence")
superframe_interleaving(False, True)

# Case 4: Member node, no coexistence
print("\nCase 4: Member node, no coexistence")
superframe_interleaving(False, False)

print("\nSimulation complete.")
