import os
import json
import time
from create_requirements import generate_requirements_txt, read_solution_file
from dependency import fetch_direct_dependencies, fetch_transitive_dependencies
from requirements import parse_requirements
from smt import generate_smt_expression, smt_solver
from z3 import Context


def read_requirements(directory):

    with open(os.path.join(directory, "requirements.txt"), "r") as file:
        return file.read()


def read_json_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def process_folder(directory, projects_data):
    # Log file setup
    dir = "D:/Windsor/WindsorThesis/Git repo/Thesis-Project-Python-Dependency-Conflict-Resolution/Result"
    log_file = os.path.join(dir, "watchman_execution_log.txt")
    # log_file = os.path.join(dir, 'gist_execution_log.txt')
    # Ensure the output directory exists
    os.makedirs(directory, exist_ok=True)

    def log_execution_time(action_name, start_time, end_time):
        with open(log_file, "a") as file:
            file.write(
                f"{action_name} execution time: {end_time - start_time} seconds\n"
            )

    def log_error(action_name, error_message):
        with open(log_file, "a") as file:
            file.write(f"{action_name} error: {error_message}\n")

    try:
        # Read files from the directory
        start_time = time.time()
        requirements_txt = read_requirements(directory)
        end_time = time.time()
        # Log the filename being processed
        log_execution_time(f"Processing file: {directory}", start_time, end_time)
        log_execution_time("Reading requirements file", start_time, end_time)

        # Parse requirements
        start_time = time.time()
        requirements = parse_requirements(requirements_txt)
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
        solver, constraints = generate_smt_expression(
            direct_dependencies, transitive_dependencies, ctx, add_soft_clauses=False
        )
        end_time = time.time()
        log_execution_time("Generating SMT expression", start_time, end_time)

        # Save SMT expression to a file (optional)
        smt_expression_file_path = os.path.join(directory, "SMT_expression.txt")
        with open(smt_expression_file_path, "w") as file:
            file.write(str(solver))

        # Solve the SMT expression
        solution, proof, start_time, end_time = smt_solver(solver, ctx)
        if solution:  # Check if a solution was found before logging and printing
            log_execution_time("Solving SMT expression", start_time, end_time)
            print(f"Optimal Solution: {solution}")
            # Save string solution to a file
            string_solution_file_path = os.path.join(directory, "string_solution.txt")
            with open(string_solution_file_path, "w") as file:
                file.write(str(solution))
                # Generate requirements_txt
            solution_dict = read_solution_file(string_solution_file_path)

            start_time = time.time()
            # Define the path for the requirements.txt file
            requirements_file_path = os.path.join(directory, "solution.txt")
            # Generate requirements.txt
            generate_requirements_txt(
                solution_dict, requirements_file_path
            )  # Need to add arg directory
            end_time = time.time()
            log_execution_time("Generating requirements.txt", start_time, end_time)
        else:
            # print(proof)
            # Save proof to a file
            start_time = time.time()
            proof_file_path = os.path.join(directory, "proof.txt")
            with open(proof_file_path, "w") as file:
                file.write(str(proof))
            end_time = time.time()
            log_execution_time("Proof for UNSAT", start_time, end_time)

    except Exception as e:
        log_error("Processing folder", str(e))
        print(f"Error processing folder {directory}: {e}")
