#!/usr/bin/env python
# coding: utf-8

# In[ ]:


alpha_inputs = [
    {
        'type': 'REGULAR',
        'settings': {
            'instrumentType': 'EQUITY',
            'region': 'USA',
            'universe': 'TOP3000',
            'delay': 1,
            'decay': 4,
            'neutralization': 'SUBINDUSTRY',
            'truncation': 0.01,
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'OFF',
            'language': 'FASTEXPR',
            'visualization': False,
        },
        'regular': 'rank(0 - (1 * ((close - vwap) / ts_decay_linear(rank(ts_arg_max(close, 5)), 1))))'
    },
    # Add more sets of alpha simulation settings here if needed
]

alpha_list = []


# In[ ]:


for alpha_input in alpha_inputs:
    simulation_response = s.post('https://api.worldquantbrain.com/simulations', json=alpha_input)
    from time import sleep

    simulation_progress_url = simulation_response.headers['Location']
    finished = False
    while True:
        simulation_progress = s.get(simulation_progress_url)
        if simulation_progress.headers.get("Retry-After", 0) == 0:
            break
        print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")
        sleep(float(simulation_progress.headers["Retry-After"]))
    print("Alpha done simulating, getting alpha details")
    alpha_id = simulation_progress.json()["alpha"]
    
    # Get Alpha Details
    alpha = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id)
    alpha_details = alpha.json()
    # Extract specific fields from alpha_details
    alpha_info = {
        'code': alpha_details['regular']['code'],
        'PnL': alpha_details['is']['pnl'],
        'bookSize': alpha_details['is']['bookSize'],
        'neutralization' : alpha_details['settings']['neutralization'],
        'region': alpha_details['settings']['region'],
        'universe': alpha_details['settings']['universe'],
        'decay' : alpha_details['settings']['decay'],
        'delay' : alpha_details['settings']['delay'],
        'sharpe': alpha_details['is']['sharpe'],
        'returns': alpha_details['is']['returns'],
        'drawdown': alpha_details['is']['drawdown'],
        'margin': alpha_details['is']['margin'],
        'fitness': alpha_details['is']['fitness'],
        'turnover': alpha_details['is']['turnover'],
        'IS_ladder_sharpe' : alpha_details['name']
    }

    # Print the alpha details
    print("Alpha:", alpha_info['code'])
    print("PnL:", alpha_info['PnL'])
    print("Book Size:", alpha_info['bookSize'])
    print("Sharpe:", alpha_info['sharpe'])
    print("Fitness:", alpha_info['fitness'])
    print("Turnover:", alpha_info['turnover'])
    print("Neutral:", alpha_info['neutralization'])
    print("Decay:", alpha_info['decay'])
    print("Delay:", alpha_info['delay'])
    print("Region:", alpha_info['region'])
    print("Region:", alpha_info['region'])
    print("Universe:", alpha_info['universe'])
    
    is_ladder_sharpe_check = next(
        (check for check in alpha_details['is']['checks'] if check['name'] == 'IS_LADDER_SHARPE'),
        None
    )
    if is_ladder_sharpe_check:
        print("IS_LADDER_SHARPE :", is_ladder_sharpe_check['result'])
    # Append alpha_info to the alpha_list
    alpha_list.append(alpha_info)
    
    # ... (print other details if needed)


# In[ ]:


from time import sleep

finished = False
# Get Profit and Loss (PnL)
while True:
    pnl = s.get("https://api.worldquantbrain.com/alphas/" + alpha_id + "/recordsets/pnl")
    if pnl.headers.get("Retry-After", 0) == 0:
        break
    print("Sleeping for " + pnl.headers["Retry-After"] + " seconds")
    sleep(float(pnl.headers["Retry-After"]))

pnl_data = pnl.json()

# Convert the PnL data to a Pandas DataFrame for easy manipulation
pnl_df = pd.DataFrame(pnl_data['records'], columns=['date', 'pnl'])

# Assuming the 'date' column contains dates in a proper format, you can convert it to a datetime object
pnl_df['date'] = pd.to_datetime(pnl_df['date'])

# Plotting the PnL data
plt.figure(figsize=(8, 4))
plt.plot(pnl_df['date'], pnl_df['pnl'])
plt.xlabel('Date')
plt.ylabel('PnL')
plt.title('Profit and Loss (PnL) Over Time')
plt.grid(True)
plt.show()

