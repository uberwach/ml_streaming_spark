from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-78806dd4-42a6-11e4-aed8-02ee2ddab7fe"
pnconfig.publish_key = "my_pubkey"
pnconfig.ssl = False

pb = PubNub(pnconfig)

def receive(msg):
    print(msg)
    return True

pb.subscribe({
    'channel' : 'pubnub-twitter',
    'callback' : receive})
