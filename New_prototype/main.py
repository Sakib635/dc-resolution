import os
import time
from z3 import Context
from create_requirements import generate_requirements_txt, read_solution_file
from dependency import fetch_direct_dependencies, fetch_transitive_dependencies
from read import read_json_file, read_requirements
from requirements import parse_requirements
from smt import generate_smt_expression, smt_solver


def main():
    """
    Main function to execute the dependency resolution process, including reading files,
    parsing requirements, fetching dependencies, generating SMT expressions, and solving them.
    """
    directory = "C:/Users/sakib51/Documents/dc-resolution/Dataset"

    # Log file setup
    log_file = "execution_log.txt"

    def log_execution_time(action_name, start_time, end_time):
        """
        Log the execution time of a specific action to a log file.

        Args:
        action_name (str): The name of the action being logged.m
        start_time (float): The start time of the action.
        end_time (float): The end time of the action.
        """
        with open(os.path.join(directory, log_file), "a") as file:
            file.write(
                f"{action_name} execution time: {end_time - start_time} seconds\n"
            )

    # Read files from the directory
    start_time = time.time()
    requirements_txt = read_requirements(directory)
    projects_data = read_json_file(directory)
    end_time = time.time()
    log_execution_time("Reading files", start_time, end_time)

    # Parse requirements
    start_time = time.time()
    requirements = parse_requirements(requirements_txt)
    # assert parse_requirements("python-sat>=3.1") == ("python-sat", [(">=", 3.1)])
    end_time = time.time()
    log_execution_time("Parsing requirements", start_time, end_time)
    print("Parsed requirements:", requirements)

    # Fetch matching versions and their dependencies
    start_time = time.time()
    direct_dependencies = fetch_direct_dependencies(requirements, projects_data)
    end_time = time.time()
    log_execution_time("Fetching versions and dependencies", start_time, end_time)
    # print("Direct dependencies:", direct_dependencies)

    # Fetch transitive dependencies
    start_time = time.time()
    transitive_dependencies = fetch_transitive_dependencies(
        direct_dependencies, projects_data
    )
    end_time = time.time()
    log_execution_time("Fetching transitive dependencies", start_time, end_time)
    # print("Transitive dependencies:", transitive_dependencies)

    # Generate SMT expression
    start_time = time.time()
    ctx = Context()
    solver = generate_smt_expression(
        direct_dependencies, transitive_dependencies, ctx, add_soft_clauses=True
    )
    end_time = time.time()
    log_execution_time("Generating SMT expression", start_time, end_time)

    # Save SMT expression to a file (optional)
    with open(os.path.join(directory, "SMT_expression.txt"), "w") as file:
        file.write(str(solver))

    # Solve the SMT expression
    solution, proof, start_time, end_time = smt_solver(solver, ctx)
    if solution:  # Check if a solution was found before logging and printing
        log_execution_time("Solving SMT expression", start_time, end_time)
        # print(f"Optimal Solution: {solution}")
        with open(os.path.join(directory, "string_solution.txt"), "w") as file:
            file.write(str(solution))
            # Generate requirements_txt
        solution_dict = read_solution_file(
            "C:/Users/sakib51/Documents/dc-resolution/Dataset/string_solution.txt"
        )
        start_time = time.time()
        generate_requirements_txt(solution_dict, directory, "solution.txt")
        end_time = time.time()
        log_execution_time("Generating requirements.txt", start_time, end_time)
        print("solved")
    else:
        print(proof)
        # Save SMT expression to a file (optional)
        with open(os.path.join(directory, "proof.txt"), "w") as file:
            file.write(proof)


if __name__ == "__main__":
    main()
