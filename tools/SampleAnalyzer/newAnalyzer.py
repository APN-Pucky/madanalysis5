#!/usr/bin/env python

################################################################################
#  
#  Copyright (C) 2012-2013 Eric Conte, Benjamin Fuks
#  The MadAnalysis development team, email: <ma5team@iphc.cnrs.fr>
#  
#  This file is part of MadAnalysis 5.
#  Official website: <https://launchpad.net/madanalysis5>
#  
#  MadAnalysis 5 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  MadAnalysis 5 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with MadAnalysis 5. If not, see <http://www.gnu.org/licenses/>
#  
################################################################################


import os
import sys
import shutil

class AnalyzerManager:
    
    def __init__(self,name,title):
        self.name       = name
        self.title      = title
        self.currentdir = os.getcwd()

    def CheckFilePresence(self):
        if not os.path.isdir(self.currentdir + "/Analyzer"):
            print "Error: the directory called 'Analyzer' is not found."
            return False
        if os.path.isfile(self.currentdir + "/Analyzer/" + self.name + ".cpp"):
            print "Error: a file called 'Analyzer/"+self.name+\
                     ".cpp' is already defined."
            print "Please remove this file before."
            return False
        if os.path.isfile(self.currentdir + "/Analyzer/" + self.name + ".h"):
            print "Error: a file called 'Analyzer/"+self.name+\
                     ".h' is already defined."
            print "Please remove this file before."
            return False
        return True

    def AddAnalyzer(self):
        # creating the file from scratch
        if not os.path.isfile(self.currentdir + "/Analyzer/analysisList.h"):
            output = open(self.currentdir + "/Analyzer/analysisList.h","w")
            path = os.path.normpath(self.name+".h")
            output.write('#include "SampleAnalyzer/User/Analyzer/'+path+'"\n')
            output.write('#include "SampleAnalyzer/Process/Analyzer/AnalyzerManager.h"\n')
            output.write('#include "SampleAnalyzer/Commons/Service/LogStream.h"\n')
            output.write('\n')
            output.write('// -----------------------------------------------------------------------------\n')
            output.write('// BuildTable\n')
            output.write('// -----------------------------------------------------------------------------\n')
            output.write('void BuildUserTable(MA5::AnalyzerManager& manager)\n')
            output.write('{\n')
            output.write('  using namespace MA5;\n')
            output.write('  manager.Add("'+self.title+'",new '+self.name+");\n")
            output.write('}\n')
            output.close()

        # updating the file 
        else:
            shutil.copy(self.currentdir + "/Analyzer/analysisList.h",
                        self.currentdir + "/Analyzer/analysisList.bak")
            output = open(self.currentdir + "/Analyzer/analysisList.h","w")
            input  = open(self.currentdir + "/Analyzer/analysisList.bak")

            path = os.path.normpath(self.name+".h")
            output.write('#include "SampleAnalyzer/User/Analyzer/'+path+'"\n')

            for line in input:

                theline = line.lstrip()
                theline = theline.split()
                tit = self.title.replace(' ','_')
                for word in theline:
                    if word=="}":
                        output.write('  manager.Add("'+self.title+'",new '+self.name+');\n')
                        continue
                
                output.write(line)

            input.close()
            output.close()

    def WriteHeader(self):
        
        file = open(self.currentdir + "/Analyzer/" + self.name + ".h","w")
        file.write('#ifndef analysis_'+self.name+'_h\n')
        file.write('#define analysis_'+self.name+'_h\n\n')
        file.write('#include "SampleAnalyzer/Process/Analyzer/AnalyzerBase.h"\n\n')
        file.write('namespace MA5\n')
        file.write('{\n')
        file.write('class '+self.name+' : public AnalyzerBase\n')
        file.write('{\n')
        file.write('  INIT_ANALYSIS('+self.name+',"'+self.title+'")\n\n')
        file.write(' public:\n')
        file.write('  virtual bool Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters);\n')
        file.write('  virtual void Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files);\n')
        file.write('  virtual void Execute(SampleFormat& sample, const EventFormat& event);\n\n')
        file.write(' private:\n')
        file.write('};\n')
        file.write('}\n\n')
        file.write('#endif')
        file.close()
    def WriteSource(self):
        
        file = open(self.currentdir + "/Analyzer/" + self.name + ".cpp","w")
        file.write('#include "Analyzer/'+self.name+'.h"\n')
        file.write('using namespace MA5;\n')
        file.write('using namespace std;\n')
        file.write('\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('// Initialize\n')
        file.write('// function called one time at the beginning of the analysis\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('bool '+self.name+'::Initialize(const MA5::Configuration& cfg, const std::map<std::string,std::string>& parameters)\n')
        file.write('{\n')
        file.write('  cout << "BEGIN Initialization" << endl;\n')
        file.write('  // initialize variables, histos\n')
        file.write('  cout << "END   Initialization" << endl;\n')
        file.write('  return true;\n')
        file.write('}\n')
        file.write('\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('// Finalize\n')
        file.write('// function called one time at the end of the analysis\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('void '+self.name+'::Finalize(const SampleFormat& summary, const std::vector<SampleFormat>& files)\n')
        file.write('{\n')
        file.write('  cout << "BEGIN Finalization" << endl;\n')
        file.write('  // saving histos\n')
        file.write('  cout << "END   Finalization" << endl;\n')
        file.write('}\n')
        file.write('\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('// Execute\n')
        file.write('// function called each time one event is read\n')
        file.write('// -----------------------------------------------------------------------------\n')
        file.write('void '+self.name+'::Execute(SampleFormat& sample, const EventFormat& event)\n')
        file.write('{\n')
        file.write('  // ***************************************************************************\n')
        file.write('  // Example of analysis with generated particles\n')
        file.write('  // Concerned samples : LHE/STDHEP/HEPMC\n')
        file.write('  // ***************************************************************************\n')
        file.write('  /*\n')
        file.write('  if (event.mc()!=0)\n')
        file.write('  {\n')
        file.write('    cout << "---------------NEW EVENT-------------------" << endl;\n')
        file.write('\n')
        file.write('    // Initial state\n')
        file.write('    for (unsigned int i=0;i<event.mc()->particles().size();i++)\n')
        file.write('    {\n')
        file.write('      const MCParticleFormat& part = event.mc()->particles()[i];\n')
        file.write('\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "MC particle" << endl;\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('\n')
        file.write('      // display index particle\n')
        file.write('      cout << "index=" << i+1;\n')
        file.write('\n')
        file.write('      // display the status code\n')
        file.write('      cout << "Status Code=" << part.statuscode() << endl;\n')
        file.write('      if (PHYSICS->IsInitialState(part)) cout << " (Initial state) ";\n')
        file.write('      else if (PHYSICS->IsFinalState(part)) cout << " (Intermediate state) ";\n')
        file.write('      else cout << " (Final state) ";\n')
        file.write('      cout << endl;\n')
        file.write('\n')
        file.write('      // pdgid\n')
        file.write('      cout << "pdg id=" << part.pdgid() << endl;\n')
        file.write('      if (PHYSICS->IsInvisible(part)) cout << " (invisible particle) ";\n')
        file.write('      else cout << " (visible particle) ";\n')
        file.write('      cout << endl;\n')
        file.write('\n')
        file.write('      // display kinematics information\n')
        file.write('      cout << "px=" << part.px()\n')
        file.write('                << " py=" << part.py()\n')
        file.write('                << " pz=" << part.pz()\n')
        file.write('                << " e="  << part.e()\n')
        file.write('                << " m="  << part.m() << endl;\n')
        file.write('      cout << "pt=" << part.pt() \n')
        file.write('                << " eta=" << part.eta() \n')
        file.write('                << " phi=" << part.phi() << endl;\n')
        file.write('\n')
        file.write('      // display particle mother id\n')
        file.write('      if (part.mother1()==0) \n')
        file.write('      {\n')
        file.write('        cout << "particle with no mother." << endl;\n')
        file.write('      }\n')
        file.write('      else if (part.mother2()==0 || part.mother1()==part.mother2())\n')
        file.write('      {\n')
        file.write('        const MCParticleFormat* mother = part.mother1();\n')
        file.write('        cout << "particle coming from the decay of " \n')
        file.write('             << mother->pdgid() << "." << endl;\n')
        file.write('      }\n')
        file.write('      else\n')
        file.write('      {\n')
        file.write('        const MCParticleFormat* mother1 = part.mother1();\n')
        file.write('        const MCParticleFormat* mother2 = part.mother2();\n')
        file.write('        cout << "particle coming from interaction between "\n')
        file.write('             << mother1->pdgid() << " and " << mother2->pdgid()\n')
        file.write('             << "." << endl;\n')
        file.write('      }\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    // Transverse missing energy (MET)\n')
        file.write('    cout << "MET pt=" << event.mc()->MET().pt()\n')
        file.write('         << " phi=" << event.mc()->MET().phi() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Transverse missing hadronic energy (MHT)\n')
        file.write('    cout << "MHT pt=" << event.mc()->MHT().pt()\n')
        file.write('              << " phi=" << event.mc()->MHT().phi() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Total transverse energy (TET)\n')
        file.write('    cout << "TET=" << event.mc()->TET() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Total transverse hadronic energy (THT)\n')
        file.write('    cout << "THT=" << event.mc()->THT() << endl; \n')
        file.write('   cout << endl;\n')
        file.write('\n')
        file.write('  }\n')
        file.write('  */\n')
        file.write('\n\n')
        file.write('  // ***************************************************************************\n')
        file.write('  // Example of analysis with reconstructed objects\n')
        file.write('  // Concerned samples : \n')
        file.write('  //   - LHCO samples\n')
        file.write('  //   - LHE/STDHEP/HEPMC samples after applying jet-clustering algorithm\n')
        file.write('  // ***************************************************************************\n')
        file.write('  /*\n')
        file.write('  if (event.rec()!=0)\n')
        file.write('  {\n')
        file.write('    cout << "---------------NEW EVENT-------------------" << endl;\n')
        file.write('\n')
        file.write('    // Looking through the reconstructed electron collection\n')
        file.write('    for (unsigned int i=0;i<event.rec()->electrons().size();i++)\n')
        file.write('    {\n')
        file.write('      const RecLeptonFormat& elec = event.rec()->electrons()[i];\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "Electron" << endl;\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "index=" << i+1 \n')
        file.write('                << " charge=" << elec.charge() << endl;\n')
        file.write('      cout << "px=" << elec.px()\n')
        file.write('                << " py=" << elec.py()\n')
        file.write('                << " pz=" << elec.pz()\n')
        file.write('                << " e="  << elec.e()\n')
        file.write('                << " m="  << elec.m() << endl;\n')
        file.write('      cout << "pt=" << elec.pt() \n')
        file.write('                << " eta=" << elec.eta() \n')
        file.write('                << " phi=" << elec.phi() << endl;\n')
        file.write('      cout << "pointer address to the matching MC particle: " \n')
        file.write('                << elec.mc() << endl;\n')
        file.write('      cout << endl;\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    // Looking through the reconstructed muon collection\n')
        file.write('    for (unsigned int i=0;i<event.rec()->muons().size();i++)\n')
        file.write('    {\n')
        file.write('      const RecLeptonFormat& mu = event.rec()->muons()[i];\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "Muon" << endl;\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "index=" << i+1 \n')
        file.write('                << " charge=" << mu.charge() << endl;\n')
        file.write('      cout << "px=" << mu.px()\n')
        file.write('                << " py=" << mu.py()\n')
        file.write('                << " pz=" << mu.pz()\n')
        file.write('                << " e="  << mu.e()\n')
        file.write('                << " m="  << mu.m() << endl;\n')
        file.write('      cout << "pt=" << mu.pt() \n')
        file.write('                << " eta=" << mu.eta() \n')
        file.write('                << " phi=" << mu.phi() << endl;\n')
        file.write('      cout << "ET/PT isolation criterion =" << mu.ET_PT_isol() << endl;\n')
        file.write('      cout << "pointer address to the matching MC particle: " \n')
        file.write('           << mu.mc() << endl;\n')
        file.write('      cout << endl;\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    // Looking through the reconstructed hadronic tau collection\n')
        file.write('    for (unsigned int i=0;i<event.rec()->taus().size();i++)\n')
        file.write('    {\n')
        file.write('      const RecTauFormat& tau = event.rec()->taus()[i];\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "Tau" << endl;\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "tau: index=" << i+1 \n')
        file.write('                << " charge=" << tau.charge() << endl;\n')
        file.write('      cout << "px=" << tau.px()\n')
        file.write('                << " py=" << tau.py()\n')
        file.write('                << " pz=" << tau.pz()\n')
        file.write('                << " e="  << tau.e()\n')
        file.write('                << " m="  << tau.m() << endl;\n')
        file.write('      cout << "pt=" << tau.pt() \n')
        file.write('                << " eta=" << tau.eta() \n')
        file.write('                << " phi=" << tau.phi() << endl;\n')
        file.write('      cout << "pointer address to the matching MC particle: " \n')
        file.write('           << tau.mc() << endl;\n')
        file.write('      cout << endl;\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    // Looking through the reconstructed jet collection\n')
        file.write('    for (unsigned int i=0;i<event.rec()->jets().size();i++)\n')
        file.write('    {\n')
        file.write('      const RecJetFormat& jet = event.rec()->jets()[i];\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "Jet" << endl;\n')
        file.write('      cout << "----------------------------------" << endl;\n')
        file.write('      cout << "jet: index=" << i+1 \n')
        file.write('           << " charge=" << jet.charge() << endl;\n')
        file.write('      cout << "px=" << jet.px()\n')
        file.write('           << " py=" << jet.py()\n')
        file.write('           << " pz=" << jet.pz()\n')
        file.write('           << " e="  << jet.e()\n')
        file.write('           << " m="  << jet.m() << endl;\n')
        file.write('      cout << "pt=" << jet.pt() \n')
        file.write('           << " eta=" << jet.eta() \n')
        file.write('           << " phi=" << jet.phi() << endl;\n')
        file.write('      cout << "b-tag=" << jet.btag()\n')
        file.write('           << " true b-tag (before eventual efficiency)=" \n')
        file.write('           << jet.true_btag() << endl;\n')
        file.write('      cout << "EE/HE=" << jet.EEoverHE()\n')
        file.write('           << " ntracks=" << jet.ntracks() << endl;\n')
        file.write('      cout << endl;\n')
        file.write('    }\n')
        file.write('\n')
        file.write('    // Transverse missing energy (MET)\n')
        file.write('    cout << "MET pt=" << event.rec()->MET().pt()\n')
        file.write('         << " phi=" << event.rec()->MET().phi() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Transverse missing hadronic energy (MHT)\n')
        file.write('    cout << "MHT pt=" << event.rec()->MHT().pt()\n')
        file.write('              << " phi=" << event.rec()->MHT().phi() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Total transverse energy (TET)\n')
        file.write('    cout << "TET=" << event.rec()->TET() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('\n')
        file.write('    // Total transverse hadronic energy (THT)\n')
        file.write('    cout << "THT=" << event.rec()->THT() << endl;\n')
        file.write('    cout << endl;\n')
        file.write('  }\n')
        file.write('  */\n')
        file.write('}\n')
        file.write('\n')
        file.close()

    def UpdateMain(self,title):
        if not os.path.isfile(self.currentdir + "/../Main/main.cpp"):
          return;
        else:
          shutil.copy(self.currentdir + "/../Main/main.cpp",
             self.currentdir + "/../Main/main.bak")
          output = open(self.currentdir + "/../Main/main.cpp","w")
          input  = open(self.currentdir + "/../Main/main.bak")
          IsExecuted=False
          for line in input:
            if "Getting pointer to the analyzer" in line:
              output.write(line)
              TheName = title.replace(' ','_');
              TheName = title.replace('-','_');
              output.write("  std::map<std::string, std::string> prm" + TheName + ";\n")
              output.write("  AnalyzerBase* analyzer_" + TheName + "=\n")
              output.write("    manager.InitializeAnalyzer(\"" + TheName + "\",\"" +\
                 title + ".saf\",prm" + TheName + ");\n")
              output.write("  if (analyzer_" + TheName + "==0) return 1;\n\n")
            elif "Execute" in line and not IsExecuted:
              IsExecuted = True
              output.write("      analyzer_" + TheName + "->Execute(mySample,myEvent);\n")
              output.write(line)
            else:
              output.write(line)



# Reading arguments
mute=False
if len(sys.argv)==3:
    mute=True
elif len(sys.argv)!=2:
    print "Error: number of argument incorrect"
    print "Syntax: ./newAnalyzer.py name"
    print "with name the name of the analyzer"
    sys.exit()


print "A new class called '" + sys.argv[1] + "' will be created."
if not mute:
  print "Please enter a title for your analyzer : "
  title=raw_input("Title : ")
else:
  title=sys.argv[1]

analyzer = AnalyzerManager(sys.argv[1],title)

# Checking presence of required files
if not analyzer.CheckFilePresence():
    sys.exit()

analyzer.UpdateMain(title)
analyzer.WriteHeader()
analyzer.WriteSource()

# Adding analysis in analysisList.h
analyzer.AddAnalyzer()

print "Done !"



