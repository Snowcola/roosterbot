import subprocess


char = "bustedgun"
realm = "hyjal"
region = "us"
calculate_scale_factors=1
html="john.html"
armory = f'{region},{realm},{char}'

class SimC:
    def __init__(self, bot):
        self.bot = bot

    def run_sim(armory, calculate_scale_factors, html=None)
        sim = subprocess.check_output(["/Applications/SimC/simc",
                                        f"armory={armory}", 
                                        f"calculate_scale_factors={calculate_scale_factors}", 
                                        f"html={html}"
                                        ]) 
        return sim

    

