from simulator import Simulator


partner_id = 'C0F515F0A2D0A5D9F854008BA76EB537'  # partner_id for plotting
# partner_id = '04A66CE7327C6E21493DA6F3B9AACC75'  # partner_id for logs

strategy = 'random'

if __name__ == "__main__":
    simulator = Simulator(partner_id, strategy)
    simulator.run_simulation()
