import subprocess
import platform
import json
from dotmap import DotMap

char = "bustedgun"
realm = "hyjal"
region = "us"
calculate_scale_factors = 1
html = "john.html"
armory = f'{region},{realm},{char}'


class SimC:
    def __init__(self, bot, simc_path):
        self.bot = bot
        self.simc = simc_path
        if platform.system() == "Windows":
            self.simc += ".exe"
        self.data = DotMap()

    def run_sim(self,
                armory,
                calculate_scale_factors,
                html="resutls.html",
                json="results.json"):

        sim = subprocess.check_output([
            f"{self.simc}", f"armory={armory}",
            f"calculate_scale_factors={calculate_scale_factors}",
            f"html={html}", f"json2={json}"
        ])
        json_data = open("results.json").read()
        self.data = DotMap(json.loads(json_data))
        return sim

    def get_PAWN_String(self):
        sim = self.data
        scale_factors = sim.sim.players[0].scale_factors
        player = sim.sim.players[0]
        player_info = {
            "name": player["name"],
            "spec": player["specialization"].split()[0],
            "class": player["specialization"].split()[1]
        }
        first = True
        PAWN_String = f'Pawn: v1: "{player_info["name"]}-{player_info["spec"]}" '
        for key, val in scale_factors.items():
            temp = f"{key}={val}"
            if first:
                PAWN_String += temp
                first = False
            else:
                PAWN_String += ", " + temp

        return PAWN_String


main = SimC("bot", "C:\Simulationcraft(x64)\801-01\simc")

#main.run_sim(armory, 1)
json_data = open("results.json").read()
sim = DotMap(json.loads(json_data))
scale_factors = sim.sim.players[0].scale_factors
player = sim.sim.players[0]
player_info = {
    "name": player["name"],
    "spec": player["specialization"].split()[0],
    "class": player["specialization"].split()[1]
}
print(scale_factors)
print(player_info)
print(main.get_PAWN_String())