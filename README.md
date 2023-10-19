# VCF2Relate
A script to convert a VCF file to a format used by the R program Relate

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script have been tested with Python 3.
The script requires the following file(s).
    
Files:<br /><br />
&nbsp;&nbsp;&nbsp;A vcf file (can be compressed)<br />
&nbsp;&nbsp;&nbsp;(Optional) A population file (not tested).  Format: individual(tab)population (two letter for population based on Relate documentation)

<!-- usage -->
## Usage

1) Convert vcf file to format used by Relate:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;python VCF2Relate.v1.0.py -vcf File.vcf.gz > Output.relate.txt
    
<!-- license -->
## License 

Distributed under the MIT License.
