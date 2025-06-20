import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("epidemic_data_30days.csv")

def estimate_rates(data):
    beta_s_list,beta_a_list,gamma_list,delta_list,sigma_list=[],[],[],[],[]

    for i in range(1,len(data)):
        prev=data.iloc[i-1]
        curr=data.iloc[i]

        S_prev,E_prev=prev['S'],prev['E']
        Ia_prev,Is_prev=prev['Ia'],prev['Is']
        I_prev=Ia_prev+Is_prev
        N=S_prev+E_prev+I_prev+prev['R']+prev['V']

        if S_prev>0 and I_prev>0:
            delta_E=curr['E']-E_prev
            beta=(delta_E*N)/(S_prev*I_prev)
            beta_s_list.append(beta*0.6)
            beta_a_list.append(beta*0.4)

        if Is_prev>0:
            gamma_list.append((curr['R']-prev['R'])/Is_prev)
            delta_list.append((curr['D']-prev['D'])/Is_prev)

        if E_prev>0:
            sigma_list.append(((curr['Ia']+curr['Is'])-(prev['Ia']+prev['Is']))/E_prev)

    return(
        np.mean(beta_s_list),np.mean(beta_a_list),
        np.mean(gamma_list),np.mean(delta_list),
        np.mean(sigma_list)
    )

beta_s,beta_a,gamma,delta,sigma=estimate_rates(df)

hospital_capacity=100
reduced_gamma=gamma*0.5
vacc_rate=0.01
reinfection_days=60
birth_rate=0.001
natural_death_rate=0.0005

state=df.iloc[-1].copy().to_dict()
N=sum([state[k] for k in ['S','E','Ia','Is','R','V']])
state['day_since_recovery']={}
day=int(state['day'])+1
history=[]
prev_state=None

while (state['Is']+state['E']+state['Ia'])>0 and \
      (state['S']+state['E']+state['Ia']+state['Is']+state['R']+state['V'])>0 and day<500:

    new_vacc=min(vacc_rate*state['S'],state['S'])
    state['S']-=new_vacc
    state['V']+=new_vacc

    new_infectious=sigma*state['E']
    new_Ia=0.4*new_infectious
    new_Is=0.6*new_infectious
    state['E']-=new_infectious
    state['Ia']+=new_Ia
    state['Is']+=new_Is

    infection_pressure=(beta_a*state['Ia']+beta_s*state['Is'])/N
    infection_pressure=min(infection_pressure,1.0)
    new_E=np.random.binomial(int(state['S']),infection_pressure)
    state['S']-=new_E
    state['E']+=new_E

    current_gamma=reduced_gamma if state['Is']>hospital_capacity else gamma
    new_R_sym=current_gamma*state['Is']
    new_D=delta*state['Is']
    state['Is']-=(new_R_sym + new_D)
    state['R']+=new_R_sym
    state['D']+=new_D

    new_R_asym=gamma*state['Ia']
    state['Ia']-=new_R_asym
    state['R']+=new_R_asym

    reinfect_keys=[]
    for d_rec,count in state['day_since_recovery'].items():
        if day-int(d_rec)>=reinfection_days:
            state['S']+=count
            state['R']-=count
            reinfect_keys.append(d_rec)
    for k in reinfect_keys:
        del state['day_since_recovery'][k]
    state['day_since_recovery'][str(day)]=new_R_sym+new_R_asym

    state['S']+=birth_rate*N
    for comp in ['S','E','Ia','Is','R','V']:
        d_nat=natural_death_rate*state[comp]
        state[comp]-=d_nat
        state['D']+=d_nat

    today={
        'day':day,
        'S':round(state['S']),
        'E':round(state['E']),
        'Ia':round(state['Ia']),
        'Is':round(state['Is']),
        'R':round(state['R']),
        'V':round(state['V']),
        'D':round(state['D'])
    }
    history.append(today)

    if prev_state is not None:
        print(f"Day {day}: S={today['S']}, E={today['E']}, Ia={today['Ia']}, Is={today['Is']}, R={today['R']}, V={today['V']}, D={today['D']}")
    prev_state=today.copy()

    day+=1

sim_df=pd.DataFrame(history)
plt.figure(figsize=(12, 6))
for col in ['S','E','Ia','Is','R','V','D']:
    plt.plot(sim_df['day'],sim_df[col],label=col)
plt.title("Epidemic Simulation (Auto-Estimated Rates)")
plt.xlabel("Day")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()