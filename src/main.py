from simulator import Simulator

partner_id = '04A66CE7327C6E21493DA6F3B9AACC75'
strategy = 'random'

if __name__ == "__main__":
    simulator = Simulator(partner_id, strategy)
    simulator.run_simulation()
