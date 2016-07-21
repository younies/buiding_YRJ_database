#!/usr/bin/python
"""
this program is going to call every thing and build the data base and taking only as argument how long of the kmers that you want
"""
import os
import sys
import subprocess
import re


##some configuration variables:



path_to_the_program = "/export1/project/hondius/newKrakenResearch/"
path_to_the_place_of_the_database = "/export1/project/hondius/newKrakenResearch/databases/"
name_of_genomes_database = "genomesDatabase"
path_for_converting_yjr = "/export/project/hondius/newProject/NewTaxonomer/convert_kmerFasta_to_yrj.out"
kmer_databaseName = "" #setted in the program
kmer = -1 #will be set later



def getTheSizeOfFile(path):
	commad = ["wc" , "-l" , path]
	runComm = subprocess.Popen(commad ,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out ,err = runComm.communicate()
	if not err:
		size = re.findall(r'[0-9][0-9]*' , out)
		size = size[0]
		size = int(size)
		return size
	else:
		print "the command to get the size for " + path + "failed :("
		return False


def osRunningCommand(commad , message = "process"):
	err = os.system(commad)
	if not err:
		print " the " + message + " ..... succeded"
		return True
	else:
		print "the " + message + " ..... fialed"
		return False


def subProRunning(commadList , message = "process  " ):
	runComm = subprocess.Popen(commadList , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out , err = runComm.communicate()
	if not err:
		print "all the data base built ...... succeed"
		return True
	else:
		print err
		print "failed to build all the database"
		return False









def osRunForName(name):
	"""
	taking a name like 1094.fa and produce the 1098.jf file and then .yjr file
	"""
	global path_to_the_place_of_the_database
	global path_to_the_program , name_of_genomes_database, path_for_converting_yjr, kmer_databaseName
	global kmer

	uid = name[:-3]
	path_to_the_database = path_to_the_place_of_the_database + '/' + kmer_databaseName + '/'

	name_in_genomesDB = path_to_the_program + name_of_genomes_database + "/" + name
	name_in_kmerDB = path_to_the_place_of_the_database + kmer_databaseName + "/" + name[:-3] + '.jf'

	commadList = ["jellyfish" , "count", '-m' , str(kmer) , '-s' , '100M' , '-C' , '-o']
	commadList.append(name_in_kmerDB)
	commadList.append(name_in_genomesDB)
	subProRunning(commadList , "for the uid: " + name)

	##now bulding the fastafile from the jf
	name_fasta_in_kmerDB = name_in_kmerDB[:-3] + ".fa"
	commad = "jellyfish dump " + name_in_kmerDB + "  > " + name_fasta_in_kmerDB
	osRunningCommand(commad , "building the fasta for uid" + name)

	##for removing the jf file
	commadRemove = "rm " + name_in_kmerDB
	osRunningCommand(commadRemove , "remove the jf of uid: " + name)

	##for building the yjr file
	command_yjrList = [path_for_converting_yjr]
	command_yjrList.append(path_to_the_database)
	command_yjrList.append(uid)
	command_yjrList.append(str(getTheSizeOfFile(path_to_the_database + uid + '.fa')))
	command_yjrList.append(str(kmer))
	subProRunning(command_yjrList , "building the yrj for the " + name)

	##remove the fasta file
	commandRemoceFasta = "rm " + path_to_the_database + uid + '.fa'
	osRunningCommand(commandRemoceFasta , "removing the fasta kmer of " + name)

	##return
	return True









if len(sys.argv) < 2:
	print "Usage: ./program_name <number of the kmers>"
	exit()
else:
	kmer = int(sys.argv[1])
	kmer_databaseName = 'kmerDatabase' + str(kmer)



##make the kmer database directory

make_directory = subprocess.Popen(['mkdir', path_to_the_place_of_the_database + kmer_databaseName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out , err = make_directory.communicate()

if not err:
	print "making the directory for the kmer database done!"
else:
	print err
	print "failed to build the kmer directory!"



## to get the names of all the fasta files in the database
namesOrder =  subprocess.Popen(['ls' , path_to_the_program + name_of_genomes_database  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

names , err = namesOrder.communicate()
names = names.split('\n')


if not err:
	print "getting the names succeded !"
else:
	print err
	print "failed to get the names"


full_names = []
for name in names:
	name = path_to_the_program + name_of_genomes_database + '/' + name
	full_names.append(name)


print full_names[0]
##for building all the data base

all_database_name = path_to_the_place_of_the_database + kmer_databaseName + '/all.jf'

building_all = subprocess.Popen(['jellyfish', 'count' , '-m' , str(kmer) , '-s' , '10000M' , '-C' , '-o' , all_database_name ] + full_names, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out , err = building_all.communicate()
if not err:
	print "all the data base built ...... succeed"
else:
	print err
	print "failed to build all the database"
	exit()




## building the kmers for the database

name_of_fasta_all = path_to_the_place_of_the_database + kmer_databaseName + '/all.fa'

print all_database_name
print name_of_fasta_all

#building_all_fasta = subprocess.Popen(['jellyfish', 'dump' , all_database_name , '>' , name_of_fasta_all], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

err = os.system( "jellyfish dump " + all_database_name + " > " + name_of_fasta_all)
#out , err = building_all_fasta.communicate()
if not err:
	print "fasta for akmers is buit ..... done!"
else:
	print err
	print "failed to build the all kmers fasta file"

##remove the jf file for all database
removeAllCommand = "rm " + all_database_name
osRunningCommand(removeAllCommand , "removing all jf from the disk")


### build the yrj for the database
commandYJR_for_all = [path_for_converting_yjr ,path_to_the_place_of_the_database + kmer_databaseName +'/', 'all'  ]
commandYJR_for_all.append(str(getTheSizeOfFile(name_of_fasta_all) ))
commandYJR_for_all.append(str(kmer))
subProRunning( commandYJR_for_all , "building yjr for all")


##remove the fasta all
commandRemoveFastaAll = "rm " + name_of_fasta_all
osRunningCommand(commandRemoveFastaAll , "removing the fasta all")


##for building all the uids

for name in names:
	osRunForName(name)










