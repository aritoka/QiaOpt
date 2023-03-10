""" Defines the run"""
import os
# import glob
# import shutil
import pandas as pd
from qcg.pilotjob.api.manager import LocalManager
from qcg.pilotjob.api.job import Jobs
from qiaopt.pre import Experiment


def create_points(parameters):
    """
    Creates a list of points based on the given parameters.

    Parameters:
    -----------
    parameters: list
        List of parameters used to create new points.

    Returns:
    --------
    list
        List of new points created based on the given parameters.
    """
    return [3, 4, 5]


def qcgpilot_commandline(experiment):
    """
     Creates a command line for the QCG-PilotJob executor based on the experiment configuration.

     Parameters:
     -----------
     experiment: Experiment
         The experiment to configure the command line for.

     Returns:
     --------
     list
         A list of strings representing the command line arguments for the QCG-PilotJob executor.
     """
    cmdline = [experiment.system_setup.program_name]
    for key, value in experiment.system_setup.cmdline_arguments.items():
        cmdline.append(key)
        cmdline.append(str(value))
    return cmdline


# def getfiles2(directory, extension):
#     all_filenames = [i for i in glob.glob('{}.{}'.format(directory, extension))]


def getfiles(directory, extension):
    """
    Returns a list of files in the given directory with the specified extension.

    Parameters:
    -----------
    directory: str
        The directory to search for files in.
    extension: str
        The file extension to search for.

    Returns:
    --------
    list
        A list of files in the given directory with the specified extension.
    """
    # todo : this collects before all jobs are done in the test
    return [file for file in os.listdir(directory) if file.endswith(extension)]


def files_to_list(files):
    """
    Reads CSV files and returns their contents as a list of dataframes.

    Parameters:
    -----------
    files: list
        A list of CSV files to read.

    Returns:
    --------
    list
        A list of pandas dataframes, each representing the contents of a CSV file.
    """
    # todo check if extension is csv?
    return [pd.read_csv(file, delim_whitespace=True) for file in files]


def set_basic_directory_structure_for_job(experiment: Experiment, step_number: int, job_number: int) -> None:
    """
    Creates a new directory for the given step number and updates the experiment's working directory accordingly.

    The basic directory structure is as follows
    source_dir
        - output_dir
            - step_{i}
                analysis_script.py
                analysis_output.csv
                - job_{j}
                    output_of_your_script.extension
                    stdout{j}.txt

    Parameters
    ----------
    experiment : Experiment
        The :obj:Experiment that is being run.
    step_number : int
        The number of the current step.
    job_number : int
        The number of the current job.
    """
    source_dir = experiment.system_setup.source_directory
    output_dir = experiment.system_setup.output_directory
    new_working_dir = os.path.join(source_dir, output_dir, f'step{step_number}', f'job{job_number}')

    if not os.path.exists:
        os.makedirs(new_working_dir)

    experiment.system_setup.working_directory = new_working_dir

# TODO: old and maybe no longer needed
# def move_output_to_output_directory(self):
#     output_dir = self.experiment.system_setup.output_directory
#     files_list = getfiles(directory=output_dir, extension=self.experiment.system_setup.output_extension)
#     for file in files_list:
#         shutil.move(file, output_dir)
#
#
# def move_stdout_to_log_dir(self):
#     def is_stdout_file(file, basename):
#         return os.path.basename(file).endswith('txt') and os.path.basename(file).startswith(basename)
#     file_list = [file for file in os.listdir(self.experiment.system_setup.source_directory)
#                  if is_stdout_file(file, self.experiment.system_setup.stdout_basename)]
#     for file in file_list:
#         shutil.move(file, log_dir)


class Core:
    """
    Defines the default run function for the executor.

    Parameters:
    -----------
    experiment: Experiment
        The experiment to run.
    """

    def __init__(self, experiment):
        self.experiment = experiment

    def run(self):
        """ Submits jobs to the LocalManager, collects the output, creates new data points, and finishes the run."""
        print("Starting default run: submit, collect, create")
        self.submit()
        directory = self.experiment.system_setup.source_directory
        data = self.collect_data(directory)
        self.create_points_based_on_method(data)
        print("Finished run")

    def submit(self):
        """
        Submits jobs to the LocalManager.

        Returns:
        --------
        list
            A list of job IDs submitted to the LocalManager.
        """
        manager = LocalManager()
        stdout = self.experiment.system_setup.stdout_basename

        jobs = Jobs()
        for i, item in enumerate(self.experiment.data_points):
            set_basic_directory_structure_for_job(experiment=self.experiment, step_number=0, job_number=i)
            jobs.add(
                name=self.experiment.name + str(i),
                exec=self.experiment.system_setup.executor,
                args=qcgpilot_commandline(self.experiment),
                stdout=stdout + str(i) + ".txt",
                wd=self.experiment.system_setup.working_directory,
            )
        job_ids = manager.submit(jobs)
        manager.wait4(job_ids)
        manager.finish()
        manager.cleanup()
        return job_ids

    def collect_data(self, directory):
        """
        Collects data from output files in the given directory.

        Parameters
        ----------
        directory : str
            Path to the directory containing the output files.

        Returns
        -------
        list
            A list of pandas dataframes, each containing the data from an output file.

        """
        directory = self.experiment.system_setup.source_directory
        extension = self.experiment.system_setup.output_extension
        files = getfiles(directory, extension)
        # filesextension = getfiles2(directory,extension)
        data = files_to_list(files)
        return data

    @staticmethod
    def create_points_based_on_method(data):
        """
        Applies a method to process the collected data and create new data points.

        Parameters
        ----------
        data : list
            A list of pandas dataframes containing the collected data.

        Returns
        -------
        list
            A list of new data points created based on the input data.

        """
        # do something with data
        new_points = data
        return new_points


class Executor(Core):
    def run(self):
        pass
