from tqdm import tqdm
import time
from colorama import Fore, Back, Style, init

init()

def running_process():
    time.sleep(0.1)

def progress_check(checker, msg):
    # Define a list of items to process
    items = list(range(checker))

    # Initialize a tqdm progress bar with colored output
    with tqdm(total=len(items), desc=f"Validating {msg} config", bar_format="{desc}: {percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} [{postfix}]", ncols=100) as pbar:
        # Process each item and update the progress bar
        for item in items:
            running_process()
            pbar.update(1)
            # Change the color of the progress bar based on the progress
            if pbar.n <= len(items) * 0.5:
                pbar.set_postfix_str(Fore.MAGENTA + "Scanning..." + Style.RESET_ALL)
            elif pbar.n <= len(items) * 0.8:
                pbar.set_postfix_str(Fore.YELLOW + "Scanning..." + Style.RESET_ALL)
            elif pbar.n == len(items) * 1:
                pbar.set_postfix_str(Fore.GREEN + "Done" + Style.RESET_ALL)
