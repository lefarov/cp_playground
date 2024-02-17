import os
import sys
import seaborn
import subprocess
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Setup plotting style
    markers = ["X", "P", "D", "o"]
    seaborn.set_style("darkgrid")
    
    # Evaluate perfromance
    num_workers = [1, 2, 4, 8]
    scripts = ["multiprocessing", "ray", "openmpi"]

    for script, marker in zip(scripts[:1], markers[:1]):
        py_file = os.path.join(os.path.dirname(__file__), f"kmp_{script}.py")
        res = []
        
        for n in num_workers:
            res.append(float(
                subprocess.check_output(
                    f"{sys.executable} {py_file} -n {n}", 
                    stderr=subprocess.STDOUT, 
                    shell=True
                )
            ))

        plt.plot(res, marker=marker, label=script)
    
    plt.xticks(range(len(num_workers)), num_workers)
    plt.xlabel("number of workers")
    plt.ylabel("computation time [s]")
    plt.legend()
    
    plt.savefig("comparison.png")