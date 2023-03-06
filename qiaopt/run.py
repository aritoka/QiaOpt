""" Defines the run"""
import csv
import os
import pandas as pd
from qiaopt.pre import Experiment
from qcg.pilotjob.api.manager import LocalManager
from qcg.pilotjob.api.job import Jobs


def createpoints(parameters):
	return [3,4,5]

def qcgpilot_commandline(experiment):
	cmdline = []
	cmdline.append(experiment.system_setup.program_name)
	for key, value in experiment.system_setup.cmdline_arguments.items():
		cmdline.append(key)
		cmdline.append(str(value))
	return cmdline


def getfiles2(directory, extension):
    all_filenames = [i for i in glob.glob('{}.{}'.format(directory,extension))]

def getfiles(directory, extension):  
    dir_path = directory
    files = []
    for file in os.listdir(dir_path):
        if file.endswith(extension):
        	files.append(file)
    return files

def filestolist(files):
	data = []
	print(files)
	for file in files:
		#if extension == "csv":
		filedata = pd.read_csv(file)
		data.append(filedata)
	return data

class Core:
	"""Defines the default run function for the executor
	Parameters
	----------
	experiment : Experiment
		Experiment to run.
	"""
	def __init__(self, experiment):
		self.experiment = experiment

	def run(self):
		print("Starting default run: submit, collect, create")
		self.submit()
		self.collectdata() 
		self.create_points_based_on_method()

	def submit(self):
		manager = LocalManager()
		#extension = self.experiment.extension
		#directory = self.experiment.directory
		extension = "csv"
		directory = os.getcwd()
		stdout = "output"
		
		jobs = Jobs()
		for i, item in enumerate(self.experiment.data_points):
			jobs.add(
				name = self.experiment.name + str(i), 
				#exec = self.experiment.executor,
				exec = "python3",
                args = qcgpilot_commandline(self.experiment),  
				#stdout = self.experiment.stdout + str(i) + "." + extension,
				stdout = stdout + str(i) + "." + extension,
				wd = directory,
			)
		job_ids = manager.submit(jobs)
		manager.wait4(job_ids)
		manager.cleanup()
		manager.finish()
		return job_ids


	def collectdata(self):
		extension = "csv"
		directory = os.getcwd()
		#directory = self.experiment.system_setup.directory
		#extension = self.experiment.extension
		files = getfiles(directory,extension)
		#filesextension = getfiles2(directory,extension)
		data = filestolist(files)
		return data

	def create_points_based_on_method(self):
		#call optimization(experiments)
		parameters = [5,5,5]
		return parameters


class Executor(Core):
	def run():
		pass
