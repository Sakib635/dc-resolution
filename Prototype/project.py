import os
import json
import re
from z3 import Solver, Bool, Or, And, Implies, sat, Int, String, Not, Real

# Function to read the requirements.txt file from a directory
def read_requirements(directory):
    with open(os.path.join(directory, 'r.txt'), 'r') as file:
        return file.read()

# Function to read the JSON file from a directory
def read_json_file(directory, filename='Test_KG.json'):
    with open(os.path.join(directory, filename), 'r') as file:
        return json.load(file)

# Function to parse the requirements.txt content
def parse_requirements(requirements_txt):
    requirements = {}
    lines = requirements_txt.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            if '==' in line:
                package, version = line.split('==')
                requirements[package.strip()] = ('==', version.strip())
            elif '>=' in line:
                package, version = line.split('>=')
                requirements[package.strip()] = ('>=', version.strip())
            elif '<=' in line:
                package, version = line.split('<=')
                requirements[package.strip()] = ('<=', version.strip())
            elif '>' in line:
                package, version = line.split('>')
                requirements[package.strip()] = ('>', version.strip())
            elif '<' in line:
                package, version = line.split('<')
                requirements[package.strip()] = ('<', version.strip())
            elif '!=' in line:
                package, version = line.split('!=')
                requirements[package.strip()] = ('!=', version.strip())
    return requirements

# Function to fetch versions according to constraints
def fetch_versions(requirements, projects_data):
    matching_versions = {}
    for package, (operator, version_constraint) in requirements.items():
        if package in projects_data['projects']:
            available_versions = projects_data['projects'][package].keys()
            if operator == '==':
                pattern = re.compile(f'^{version_constraint.replace("*", ".*")}$')
                matching_versions[package] = [v for v in available_versions if pattern.match(v)]
            elif operator == '>=':
                matching_versions[package] = [v for v in available_versions if v >= version_constraint]
            elif operator == '<=':
                matching_versions[package] = [v for v in available_versions if v <= version_constraint]
            elif operator == '>':
                matching_versions[package] = [v for v in available_versions if v > version_constraint]
            elif operator == '<':
                matching_versions[package] = [v for v in available_versions if v < version_constraint]
            elif operator == '!=':
                matching_versions[package] = [v for v in available_versions if v != version_constraint]
    return matching_versions

# Function to fetch dependencies for a specific version of a package
def fetch_dependencies(package, version, projects_data):
    dependencies = projects_data['projects'][package][version].get('dependency_packages', [])
    if dependencies is None:
        dependencies = []
    return dependencies

# Function to recursively fetch versions and their dependencies
def fetch_versions_and_dependencies(requirements, projects_data, visited=None):
    if visited is None:
        visited = set()
    direct_dependencies = fetch_versions(requirements, projects_data)
    transitive_dependencies = {}

    for package, versions in list(direct_dependencies.items()):  # Use list to create a copy for iteration
        for version in versions:
            if (package, version) not in visited:
                visited.add((package, version))
                dependencies = fetch_dependencies(package, version, projects_data)
                if dependencies:  # Only proceed if there are dependencies
                    dependency_requirements = parse_requirements_from_list(dependencies)
                    if dependency_requirements:
                        dep_direct, dep_transitive = fetch_versions_and_dependencies(dependency_requirements, projects_data, visited)
                        transitive_dependencies[f"{package}=={version}"] = dep_direct
                        transitive_dependencies.update(dep_transitive)

    return direct_dependencies, transitive_dependencies

# Function to parse requirements from a list of dependencies
def parse_requirements_from_list(dependencies):
    requirements = {}
    for dependency in dependencies:
        if '==' in dependency:
            package, version = dependency.split('==')
            requirements[package.strip()] = ('==', version.strip())
        elif '>=' in dependency:
            package, version = dependency.split('>=')
            requirements[package.strip()] = ('>=', version.strip())
        elif '<=' in dependency:
            package, version = dependency.split('<=')
            requirements[package.strip()] = ('<=', version.strip())
        elif '>' in dependency:
            package, version = dependency.split('>')
            requirements[package.strip()] = ('>', version.strip())
        elif '<' in dependency:
            package, version = dependency.split('<')
            requirements[package.strip()] = ('<', version.strip())
        elif '!=' in dependency:
            package, version = dependency.split('!=')
            requirements[package.strip()] = ('!=', version.strip())
    return requirements


#Generate the CNF Formate
def generate_smt_expression(direct_dependencies, transitive_dependencies):
    constraints = []

    # Generate constraints for direct dependencies
    for package, versions in direct_dependencies.items():
        if isinstance(versions, list):
            package_constraint = Or([String(package) == v for v in versions])
            constraints.append(package_constraint)

    # Generate constraints for transitive dependencies
    for package_version, dependencies in transitive_dependencies.items():
        if isinstance(dependencies, dict):
            package, version = package_version.split('==')
            dependency_constraint = Or([String(dep_package) == dep_version for dep_package, dep_versions in dependencies.items() for dep_version in dep_versions])
            constraints.append(Or(Not(String(package) == version), dependency_constraint))

    # Combine all constraints
    final_constraint = And(constraints)
    return final_constraint

def smt_solver(smt_expression):
    # Define the variables
    variables = {}
    # Create the solver
    solver = Solver()
    # Add the expression to the solver
    solver.add(smt_expression)
    solutions = []
    while solver.check() == sat:
        model = solver.model()
        solution = {d.name(): model[d].as_string() for d in model.decls()}
        solutions.append(solution)

        # Create a constraint to block the current model
        block = []
        for d in model.decls():
            c = d()
            block.append(c != model[d])
        solver.add(Or(block))

    return solutions

#Optimize for the latest version: Identify the latest version that satisfies all constraints.
def get_latest_version(solutions):
    latest_solution = None

    if not solutions:
        return latest_solution

    # Initialize the latest_solution with the first solution
    latest_solution = solutions[0]

    for solution in solutions:
        for key in solution.keys():
            current_version = solution[key].split('.')
            latest_version = latest_solution[key].split('.')

            # Pad shorter version numbers with zeros for fair comparison
            while len(current_version) < len(latest_version):
                current_version.append('0')
            while len(latest_version) < len(current_version):
                latest_version.append('0')

            if current_version > latest_version:
                latest_solution = solution
                break
            elif current_version < latest_version:
                break

    return latest_solution



def main():
    directory = 'D:\Windsor\Windsor Thesis\Git repo\Thesis-Project-Python-Dependency-Conflict-Resolution\Prototype\Demo data'

    # Read files from the directory
    requirements_txt = read_requirements(directory)
    projects_data = read_json_file(directory)

    # Parse requirements
    requirements = parse_requirements(requirements_txt)
    print("Parsed requirements:", requirements)

    # Fetch matching versions and their dependencies
    direct_dependencies, transitive_dependencies = fetch_versions_and_dependencies(requirements, projects_data)
    print("Direct dependencies:", direct_dependencies)
    print("Transitive dependencies:", transitive_dependencies)

    # Generate SMT expression
    smt_expression = generate_smt_expression(direct_dependencies, transitive_dependencies)
    print("SMT Expression:", smt_expression)

    # Solve the SMT expression
    solution = smt_solver(smt_expression)
    print(f'Possible Solutions: {solution}')

    # Get the latest version solution
    latest_version_solution = get_latest_version(solution)
    print(f'Latest Solution: {latest_version_solution}')

if __name__ == "__main__":
    main()