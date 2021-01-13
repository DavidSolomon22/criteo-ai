from simulator import Simulator

partner_id = 'C0F515F0A2D0A5D9F854008BA76EB537'
strategy = 'random'

if __name__ == "__main__":
    simulator = Simulator(partner_id, strategy)
    simulator.run_simulation()
