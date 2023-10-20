##########################################################
### Import Necessary Modules #############################

import argparse                       #provides options at the command line
import sys                            #take command line arguments and uses it in the script
import gzip                           #allows gzipped files to be read
import re                             #allows regular expressions to be used

##########################################################
### Command-line Arguments ###############################

parser = argparse.ArgumentParser(description="A script to convert a vcf file to a format used by Relate (R) program to estimate relatedness.")
parser.add_argument("-vcf", help = "The location of the vcf file", default=sys.stdin, required=True)
parser.add_argument("-pop", help = "The location of the population file (IndividualName<tab>IndivdualPopulation per line)", default="NA", required=False)
args = parser.parse_args()

#########################################################
###Variables ############################################

class Variables():
   population = {}
   populations = []
   numIndividuals = 0

#########################################################
### Body of script ######################################

class OpenFile():
    def __init__ (self, f, typ, occ):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r') 
        if typ == "vcf":
            sys.stderr.write("\nOpened vcf file: {}\n".format(occ))
            OpenVcf(self.filename,occ)
        elif typ == "pop":
            sys.stderr.write("\nOpened pop file: {}\n".format(occ))
            OpenPop(self.filename,occ)

class OpenVcf():
    def __init__ (self,f,o):
        """Reads a vcf file to covert to another format"""
        ### IndividualName LociGenotypes (A=1, C=2, G=3, T=4, missing = 0)
        self.numInds = 0
        self.numMarkers = 0
        self.loci = []
        self.genotypes = {}   
        self.individuals = []   
        for self.line in f:
            ### Allows gzipped files to be read ###
            try:
                self.line = self.line.decode('utf-8')
            except:
                pass
            self.line = self.line.rstrip('\n')            
            if not re.search("^#", self.line):
                self.referenceAllele = 4
                self.altAllele = 4
                self.chr, self.pos, self.id, self.ref, self.alt, self.qual, self.filt, self.info, self.fmt = self.line.split()[0:9]
                self.individualGenotypes = self.line.split()[9:]
                self.numMarkers += 1
                #self.locus = "{}_{}".format(self.chr, self.pos)
                #self.loci.append(self.locus)
                for self.position, self.indGeno in enumerate(self.individualGenotypes):
                    self.indName = self.individuals[self.position]
                    self.tmpGeno = "0 0"
                    self.indGeno = self.indGeno.split(":")[0]
                    if self.indGeno == "0/0":
                        self.tmpGeno = "{} {}".format(1, 1)
                    elif self.indGeno == "0/1" or self.indGeno == "1/0":
                        self.tmpGeno = "{} {}".format(1, 2)
                    elif self.indGeno == "1/1":
                        self.tmpGeno = "{} {}".format(2, 2)
                    if self.indName in self.genotypes:
                        self.genotypes[self.indName] += " {}".format(self.tmpGeno)
                    else:
                        self.genotypes[self.indName] = self.tmpGeno
            elif re.search("^#CHROM", self.line):
                self.individuals = self.line.split()[9:]
                self.numInds = len(self.individuals)
                if int(self.numInds)  != int(Variables.numIndividuals):
                    if args.pop != "NA":
                        sys.stderr.write("Warning, population and vcf files have different number of individuals.\n")
        for self.indGenotyped in self.genotypes:
            if args.pop != "NA":
                if self.indGenotyped in Variables.population:
                    print("{}_{} {}".format(Variables.population[self.indGenotyped], self.indGenotyped, self.genotypes[self.indGenotyped]))
                else:
                    sys.stderr.write("Warning, unable to find the population for (not outputting): {}".format(self.indGenotyped))                    
            else:
                print("{} {}".format(self.indGenotyped, self.genotypes[self.indGenotyped]))
        f.close()
        
class OpenPop():
    def __init__ (self,f,o):
        """Reads a population file to identify which individual goes to which population"""
        self.pops = {}
        for self.line in f:
            ### Allows gzipped files to be read ###
            try:
                self.line = self.line.decode('utf-8')
            except:
                pass
            self.line = self.line.rstrip('\n')             
            if not re.search("^#", self.line):
                self.individual, self.pop = self.line.split()
                if self.individual in Variables.population:
                    sys.stderr.write("\tWarning: {} already defined for population {}, replacing with population {}\n\n".format(self.individual, Variables.population[self.individual], self.pop))
                Variables.population[self.individual] = self.pop
                if self.pop in self.pops:
                    self.pops[self.pop] += 1
                else:
                    self.pops[self.pop] = 1
                Variables.numIndividuals += 1
        for self.pop in sorted(self.pops):
            Variables.populations.append(self.pop)
            sys.stderr.write("\tIdentified population {} with {} samples\n".format(self.pop, self.pops[self.pop]))
        f.close()

### Order of script ####
if __name__ == '__main__':
    Variables()
    if args.pop != "NA":
        open_aln = OpenFile(args.pop, "pop", args.pop)
    open_aln = OpenFile(args.vcf, "vcf", args.vcf)
