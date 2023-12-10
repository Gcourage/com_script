import logging
import multiprocessing
import subprocess


def execute_command(command):
    # Set up a logger
    logger = logging.getLogger(f"command-{command}")
    logger.setLevel(logging.DEBUG)

    # Create a handler for logging to a file
    handler = logging.FileHandler(f"command_{command}.log")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    try:
        # Execute the command using subprocess
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Capture the output and error streams
        output, error = process.communicate()

        # Check if the command was successful
        if process.returncode == 0:
            logger.info(f"Command '{command}' executed successfully.")
            logger.debug(output.decode("utf-8"))
        else:
            logger.error(f"Command '{command}' failed with error:")
            logger.debug(error.decode("utf-8"))
    except Exception as e:
        logger.critical(f"Unexpected error occurred during execution of command '{command}'.")
        logger.exception(e)


if __name__ == "__main__":
    # Define the commands to execute
    commands = ["ls", "pwd", "whoami"]

    # Determine the number of available CPU cores
    num_cores = multiprocessing.cpu_count()

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_cores)

    # Execute each command in a separate process
    pool.map(execute_command, commands)

    # Wait for all processes to finish
    pool.close()
    pool.join()

