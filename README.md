# README #

The script obtains all information necessary from a bam file and a list of structural variations in order to accurately count variant allele frequencies (VAF) and detect subclones from SV data. 

### How do I get set up? ###

Ensure you have the following dependencies installed:

* [Numpy](http://www.numpy.org/) - install for python 2
* [PySam](http://pysam.readthedocs.org/en/latest/)
* [Pandas](http://pandas.pydata.org/)
* [Pandasql](https://pypi.python.org/pypi/pandasql)
* [sqlite3](https://docs.python.org/2/library/sqlite3.html)
* [ipdb](https://pypi.python.org/pypi/ipdb)
* [ipython](https://pypi.python.org/pypi/ipython)
* [matplotlib] (http://matplotlib.org/)

If you want to run unit tests:

* [nose](https://nose.readthedocs.org/en/latest/)

Install like so:

    python setup.py install

### Pre-processing of SVs ###

Run SV pre-processing on each sample BAM file using:

    python -m phylo_sv.preprocess.cmd -i <svs.txt> -b <indexed bamfile> -hd <header.cfg> -o <output name> -d <average coverage>

#### Required Parameters ####

* -i or --input : structural variants input file. See file formats section for more details.
* -b or --bam : bam file with corresponding index file.
* -o or --out : output base name. Will create processed output file as <name>_svproc.txt, parameters output as <name>_params.txt and database output as <name>.db
* -d or --depth (floating-point value) : average depth of coverage for corresponding BAM file. See the calculating coverage section.

#### Optional Parameters ####

* -hd or --header : config file specifying header columns. If not provided, default column names assumed (see file formats section).
* -sc or --softclip (default = 25) : reads must overlap by this many basepairs to be counted as supporting the break, or being a non-supporting normal read lying across the break.
* -cn or --max_cn (default = 15) : maximum expected copy-number. Will skip any areas with more reads than <depth> * <max_cn>

#### Beyond Advanced Parameters ####

The package also contains a parameters.py file which has the following hard-coded parameters. Modify these with care.
```
tr      = 5    # if soft-clipped by less than these number of bases at this end, is not a "true" soft-clip
window  = 500  # base-pair window considered to the left and right of the break when processing reads
```
#### File Formats ####

The structural variation input file must be in the following tab-separated format:

```
bp1_chr	bp1_pos	bp1_dir	bp2_chr	bp2_pos	bp2_dir	classification
22	18240676	-	22	18232335	-	INV
22	19940482	-	22	19937820	-	INV
22	21383572	+	22	21382745	+	INV
22	21383573	-	22	21382746	-	INV 
```

The column names can be different, but must be specified in the header.cfg file, which looks like:

```
bp1_chr=bp1_chr
bp1_pos=bp1_pos
bp1_dir=bp1_dir
bp2_chr=bp2_chr
bp2_pos=bp2_pos
bp2_dir=bp2_dir
classification=classification
```

The left fields are used by the program (do not change these), the right fields correspond to the equivalent column in the SV text file.

### Running SV VAF clustering ###

Running the flat clustering approach on a single sample (the only currently supported method), can be done like so:

python -m phylo_sv.cmd -s <sample name> -i <sv preprocessing out> -c <battenberg subclones file>  -p <tumour purity> -o <output directory> -r <read length> -v <insert size> -y <ploidy number> -n <number of MCMC runs>

More info:

#### Required Parameters ####

* -s or --samples : sample names, currently only a single sample is supported.
* -i or --input : pre-processed SV output from pre-precessing script.
* -c or --cnvs : Battenberg subclones.txt file containing segmented copy-numbers for patient sample.
* -o or --outdir : output directory to create files.

#### Optional Parameters ####

Note that read length and insert sizes are provided as outputs from the pre-processing script (<out>_params.txt), based on the first 1000 sampled reads in the bam file. 

* -p or --purity (default = 1.0) : tumour purity. A floating point number between 0 - 1 indicating the percentage of tumour cells.
* -r or --readlen (default = 100) : read length in bp. If differs from default, it is essential to set this parameter.
* -v or --insert (default = readlen) : insert size mean in bp (may be floating point number). If differs from read length, is essential to set correctly. Insert size here means fragment_len - (2 * read_len), hence not including the read lengths.
* -n or --iterations (default = 10) : number of complete MCMC runs (does not set the number of MCMC iterations, but the number of times the clustering runs are performed). Each run will have distinct results. 

#### Advanced/unimplemented Parameters ####

* -y or --ploidy (default = 2.0) : tumour ploidy. Currently not considered and assumed to be diploid
* -g or --germline (UNIMPLEMENTED!) : SV input can be optionally be automatically filtered against the germline by inputting the germline BAM file with the -g argument. Currently, all SVs are assumed to be germline filtered.

#### Beyond Advanced Usage ####

The package also contains a parameters.py file which has the following hard-coded parameters. Modify these with care.
```
* subclone_threshold      = 0.05 # throw out any subclones with frequency lower than this value
* subclone_sv_prop        = 0.08 # remove any cluster groups with fewer than this proportion of SVs clustering together
* subclone_diff           = 0.10 # merge any clusters within this range
* tolerate_svloss         = 0.30 # recluster if we lose more than x% of SVs from clustering/filtering
* init_iters              = 100000 # inital clustering mcmc iterations
* reclus_iters            = 50000 # reclustering iterations
* burn                    = 5000 # burn-in period
* thin                    = 10 # thinning parameter for sampling
* clus_limit              = 20 # maximum number of clusters generated by dirichlet process
```
### Calculating Coverage ###

Coverage can be approximately calculated using a script such as:

```
#!/bin/sh
bam=$1
genome=$2

bedtools random -g $genome -n 1000 -l 1000 > rand_intervals_1kb.bed
bedtools sort -chrThenSizeA -i rand_intervals_1kb.bed > rand_intervals_1kb.sort.bed
coverageBed -abam $bam -b rand_intervals_1kb.sort.bed > cov.txt

#in coverage_script.R
rlen = 100
interval = 1000
x <- read.delim(‘cov.txt’,header=F,stringsAsFactors=F)
print((mean(x[x$V3!=0,’V3’])*rlen)/interval
```

### Who do I talk to? ###

For queries, contact cmerom@gmail.com