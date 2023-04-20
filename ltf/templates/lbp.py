## Run test with notebook lbp-test.ipynb
## Reference Docs:--
## Spreadsheet: https://docs.google.com/spreadsheets/d/11b7MRe1HfAc7l3tCTd9snlrLrtmeAECR/edit#gid=745957496
## Smart Contract: https://etherscan.io/address/0x751A0bC0e3f75b38e01Cf25bFCE7fF36DE1C87DE#code
## OCtopus HAckmd: https://hackmd.io/@AndrewPenland/BkSq-5A8t
## Flashswaps: https://dev.balancer.fi/resources/swaps/flash-swaps
import hvplot.pandas
import holoviews as hv
import panel as pn
import pandas as pd
import numpy as np
import param as pm
import random
import math
import plotly.express as px
pn.extension(sizing_mode="stretch_width")
hv.extension("bokeh")
pn.extension('plotly')

class LBP(pm.Parameterized):
    """[summary]

    Args:
        pm ([type]): [description]
    """
    ## SMART Pool Parameters
    sale_duration  = pm.Number(default=3, bounds=(0, 30), step = 0.5, label='Sale Duration (days)')
    sale_rate = pm.Number(default=1280000, bounds=(0, 10000000), step = 100, label='Sale Rate (TKNs/day)')
    avg_sec_per_block = pm.Number(default = 13.5, bounds=(0, 60), step = 0.5, label='Avg Time Per Block (seconds)')
    steps = pm.Number(default = 72, bounds=(0, 100), step = 1, label='Steps')
    swap_fee = pm.Number(default = 0.15, bounds=(0, 10), step = 0.01, label='Swap Fee (in percent)')
    lot_size = pm.Number(default = 10000, bounds=(0, 100000), step = 10, label='Lot Size (in TKN)')
    ## token amt and weight
    initial_tkn = pm.Number(default = 7500000, bounds=(0, 10000000), step = 10, label='Initial TKN Supply')
    initial_dai = pm.Number(default = 1333333, bounds=(0, 10000000), step = 10, label='Initial DAI Supply')
    tkn_start_weight = pm.Number(default = 99, bounds=(0, 100), step = 1, label='TKN Start Weight')
    dai_start_weight = pm.Number(default = 1, bounds=(0, 100), step = 1, label='DAI Start Weight')
    tkn_end_weight = pm.Number(default = 30, bounds=(0, 100), step = 1, label='TKN End Weight')
    dai_end_weight = pm.Number(default = 70, bounds=(0, 100), step = 1, label='DAI End Weight')
    max_price = pm.Number(default = 10000, bounds=(0, 100000), step = 100, label='Max Price (TKN/DAI)')
    millnames = ['',' Thousand',' Million',' Billion',' Trillion']
    
    def millify(self,n):
        n = float(n)
        millidx = max(0,min(len(self.millnames)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.2f}{}'.format(n / 10**(3 * millidx), self.millnames[millidx])

    def calc_simulation_params(self):
        """
        Calculates the simulation parameters
        """
        steps = []
        hours = []
        blocks = []
        tkn_weight = []
        dai_weight = []
        tkn_balance = []
        slippage = []
        tkn_price = []
        dai_balance = []
        for i in range(0, self.steps+1):
            step = i
            hour = i * ((self.sale_duration*24)/self.steps)
            block = hour * (3600/self.avg_sec_per_block)
            tkn_w = self.tkn_start_weight - (i/self.steps) * (self.tkn_start_weight - self.tkn_end_weight)
            dai_w = self.dai_start_weight - (i/self.steps) * (self.dai_start_weight - self.dai_end_weight)
            
            tkn_bal = self.initial_tkn - ((i *(self.sale_rate/24))*(self.sale_duration*24/self.steps))
            if tkn_bal < 0:
                tkn_bal = 0
                break
            
            if i==0:
                dai_bal = self.initial_dai
                tkn_p = dai_bal * ((tkn_bal/(tkn_bal-self.lot_size))**((tkn_w/dai_w))-1) / ((1 - self.swap_fee*0.01)* self.lot_size)
            else:
                dai_bal = dai_balance[-1] + (tkn_price[-1] * (tkn_balance[-1]-tkn_bal))
                tkn_p = dai_bal * ((tkn_bal/(tkn_bal-self.lot_size))**((tkn_w/dai_w))-1) / ((1 - self.swap_fee*0.01)* self.lot_size)
            
            slipp = (1-self.swap_fee*0.01) / (2*tkn_w*tkn_bal*0.01) * self.lot_size * 100


            steps.append(step)
            hours.append(hour)
            blocks.append(block)
            tkn_weight.append(tkn_w)
            dai_weight.append(dai_w) 
            tkn_balance.append(tkn_bal)
            slippage.append(slipp)
            tkn_price.append(tkn_p)
            dai_balance.append(dai_bal)
            
        df = pd.DataFrame(
            {
                'Step':steps,
                'Hours':hours,
                'Blocks':blocks,
                'TKN Weight':tkn_weight,
                'DAI Weight':dai_weight,
                'TKN Price':tkn_price,
                'TKN Balance':tkn_balance,
                'DAI Balance':dai_balance,
                'Slippage%':slippage,
                }
                )
        return df

    def view_sim_results(self, df):
        ##plot 1
        fig = px.line(df, 
              x='Step', 
              y=['TKN Price', 'TKN Weight', 'DAI Weight'],
              labels={
                  "variable": "Params",
                  "value": "Value"
              },
              title='Simulation Results'
                     )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                )
            )
        fig.update_traces(mode="lines", hovertemplate=None)
        fig.update_layout(hovermode="x")
        
        ##fig2
        fig2 = px.line(df, 
              x='Step', 
              y=['TKN Balance', 'DAI Balance'],
              labels={
                  "variable": "Params",
                  "value": "USD"
              },
              title='Simulation Results'
                     )
        fig2.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                )
            )
        fig2.update_traces(mode="lines", hovertemplate=None)
        fig2.update_layout(hovermode="x")
        
        p1 = pn.Tabs(
            ('Weight & Price', fig),
            ('Balance', fig2),
            ('Table',df.hvplot.table()),
        )
        return p1

    def show_outputs(self):
        """
        Returns derived parameters
        """
        df = self.calc_simulation_params()
        sale_duration_hours = self.sale_duration * 24
        sale_duration_blocks = sale_duration_hours * (3600/self.avg_sec_per_block)
        sale_rate_hourly = round(self.sale_rate/24,2)
        proceeds = round(df['DAI Balance'].iloc[-1] - df['DAI Balance'].iloc[0])
        unsold_tokens = round(df['TKN Balance'].iloc[-1])
        
        ##initialize pool
        p1 = self.view_sim_results(df)
        p2 = pn.Column(
            pn.Row('sale duration hours', sale_duration_hours, 'sale duration blocks', sale_duration_blocks),
            # pn.Row('sale rate hourly', sale_rate_hourly),
            pn.Row('unsold tokens', self.millify(unsold_tokens)),
            pn.Row('proceeds', self.millify(proceeds)),
        )

        return pn.Column(p2, p1)


    def view(self):
        """
        Returns the view of the model
        """

        p1 = pn.Row(
                pn.Column('##Smart Pool Inputs',
                    self.param.sale_duration,
                    self.param.sale_rate,
                    self.param.avg_sec_per_block,
                    self.param.steps,
                    self.param.swap_fee,
                    self.param.lot_size,
                    self.param.initial_tkn,
                    self.param.initial_dai,
                    pn.Row(
                        pn.Column(
                            self.param.tkn_start_weight,
                            self.param.dai_start_weight
                            ),
                        pn.Column(
                            self.param.tkn_end_weight,
                            self.param.dai_end_weight
                            ),
                    ),
                ),
                pn.Column('## Results',
                    self.show_outputs,
                ),
            )

        return p1