from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import DataForm
import requests
from .models import Chain, Block, Transactions, b2c, b2t

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

def index(request):
    if (request.method == 'POST'): 
        form = DataForm(request.POST)
        if (form.is_valid()):
            new_data = form.save(commit=True)   #Replica of data being sent
            context = {
                'temp' : new_data.temp_sensor,
                'hum' : new_data.humidity_sensor,
                'vib' : new_data.vibration_sensor,
            }
            post_object = { 
                'temp' : new_data.temp_sensor,
                'hum' : new_data.humidity_sensor,
                'vib' : new_data.vibration_sensor,
            }

            # Submit a transaction
            new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
            #Sending data to server but we dont know where will server send that data further
            requests.post(new_tx_address,
                        json=post_object,
                        headers={'Content-type': 'application/json'})

            return render(request,'main/result.html', context=context)
        else :
            form = DataForm()
            context = {
                'form' : form,
            }
            return render(request, 'main/index.html', context=context)
    else :
        form = DataForm()
        context = {
            'form' : form,
        }
        return render(request, 'main/index.html', context=context)

def mine(request) :
    mine_address = "{}/mine".format(CONNECTED_NODE_ADDRESS)
    chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    r = requests.get(mine_address)
    if (str(r) == '<Response [200]>'):
        chain = requests.get(chain_address)
        chain_dict = chain.json()
        chain_obj = get_object_or_404(Chain,name='IOT_Chain')
        if (int(chain_dict['length'])!=int(chain_obj.length)):
            
            ch_d = chain_dict['chain']
            for i in range (int(chain_obj.length),int(chain_dict['length'])):
                for j in ch_d :
                    block = Block()
                    block.time_stamp = j['timestamp']
                    block.previous_hash = j['previous_hash']
                    block.hash_num = j['hash']
                    block.nonce = j['nonce']
                    block.index = j['index']
                    block.save()
                    for k in j['transactions'] :
                        transaction = Transactions()
                        transaction.temp_sensor = k['temp']
                        transaction.humidity_sensor = k['hum']
                        transaction.vibration_sensor = k['vib']
                        transaction.time_stamp = k['timestamp']
                        transaction.save()
                        bt = b2t()
                        bt.block = block
                        bt.transaction = transaction
                        bt.save()
                    bc = b2c()
                    bc.block = block
                    bc.chain = chain_obj
                    bc.save()
        chain_obj.length = chain_dict['length']
        chain_obj.save()
        form = DataForm()
        context = {
            'form' : form,
        }
        return HttpResponseRedirect("/")
        
